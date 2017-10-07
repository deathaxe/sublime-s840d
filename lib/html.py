# -*- encoding: utf-8 -*-

POPUP_TEMPLATE = """
<body id="s840d">
<style>
    html.light {{
        --html-background: color(var(--background) blend(black 91%));
        --border-color: color(var(--html-background) blend(black 95%));
    }}
    html.dark {{
        --html-background: color(var(--background) blend(white 93%));
        --border-color: color(var(--html-background) blend(white 95%));
    }}
    html, body {{
        margin: 0;
        padding: 0;
        background-color: var(--html-background);
        color: var(--foreground);
    }}
    h1, h2 {{
        border-bottom: 1px solid var(--border-color);
        font-weight: normal;
        margin: 0;
        padding: 0.5rem 0.6rem;
    }}
    h1 {{
        color: var(--orangish);
        font-size: 1.0rem;
    }}
    h2 {{
        color: color(var(--html-background) blend(var(--foreground) 30%));
        font-size: 1.0rem;
        font-family: monospace;
    }}
    p {{
        margin: 0;
        padding: 0.5rem;
    }}
    a {{
        text-decoration: none;
    }}
</style>
{0}
</body>
"""


def encode(string):
    """Encode some critical characters to html entities."""
    return string.replace('&', '&amp;')           \
                 .replace('<', '&lt;')            \
                 .replace('>', '&gt;')            \
                 .replace('    ', '&nbsp;&nbsp;') \
                 .replace('\n', '<br>') if string else ''
