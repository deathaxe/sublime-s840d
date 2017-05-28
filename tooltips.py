# -*- encoding: utf-8 -*-

import gzip
import locale
import os.path
import sqlite3
import xml.dom.minidom as xml

import sublime
import sublime_plugin

doc_version = "25.09.2016"  # should not be here!
doc_cache = None            # path to s840d.sqlite
doc_langs = ['en']          # available langs in s840d.sqlite


def plugin_loaded():
    """Called by SublimeText after all plugins have been loaded."""
    sublime.set_timeout_async(lambda: cache_init(False), 5000)


class ToolTipCommand(sublime_plugin.EventListener):

    s840d_source = 'source.s840d_gcode | source.s840d_hmi'

    cur_word = None
    tip_html = None

    def on_hover(self, view, point, hover_zone):
        """Handle the hover event and show tooltip if needed."""
        if hover_zone != sublime.HOVER_TEXT:
            return

        # return if no s840d source code
        if not view.match_selector(point, self.s840d_source):
            return

        region = view.word(point)
        word = view.substr(region)
        if self.cur_word != word:
            self.cur_word = word
            # load current OS display language (e.g.: de_DE)
            lang = locale.getdefaultlocale()[0][:2].lower()
            # get description for machine data or nck variable
            if view.match_selector(point, 'support.variable.nck'):
                self.tip_html = get_var_desc(word, lang)
            # nothing found
            else:
                self.tip_html = ""

        # show the tool tip
        if not self.tip_html:
            return
        window_width = int(view.viewport_extent()[0]) - 64
        view.show_popup(
            self.tip_html, location=point, max_width=window_width,
            flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY)


def get_var_desc(word, lang):
    """Create the tooltip html for <word>.

    args:
        word    The word to create the tooltip for.
        lang    The language to try to use.
    """
    try:
        tip_html = """<style>
                   body { font-family: monospace; }
                   h1 { font-size: 1.1rem; }
                   h2 { font-size: 1.0rem; }
                   </style>"""

        with sqlite3.connect(doc_cache) as sql:
            # fallback to english if OS's language is not available
            if lang not in doc_langs:
                lang = 'en'

            row = sql.execute(
                """SELECT DISTINCT id,name,type,dim,brief,desc FROM vars
                WHERE name LIKE '$""" + word + "' AND lang LIKE '" + lang + "'"
                ).fetchone()

            if not row and lang != 'en':
                # fallback to english
                row = sql.execute(
                    """SELECT DISTINCT id,name,type,dim,brief,desc FROM vars
                    WHERE name LIKE '$""" + word + "' AND lang LIKE 'en'"
                    ).fetchone()

            # number, name and array dimension
            if row[0] and row[1]:
                tip_html += '<h1>N' + str(row[0]) + ' ' + row[1]
                if row[3] > 0:
                    tip_html += '[...]'
                tip_html += '</h1>'

            # brief
            tip_html += '<h2>' + html_encode(row[4]) + '</h2>'

            # data type
            if row[2]:
                tip_html += '<p><b>type:</b> '
                tip_html += html_encode(row[2])
                tip_html += '</p>'

            # description
            tip_html += html_encode(
                gzip.decompress(bytearray(row[5])).decode())
    except:
        tip_html = ""   # do description available

    return tip_html


def html_encode(string):
    """Encode some critical characters to html entities."""
    return string.replace('&', '&amp;')           \
                 .replace('<', '&lt;')            \
                 .replace('>', '&gt;')            \
                 .replace('    ', '&nbsp;&nbsp;') \
                 .replace('\n', '<br>')


def package_name():
    """The function returns the package name without path or extension.

    By default it is "CNC SINUMERIK 840D language support", but also
    works if the user renamed the package.
    """
    return os.path.splitext(os.path.basename(
           os.path.dirname(__file__)))[0]


def cache_init(force_update):
    """Create the 'tooltips.sqlite' database for quick access to tooltips.

    As parsing the whole bunch of XML files to find the requested content
    each time a tooltip is shown is quite inefficient as well as preserving
    the whole content int RAM all the time the xml documents are cached in
    a sqlite database, which makes it easy and fast to query but still
    provides the source of documentation as readable text. This way,
    interested persons could easily contribute further variable descriptions
    not yet included in this default package.
    """
    global doc_cache, doc_langs

    # path to the sqlite database storing tooltip texts
    doc_cache = os.path.join(sublime.cache_path(),
                             package_name(),
                             "tooltips.sqlite")

    with sqlite3.connect(doc_cache) as sql:

        if not force_update:
            # check if cache is up to date
            try:
                cache_version = sql.execute("""
                                            SELECT DISTINCT value
                                            FROM attr
                                            WHERE key LIKE 'version'
                                            """).fetchone()[0]
                if doc_version == cache_version:
                    doc_langs = cache_get_langs(sql)
                    return
            except:
                pass

        # this is only cache, no critical data
        sql.execute("PRAGMA journal_mode = OFF")

        # create variable description table if not exists
        sql.execute("""
                    CREATE TABLE IF NOT EXISTS vars (
                        id INTEGER DEFAULT 0,
                        name TEXT NOT NULL,
                        lang TEXT NOT NULL,
                        type TEXT,
                        disp TEXT,
                        dim INTEGER,
                        brief TEXT,
                        desc BLOB,
                        PRIMARY KEY (name, lang) )
                    """)

        sql.execute("BEGIN TRANSACTION")

        # clear variable description table
        sql.execute("DELETE FROM vars")

        # load machine data descriptions
        cache_add_resources(sql, "*.mdat")
        # load nck variable descriptions
        cache_add_resources(sql, "*.svar")

        # create attribute table
        sql.execute("""
                    CREATE TABLE IF NOT EXISTS attr (
                        key TEXT PRIMARY KEY,
                        value TEXT)
                    """)
        # add current package version to attributes
        sql.execute("""
                    INSERT OR REPLACE INTO attr
                    VALUES('version', '""" + doc_version + "')")

        # save the database
        sql.execute("VACUUM")
        sql.commit()

        # list all available languages
        #    ['de', 'en'] by default
        doc_langs = cache_get_langs(sql)

        # for developement purposes
        # dump_vars()


def cache_get_langs(sql):
    """Get the list of languages from tooltip database."""
    return [row[0] for row in sql.execute(
        "SELECT DISTINCT lang FROM vars").fetchall()]


def cache_add_resources(sql, file_spec):
    """Load documentation from sublime-package.

    The tooltip text is shipped with CreateMyConfig. As not everybody may have
    access to this tool, its files are shipped as copy with this package, too.
    """
    for file_name in sublime.find_resources(file_spec):
        lang = os.path.basename(os.path.dirname(file_name)).lower()
        # valid language codes have a length of 2 characters
        if len(lang) == 2:
            try:
                print("reloading docs", file_name)
                cache_add_xml(sql, xml.parseString(
                    sublime.load_binary_resource(file_name)), lang)
            except Exception as err:
                print("    error", err)


def cache_add_xml(sql, root, lang):
    """Add the content of an xml tree to the tooltip database.

    args:
        sql     The database connection
        root    The root node of the xml tree
        lang    The xml tree's content language
    """

    # machine data files do not include area prefixes in var names
    # so we need to map that here with the help of the id.
    # e.g. $MM_... =    9xxx
    #            $MN_... = 10xxx to 18xxx
    #            $ON_... = 19xxx
    #            ...
    prefixes = {
        '9': '$MM_',
        '10': '$MN_', '11': '$MN_', '12': '$MN_', '13': '$MN_', '14': '$MN_',
        '15': '$MN_', '16': '$MN_', '17': '$MN_', '18': '$MN_', '19': '$ON_',
        '20': '$MC_', '21': '$MC_', '22': '$MC_', '23': '$MC_', '24': '$MC_',
        '25': '$MC_', '26': '$MC_', '27': '$MC_', '28': '$MC_', '29': '$OC_',
        '30': '$MA_', '31': '$MA_', '32': '$MA_', '33': '$MA_', '34': '$MA_',
        '35': '$MA_', '36': '$MA_', '37': '$MA_', '38': '$MA_', '39': '$OA_',
        '41': '$SN_', '42': '$SC_', '43': '$SA_',
        '51': '$MNS_', '52': '$MCS_', '53': '$MAS_',
        '54': '$SNS_', '55': '$SCS_', '56': '$SAS_'
    }

    # all variables are listed as <parameter>
    for param in root.getElementsByTagName("parameter"):

        try:
            # machine data number
            i_id = int(param.getAttribute("number"))
        except:
            i_id = 0

        s_name = None
        s_brief = None
        s_desc = None

        for child in param.childNodes:
            if child.nodeType == xml.Node.ELEMENT_NODE:
                tag_name = child.tagName.lower()
                tag_text = child.childNodes[0].data.strip()
                if tag_name == "name":
                    try:
                        # try to add machine data prefix
                        s_name = prefixes[str(int(i_id/1000))] + tag_text
                    except:
                        s_name = tag_text
                elif tag_name == "brief":
                    s_brief = tag_text
                elif tag_name == "description":
                    s_desc = gzip.compress(bytearray(tag_text.encode()))

        if s_name and (s_brief or s_desc):

            try:
                # data type: BOOLEAN, BYTE, INT, DWORD, DOUBLE, STRING
                s_type = param.getAttribute("type")
            except:
                s_type = ""

            try:
                # display as: DECIMAL, HEX, ASCII, RESTRICTEDASCII
                s_disp = param.getAttribute("display")
            except:
                s_disp = ""

            try:
                # array dimensions: 0 = no array
                i_dim = int(param.getAttribute("dim"))
                if i_dim > 0:
                    # STRING arrays dispayed as ASCII are handled as
                    # comma seperated text:
                    # SCS_J_MEA_PROTOCOL_FILE has dim = 1 but is stored
                    # as SCS_J_MEA_PROTOCOL_FILE = "FILENAME" instead
                    # of SCS_J_MEA_PROTOCOL_FILE[0] = "FILENAME"
                    if "ASCII" in s_disp:
                        i_dim -= 1

                if s_name[:3] in ("$MA", "$SA"):
                    # axis machine data's dim attributes don't store axis
                    # index so we need to correct this here to make the
                    # variable behave like any other.
                    i_dim += 1
            except:
                i_dim = 0

            sql.execute(
                'INSERT OR REPLACE INTO vars VALUES (?,?,?,?,?,?,?,?)',
                (i_id, s_name, lang, s_type, s_disp, i_dim, s_brief, s_desc))


def dump_vars():
    """Dump all variables from database into text files.

    This function is for developement to extract available NC variables and
    machine data from the newly created database. This is an easy way to get
    the list of valid variables from the CreateMyConfig documentation as
    another source of information.
    """
    path = os.path.join(sublime.packages_path(), package_name())
    # dump only, if package is not packed as suplime-package
    if not os.path.isdir(path):
        return

    with sqlite3.connect(doc_cache) as sql:

        # output all machine data
        with open(os.path.join(path, "cmc_doc_md.tea"), "w") as out:
            for row in sql.execute("""
                                   SELECT DISTINCT id,name,dim
                                   FROM vars
                                   WHERE id > 0
                                   """).fetchall():

                # print number and variable name
                line = 'N' + str(row[0]) + ' ' + row[1]
                dim = row[2]

                # print an array index
                if dim > 0:
                    line += '['
                    while dim > 0:
                        line += '0,'
                        dim -= 1
                    line = line[:-1] + ']'

                out.write(line + '\n')

        # output all other variables
        with open(os.path.join(path, "cmc_doc_vars.tea"), "w") as out:
            for row in sql.execute("""
                                   SELECT DISTINCT name,dim
                                   FROM vars
                                   WHERE id = 0
                                   """).fetchall():

                # print number and variable name
                line = row[0]
                dim = row[1]

                # print an array index
                if dim > 0:
                    line += '['
                    while dim > 0:
                        line += '0,'
                        dim -= 1
                    line = line[:-1] + ']'

                out.write(line + '\n')
