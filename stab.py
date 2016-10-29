#!/usr/bin/env python3
import os
import sys
import yaml
import mistune
from jinja2 import Environment, FileSystemLoader

ALLOWED = {'.md', '.mkd', '.markdown'}
is_allowed = lambda x: os.path.splitext(x)[1] in ALLOWED

absjoin = lambda x, y: os.path.abspath(os.path.join(x, y))
ROOT_DIR = os.getcwd()
OUT_DIR = absjoin(ROOT_DIR, '_site')
TEMPLATE_DIR = absjoin(ROOT_DIR, '_layouts')

config = yaml.load(open(absjoin(ROOT_DIR, '_config.yml')).read())
blog_dir_name = config.get('blog_dir', 'blog')
blog_dir = absjoin(ROOT_DIR, blog_dir_name)
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


def build_blog(markdown):
    for fname in os.listdir(blog_dir):
        fpath = absjoin(blog_dir, fname)
        if os.path.isfile(fpath) and is_allowed(fname):
            meta, content = extract(fpath)
            html = markdown(content)
            template = meta.get('layout', default_template)
            templater = jinja_env.get_template(template)
            info = config.copy()
            info['content'] = html
            info.update(meta)
            with open(absjoin(blog_dir, os.path.splitext(fname)[0] + '.html'), 'w') as fp:
                fp.write(templater.render(info))


def main():
    markdown = mistune.Markdown()
    build_blog(markdown)

if __name__ == '__main__':
    main()
