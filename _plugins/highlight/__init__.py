from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from stab import Plugin
import mistune

class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)


class MistuneRender(Plugin):
    def __init__(self):
        self.markdown = mistune.Markdown(renderer=HighlightRenderer())

    def to_html(self, content):
        return self.markdown(content)


def load_plugin():
    return {'inject': 'MistuneRender', 'type': 'render' }
