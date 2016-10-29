#!/usr/bin/env python3
import os
import sys
import yaml
import mistune
from jinja2 import Environment, FileSystemLoader
import importlib

ALLOWED = {'.md', '.mkd', '.markdown'}
is_allowed = lambda x: os.path.splitext(x)[1] in ALLOWED

absjoin = lambda x, y: os.path.abspath(os.path.join(x, y))
ROOT_DIR = os.getcwd()
OUT_DIR = absjoin(ROOT_DIR, '_site')
TEMPLATE_DIR = absjoin(ROOT_DIR, '_layouts')

config = yaml.load(open(absjoin(ROOT_DIR, '_config.yml')).read())
blog_dir_name = config.get('blog_dir', 'blog')
blog_dir = absjoin(ROOT_DIR, blog_dir_name)
default_template = config.get('layout', 'post')
plugins_dir_name = config.get('plugins_dir', '_plugins')

jinja_loader = FileSystemLoader(TEMPLATE_DIR)
jinja_env = Environment(loader=jinja_loader)
jinja_env.filters['datetimeformat'] = lambda x, y: x.strftime(y)


class Plugin:
    pass


class Render(Plugin):
    def __init__(self):
        self.markdown = mistune.Markdown()

    def to_html(self, content):
        return self.markdown(content)


def extract(fpath):
    meta, content, first_line, meta_parsed = [], [], True, False
    with open(fpath) as fp:
        for line in fp:
            if line.strip() == '---' and not meta_parsed:
                if not first_line:
                    meta_parsed = True
                first_line = False
            elif not meta_parsed:
                meta.append(line)
            else:
                content.append(line)
        try:
            return yaml.load('\n'.join(meta)), '\n'.join(content)
        except:
            raise SystemExit('File with invalid yaml meta block: ' + fpath)


def build_blog(renderer):
    for fname in os.listdir(blog_dir):
        fpath = absjoin(blog_dir, fname)
        if os.path.isfile(fpath) and is_allowed(fname):
            meta, content = extract(fpath)
            html = renderer.to_html(content)
            template = meta.get('layout', default_template)
            templater = jinja_env.get_template(template + '.html')
            info = config.copy()
            info['content'] = html
            info.update(meta)
            with open(absjoin(blog_dir, os.path.splitext(fname)[0] + '.html'), 'w') as fp:
                fp.write(templater.render(info))


def main():
    plugins = config.get('plugins', [])
    active_plugin = {'render': Render}
    inject_plugin = lambda module, inject, type: active_plugin.update({type: getattr(module, inject)})

    for plugin in plugins:
        m = importlib.import_module(plugins_dir_name + '.' + plugin)
        inject_plugin(module=m, **m.load_plugin())

    renderer = active_plugin['render']()
    build_blog(renderer)

if __name__ == '__main__':
    main()
