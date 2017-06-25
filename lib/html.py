# -*- encoding: utf-8 -*-

POPUP_TEMPLATE = """
<body id="s840d">
<style>
    body {{
        margin: 0;
        padding: 0;
    }}
    h1, h2 {{
        border-bottom: 1px solid color(var(--background) blend(white 80%));
        font-weight: normal;
        margin: 0;
        padding: 0.5rem;
    }}
    h1 {{
        color: color(var(--background) blend(var(--orangish) 20%));
        font-size: 1.0rem;
    }}
    h2 {{
        color: color(var(--background) blend(var(--foreground) 30%));
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
