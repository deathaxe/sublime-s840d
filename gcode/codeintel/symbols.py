# -*- encoding: utf-8 -*-
import re

from ... import lib

SYMBOLS = (
    ('entity.name.macro', True, 'macro'),
    ('entity.name.tag.label', False, 'label'),
    ('meta.definition.variable variable.other', True, 'variable'),
    ('variable.parameter.procedure', True, 'parameter'),
)


def completions(view, prefix, location):
    """Create auto-completions from scopes.

    Arguments:
        prefix (string):
            the string intended to find completion for
        location (int):
            the text position of the first character of prefix

    Returns:
        list [[trigger, contents], ...]:
            The list of symbols which match prefix distinquished by type.
    """
    selector = '- meta.definition - meta.redefinition'
    if not view.match_selector(location, selector):
        return None

    for selector, above_only, type_name in SYMBOLS:
        symbols = find_nearest_symbols(view, selector, location, above_only)
        for symbol, region in symbols.items():
            yield ('\t  '.join((symbol, type_name)), symbol)


def tooltip(view, location, keyword):
    """Lookup the keyword in the list of local definitions and format tooltip.

    Arguments:
        view (sublime.View):
            the view the symbol is defined in
        location (int):
            the text position of keyword in the buffer
        keyword (string):
            the symbol name as collected by _Symbol List.tmPreferences_

    Returns:
        string: The html encoded content to display in the popup.
    """
    for selector, above_only, type_name in SYMBOLS:
        region = find_nearest_symbol(
            view, keyword, selector, location, above_only)
        if region:
            # the tooltip function for the symbol type
            factory = globals()[type_name + '_tooltip']
            return factory(view, region, keyword)
    return None


def find_definition(view, location, keyword):
    """Find the local definition of a keyword in the view.

    Uses the tuple of scopes to search for the local definition of keyword.

    Arguments:
        view (sublime.View):
            the view the keyword is defined in
        location (int):
            the text position to use to decide which find results to include
        keyword (string):
            the symbol name as collected by _Symbol List.tmPreferences_

    Returns:
        sublime.Region if the keyword is defined in the view or None otherwise
    """
    for selector, above_only, _ in SYMBOLS:
        region = find_nearest_symbol(
            view, keyword, selector, location, above_only)
        if region:
            return region
    return None


def find_nearest_symbols(view, selector, location, above_only=True):
    """Find nearest unique symbols by selector.

    The function is a wrapper around `sublime.View.find_by_selector()` to
    return unique symbols. It is an alternative to `sublime.View.symbols()`
    which does not require symbols to be defined in a _*.tmPreference_ file.

    Arguments:
        view (sublime.View):
            the view the symbol is defined in
        selector (string):
            the scope query to pass to view.find_by_selector
        location (int):
            the text position to use to decide which find results to include
        above_only (bool):
            if True, skip all symbols followed by location (default: True)

    Returns:
        dict {symbol: region}:
            the dictionary using the symbol as key and its region as value
    """
    symbols = {}
    for region in view.find_by_selector(selector):
        # ignore declarations following the current cursor position
        if above_only and region.a > location:
            break
        symbol = view.substr(region)
        # check whether we already caught a symbol with a lower distance
        sym = symbols.get(symbol)
        if sym and abs(sym.a - location) < abs(region.a - location):
            continue
        # finally add the new symbol or update an existing one
        symbols[symbol] = region
    return symbols


def find_nearest_symbol(view, what, selector, location, above_only=True):
    """Find the region of the declaration of `what`.

    The function is a wrapper around sublime.View.find_by_selector() to find
    the position of the nearest unique symbol by `selector` and `name`.

    Arguments:
        view (sublime.View):
            the view the symbol is defined in
        what (string):
            the name of the symbol to search for
        selector (string):
            the scope query to pass to view.find_by_selector
        location (int):
            the text position to use to decide which find results to include
        above_only (bool):
            if True, skip all symbols followed by location (default: True)

    Returns:
        sublime.Region:
            the region of the found element or None
    """
    found = None
    for region in view.find_by_selector(selector):
        # ignore declarations following the current cursor position
        if above_only and region.a > location:
            break
        symbol = view.substr(region)
        if symbol != what:
            continue
        # check whether we already caught a symbol with a lower distance
        if found and abs(found.a - location) < abs(region.a - location):
            continue
        # finally add the new symbol or update an existing one
        found = region
    return found


def parameter_tooltip(view, region, symbol):
    """Format the tooltip for procedure argument definition.

    Note:
        Function name must match the parameter type name in SYMBOLS.
        Otherwise tooltip() fails.

    Arguments:
        view (sublime.View):
            the view the symbol is defined in
        region (sublime.Region):
            the start and end point of where the symbol is defined
        symbol (string):
            the symbol name as collected by _Symbol List.tmPreferences_

    Returns:
        string: The html encoded content to display in the popup.
    """
    info = get_symbol_info_for_argument(view, region, symbol)
    return (
        '<h1>{syntax}</h1>'
        '<h2>{brief} at <a href="scroll:{location}">{blockno}</a></h2>'
        '<p>{desc}</p>'.format(**info)
    )


def macro_tooltip(view, region, symbol):
    """Format the tooltip for local macro definition.

    Note:
        Function name must match the parameter type name in SYMBOLS.
        Otherwise tooltip() fails.

    Arguments:
        view (sublime.View):
            the view the symbol is defined in
        region (sublime.Region):
            the start and end point of where the symbol is defined
        symbol (string):
            the symbol name as collected by _Symbol List.tmPreferences_

    Returns:
        string: The html encoded content to display in the popup.
    """
    info = get_symbol_info_for_macro(view, region, symbol)
    return (
        '<h1>{syntax}</h1>'
        '<h2>{brief} at <a href="scroll:{location}">{blockno}</a></h2>'
        '<p>{desc}</p>'.format(**info)
    )


def variable_tooltip(view, region, symbol):
    """Format the tooltip for local variable definition.

    Note:
        Function name must match the parameter type name in SYMBOLS.
        Otherwise tooltip() fails.

    Arguments:
        view (sublime.View):
            the view the symbol is defined in
        region (sublime.Region):
            the start and end point of where the symbol is defined
        symbol (string):
            the symbol name as collected by _Symbol List.tmPreferences_

    Returns:
        string: The html encoded content to display in the popup.
    """
    info = get_symbol_info_for_variable(view, region, symbol)
    return (
        '<h1>{syntax}</h1>'
        '<h2>{brief} at <a href="scroll:{location}">{blockno}</a></h2>'
        '<p>{desc}</p>'.format(**info)
    )


def label_tooltip(view, region, symbol):
    """Format the tooltip for local goto labels.

    Note:
        Function name must match the parameter type name in SYMBOLS.
        Otherwise tooltip() fails.

    Arguments:
        view (sublime.View):
            the view the symbol is defined in
        region (sublime.Region):
            the start and end point of where the symbol is defined
        symbol (string):
            the symbol name as collected by _Symbol List.tmPreferences_

    Returns:
        string: The html encoded content to display in the popup.
    """
    info = get_symbol_info_for_label(view, region, symbol)
    return (
        '<h1>{syntax}</h1>'
        '<h2>{brief} at <a href="scroll:{location}">{blockno}</a></h2>'
        '<p>{desc}</p>'.format(**info)
    )


def get_symbol_info_for_argument(view, region, symbol):
    """Parse view content to read symbol information.

    Arguments:
        view (sublime.View):
            the view the symbol is defined in
        region (sublime.Region):
            the start and end point of where the symbol is defined
        symbol (string):
            the symbol name as collected by _Symbol List.tmPreferences_

    Returns:
        dict: { blockno, symbol, type, syntax, brief, desc }
                blockno: block number (e.g. N10) if any
                symbol:  copy of symbol
                type:    variable data type
                syntax:  what the definition looks like
                brief:   a short description
                desc:    a long description (comment)
    """
    # read the whole line
    line = view.substr(view.line(region)).strip()
    # get data type and inline comment
    pattern = (
        # block number if any
        r'(N\d+)?[ \t]*'
        # procedure name and arguments (ignore)
        r'.*?'
        # call by reference
        r'((?:VAR[ \t]+)?'
        # definition type
        r'(?:AXIS|BOOL|INT|FRAME|REAL|STRING(?:\[[^\[]*\])?))\W+'
        # the parameter we are looking for
        r'({0})'
        # inital value
        r'(?:[^,=\)]*=[ \t]*([^,\)]+))?'.format(symbol)
    )
    match = re.match(pattern, line, re.IGNORECASE)
    blockno, typdef, variable, value = match.groups() if match else (
        None, '', symbol, '')
    location = region.begin()
    if not blockno:
        blockno = 'row {}'.format(view.rowcol(location)[0] + 1)
    return {
        'location': location,
        'blockno': blockno,
        'symbol': variable,
        'type': typdef,
        'syntax': '{typdef} {variable}'.format(**locals()),
        'brief': 'procedure argument',
        'desc': 'No description found.'
    }


def get_symbol_info_for_macro(view, region, symbol):
    """Parse view content to read symbol information.

    Arguments:
        view (sublime.View):
            the view the symbol is defined in
        region (sublime.Region):
            the start and end point of where the symbol is defined
        symbol (string):
            the symbol name as collected by _Symbol List.tmPreferences_

    Returns:
        dict: { blockno, symbol, type, syntax, brief, desc }
                blockno: block number (e.g. N10) if any
                symbol:  copy of symbol
                type:   '' (not used)
                syntax:  what the definition looks like
                brief:   a short description
                desc:    a long description (comment)
    """
    # read the whole line
    line = view.substr(view.line(region)).strip()
    # get data type and inline comment
    pattern = (
        # block number if any
        r'(N\d+)?[ \t]*'
        # definition type (strip DEFINE symbol AS)
        r'DEFINE[ \t]+(\w+?)[ \t]+AS[ \t]+'
        # macro action block
        r'([^;]*)'
        # the comment at the end of the line if any
        r'(?:;[ \t]*(.+))?'
    )
    match = re.match(pattern, line, re.IGNORECASE)
    blockno, macro, action, comment = match.groups() if match else (
        None, symbol, None, None)
    location = region.begin()
    if not blockno:
        blockno = 'row {}'.format(view.rowcol(location)[0] + 1)
    return {
        'location': location,
        'blockno': blockno,
        'symbol': macro,
        'type': '',
        'syntax': '{macro} ⇨ {action}'.format(**locals()),
        'brief': 'local macro',
        'desc': lib.html.encode(comment) or 'No description found.'
    }


def get_symbol_info_for_variable(view, region, symbol):
    """Parse view content to read symbol information.

    Arguments:
        view (sublime.View):
            the view the symbol is defined in
        region (sublime.Region):
            the start and end point of where the symbol is defined
        symbol (string):
            the symbol name as collected by _Symbol List.tmPreferences_

    Returns:
        dict: { blockno, symbol, type, syntax, brief, desc }
                blockno: block number (e.g. N10) if any
                symbol:  copy of symbol
                type:    variable data type
                syntax:  what the definition looks like
                brief:   a short description
                desc:    a long description (comment)
    """
    # read the whole line
    line = view.substr(view.line(region)).strip()
    # get data type and inline comment
    pattern = (
        # block number if any
        r'(N\d+)?[ \t]*'
        # definition type (strip DEF keyword)
        r'DEF[ \t]+.*?(AXIS|BOOL|INT|FRAME|REAL|STRING(?:\[[^\[]*\])?)\W+'
        # all operands and initializations (don't care about)
        r'[^;]+'
        # the comment at the end of the line if any
        r'(?:;[ \t]*(.+))?'
    )
    match = re.match(pattern, line, re.IGNORECASE)
    blockno, typdef, comment = match.groups() if match else ('', '', None)
    location = region.begin()
    if not blockno:
        blockno = 'row {}'.format(view.rowcol(location)[0] + 1)
    return {
        'location': location,
        'blockno': blockno,
        'symbol': symbol,
        'type': typdef,
        'syntax': '{typdef} {symbol}'.format(**locals()),
        'brief': 'local variable',
        'desc': lib.html.encode(comment) or 'No description found.'
    }


def get_symbol_info_for_label(view, region, symbol):
    """Parse view content to read symbol information.

    Arguments:
        view (sublime.View):
            the view the symbol is defined in
        region (sublime.Region):
            the start and end point of where the symbol is defined
        symbol (string):
            the symbol name as collected by _Symbol List.tmPreferences_

    Returns:
        dict: { blockno, symbol, type, syntax, brief, desc }
                blockno: block number (e.g. N10) if any
                symbol:  copy of symbol
                type:   '' (not used)
                syntax:  what the definition looks like
                brief:   a short description
                desc:    a long description (comment)
    """
    # read the whole line
    line = view.substr(view.line(region)).strip()
    # get data type and inline comment
    pattern = (
        # block number if any
        r'(N\d+)?[ \t]*'
        # label
        r'([^:]*):'
        # block content
        r'([^;]*)'
        # the comment at the end of the line if any
        r'(?:;[ \t]*(.+))?'
    )
    match = re.match(pattern, line, re.IGNORECASE)
    blockno, label, action, comment = match.groups() if match else (
        None, symbol, '', '')
    location = region.begin()
    if not blockno:
        blockno = 'row {}'.format(view.rowcol(location)[0] + 1)
    return {
        'location': location,
        'blockno': blockno,
        'symbol': label,
        'type': '',
        'syntax': label + ':',
        'brief': 'label',
        'desc': lib.html.encode(comment) or 'No description found.'
    }
