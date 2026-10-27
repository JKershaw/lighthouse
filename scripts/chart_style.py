"""Shared, dependency-free SVG chart tokens. See notes/chart-style.md."""
from html import escape

SANS = '"Source Sans 3", "Source Sans Pro", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
# Theme backgrounds match site/assets/site.css. Text and mark colours are opaque.
THEMES = {
    'light': {'bg': '#fbfaf7', 'ink': '#1f1f1f', 'muted': '#5d5850', 'grid': '#e3ddd1',
              'teal': '#1f6576', 'amber': '#93600c', 'purple': '#78549b', 'blue': '#2866ab', 'neutral': '#74716a'},
    'dark': {'bg': '#15191b', 'ink': '#e6e2d9', 'muted': '#aaa498', 'grid': '#2f3538',
             'teal': '#8ec4d4', 'amber': '#e0a650', 'purple': '#c6a7df', 'blue': '#8bb9ed', 'neutral': '#aaa498'},
}
SERIES = ('teal', 'amber', 'purple', 'blue')
DASHES = ('', '7 3', '2 3', '8 3 2 3')


def css():
    """Embed in the SVG itself so both inline and <img> charts follow the theme."""
    def tokens(theme):
        return ' '.join(f'--{k}:{v};' for k, v in THEMES[theme].items())
    return ('<style>\nsvg { ' + tokens('light') + ' color-scheme:light dark; }\n'
            '@media (prefers-color-scheme: dark) { svg { ' + tokens('dark') + ' } }\n'
            'text { font-family:' + SANS + '; font-variant-numeric:tabular-nums lining-nums; fill:var(--ink); }\n'
            '.head { font-size:17px; font-weight:600; }\n'
            '.sub { font-size:13px; fill:var(--muted); }\n'
            '.ann,.ax { font-size:12px; fill:var(--muted); }\n'
            '.nm { font-size:12px; font-weight:600; }\n'
            '.note { font-size:11.5px; fill:var(--muted); }\n'
            '.sec { font-size:14px; font-weight:600; }\n'
            '.grid { stroke:var(--grid); stroke-width:1; }\n'
            '.axis { stroke:var(--muted); stroke-width:1; }\n'
            '</style>')


def svg_open(width, height, title, description):
    """Accessible root and escaped plain-text title/description, with theme style."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" role="img" aria-labelledby="chart-title chart-desc">\n'
            f'<title id="chart-title">{escape(title)}</title>\n'
            f'<desc id="chart-desc">{escape(description)}</desc>\n' + css())


def series_stroke(index):
    """A second cue accompanies each categorical colour in line charts."""
    colour = SERIES[index % len(SERIES)]
    dash = DASHES[index % len(DASHES)]
    return f'stroke="var(--{colour})" stroke-width="2.5"' + (f' stroke-dasharray="{dash}"' if dash else '')
