import gzip
import os.path
import sqlite3
import xml.dom.minidom as xml

import sublime

from .. import lib

doc_version = "15.09.2018"  # should not be here!


def tooltip(view, keyword, lang='en'):
    """Create the tooltip html for <keyword>.

    Arguments:
        view (sublime.View):
            the view to create the tooltip for
        keyword (string):
            the keyword to create the tooltip for
        lang (string):
            the language to try to use
    """
    return ''.join(_generate_tooltip(keyword, lang))


def _generate_tooltip(word, lang):
    """Generate the tooltip html for <word>.

    Arguments:
        word (string):
            the word to create the tooltip for
        lang (string):
            the language to try to use

    Yields:
        string: tooltip content tag by tag
    """
    doc_cache, doc_langs = cache_init(False)
    with sqlite3.connect(doc_cache) as sql:
        # fallback to english if OS's language is not available
        if lang not in doc_langs:
            lang = 'en'

        row = sql.execute(
            """SELECT DISTINCT id,name,type,dim,brief,desc FROM vars
            WHERE (name LIKE '$""" + word + "' OR name LIKE'" + word + "') AND lang LIKE '" + lang + "'"
            ).fetchone()

        if not row and lang != 'en':
            # fallback to english
            row = sql.execute(
                """SELECT DISTINCT id,name,type,dim,brief,desc FROM vars
                WHERE name LIKE '$""" + word + "' OR name LIKE'" + word + "' AND lang LIKE 'en'"
                ).fetchone()

        if not row:
            return ''

        data_id, data_name, data_type, data_dimension, brief, desc = row

        # number, name and array dimension
        if data_name:
            if data_dimension > 0:
                s_dim = '[...' + ',...' * (data_dimension - 1) + ']'
            else:
                s_dim = ''

            if data_id:
                yield '<h1>N{0} {1}{2}</h1>'.format(
                    data_id, lib.html.encode(data_name), s_dim)
            else:
                yield '<h1>{0}{1}</h1>'.format(
                    lib.html.encode(data_name), s_dim)

        # brief
        if brief:
            yield '<h2>{0}</h2>'.format(lib.html.encode(brief))
        # data type
        if data_type:
            yield '<h2><b>type:</b> {0}</h2>'.format(lib.html.encode(data_type))
        # description
        if desc:
            yield '<p>{0}</p>'.format(lib.html.encode(
                gzip.decompress(bytearray(desc)).decode()))


def package_name():
    """The function returns the package name without path or extension.

    By default it is "CNC SINUMERIK 840D language support", but also
    works if the user renamed the package.
    """
    return __package__.split('.')[0]


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
    if hasattr(cache_init, 'docs') and hasattr(cache_init, 'langs'):
        return cache_init.docs, cache_init.langs

    # path to the sqlite database storing tooltip texts
    cache_init.docs = os.path.join(
        sublime.cache_path(), package_name(), "tooltips.sqlite")

    with sqlite3.connect(cache_init.docs) as sql:

        if not force_update:
            # check if cache is up to date
            try:
                cache_version = sql.execute("""
                                            SELECT DISTINCT value
                                            FROM attr
                                            WHERE key LIKE 'version'
                                            """).fetchone()[0]
                if doc_version == cache_version:
                    cache_init.langs = cache_get_langs(sql)
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
        sql.commit()
        sql.execute("VACUUM")

        # list all available languages
        #    ['de', 'en'] by default
        cache_init.langs = cache_get_langs(sql)

        # for developement purposes
        # dump_vars()
        return cache_init.docs, cache_init.langs


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
                if child.childNodes:
                    tag_text = child.childNodes[0].data.strip()
                else:
                    tag_text = ""
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

    doc_cache, _ = cache_init(False)

    with sqlite3.connect(doc_cache) as sql:

        # output all machine data
        with open(os.path.join(path, "cmc_doc_md.tea"), "w") as out:
            for row in sql.execute("""
                                   SELECT DISTINCT id,name,dim,brief
                                   FROM vars
                                   WHERE id > 0 and lang is "en"
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

                if row[3]:
                    line += ' ;' + row[3]

                out.write(line + '\n')

        # output all other variables
        with open(os.path.join(path, "cmc_doc_vars.tea"), "w") as out:
            for row in sql.execute("""
                                   SELECT DISTINCT name,dim,brief
                                   FROM vars
                                   WHERE id = 0 and lang is "en"
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

                if row[2]:
                    line += ' ;' + row[2]

                out.write(line + '\n')
