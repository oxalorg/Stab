#!/usr/bin/env python3
import os, sys, yaml, mistune, importlib, collections
from jinja2 import Environment, FileSystemLoader

ALLOWED = {'.md', '.mkd', '.markdown'}
is_allowed = lambda x: os.path.splitext(x)[1] in ALLOWED
IGNORED = {'README.md'}
is_ignored = lambda x: x in IGNORED
DIR_IGNORED = {'_', '.'} #+ set(config.get('dir_ignored', []))
dir_is_ignored = lambda x: any(os.path.basename(x).startswith(y) for y in DIR_IGNORED)

absjoin = lambda x, y: os.path.abspath(os.path.join(x, y))
ROOT_DIR = os.getcwd()
OUT_DIR = absjoin(ROOT_DIR, '_site')
TEMPLATE_DIR = absjoin(ROOT_DIR, '_layouts')

config = yaml.load(open(absjoin(ROOT_DIR, '_config.yml')).read())
build_dirs_name = config.get('build_dirs', 'blog')
build_dirs = absjoin(ROOT_DIR, build_dirs_name)
default_template = config.get('layout', 'post')
plugins_dir_name = config.get('plugins_dir', '_plugins')

jinja_loader = FileSystemLoader(TEMPLATE_DIR)
jinja_env = Environment(loader=jinja_loader)
jinja_env.filters['datetimeformat'] = lambda x, y: x.strftime(y)

site = collections.defaultdict(list)
site['pages'] = {}
site['categories'] = collections.defaultdict(list)
site['tags'] = collections.defaultdict(list)


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
            if line.strip() == '---' and first_line: first_line = False
            elif line.strip() == '---' and not first_line and not meta_parsed: meta_parsed = True
            elif not meta_parsed: meta.append(line)
            else: content.append(line)
        try:
            return yaml.load('\n'.join(meta)), ''.join(content)
        except:
            raise SystemExit('File with invalid yaml meta block: ' + fpath)

def walk(markdown, func):
    for root, dirs, files in os.walk(ROOT_DIR):
        if dir_is_ignored(root): continue
        for fname in files:
            fpath = absjoin(root, fname)
            if is_allowed(fname) and not is_ignored(fname):
                func(root, fname, fpath, markdown)


def build(root, fname, fpath, markdown):
    page = site['pages'][os.path.relpath(fpath, ROOT_DIR)]
    template = page.get('layout', default_template) + '.html'
    templater = jinja_env.get_template(template)
    info = config.copy()
    info['content'] = page['content']
    info.update(page)
    with open(absjoin(root, os.path.splitext(fname)[0] + '.html'), 'w') as fp:
        fp.write(templater.render(info))


def index(root, fname, fpath, renderer):
    meta, text = extract(fpath)
    page_id = os.path.relpath(fpath, ROOT_DIR)
    category = os.path.dirname(page_id)
    meta.update({'text': text, 'content': renderer.to_html(text), 'category': category, 'slug': os.path.splitext(fname)[0]})
    site['pages'].update({ page_id: meta })
    site['categories'][category].append(page_id)
    for tag in meta.get('tags', []):
        site['tags'][tag].append(page_id)


def main():
    plugins = config.get('plugins', [])
    active_plugin = {'render': Render}
    inject_plugin = lambda module, inject, type: active_plugin.update({type: getattr(module, inject)})

    for plugin in plugins:
        m = importlib.import_module(plugins_dir_name + '.' + plugin)
        inject_plugin(module=m, **m.load_plugin())

    renderer = active_plugin['render']()

    walk(renderer, index)
    jinja_env.globals = {'site': site}
    walk(renderer, build)


if __name__ == '__main__':
    main()
