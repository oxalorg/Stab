#!/usr/bin/env python3
import os
import sys
import yaml
import mistune
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
default_template = config.get('layout', 'post.html')

jinja_loader = FileSystemLoader(TEMPLATE_DIR)
jinja_env = Environment(loader=jinja_loader)
jinja_env.filters['datetimeformat'] = lambda x, y: x.strftime(y)


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


def build(markdown):
    for root, dirs, files in os.walk(ROOT_DIR):
        if dir_is_ignored(root): continue
        for fname in files:
            fpath = absjoin(root, fname)
            if is_allowed(fname) and not is_ignored(fname):
                meta, content = extract(fpath)
                html = markdown(content)
                template = meta.get('layout', default_template)
                templater = jinja_env.get_template(template)
                info = config.copy()
                info['content'] = html
                info.update(meta)
                with open(absjoin(root, os.path.splitext(fname)[0] + '.html'), 'w') as fp:
                    fp.write(templater.render(info))


def main():
    markdown = mistune.Markdown()
    build(markdown)

if __name__ == '__main__':
    main()
