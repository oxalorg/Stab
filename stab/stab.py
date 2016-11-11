#!/usr/bin/env python3
import os, sys, yaml, mistune, importlib, collections, argparse, logging, time
from jinja2 import Environment, FileSystemLoader

absjoin = lambda x, y: os.path.abspath(os.path.join(x, y))


class Stab:
    ALLOWED, IGNORED = [], []

    def __init__(self, ROOT_DIR):
        self.ROOT_DIR = os.path.abspath(ROOT_DIR)
        self.set_defaults()
        self.set_utils()
        self.init_site()
        self.init_jinja()
        self.md2html = mistune.Markdown()

    def set_defaults(self):
        self.config = yaml.load(open(absjoin(self.ROOT_DIR, '_config.yml')).read())
        self.default_template = self.config.get('default_layout')
        self.ALLOWED = set(self.config.get('allowed', []))
        self.IGNORED = set(self.config.get('ignored', []))
        self.DIR_IGNORED = {'_', '.'} | set(self.config.get('dir_ignored', []))

    def set_utils(self):
        self.is_allowed = lambda x: os.path.splitext(x)[1] in self.ALLOWED
        self.is_ignored = lambda x: x in self.IGNORED
        self.is_dir_ignored = lambda x: any(os.path.basename(x).startswith(y) for y in self.DIR_IGNORED)

    def init_site(self):
        self.site = collections.defaultdict(list)
        self.site['pages'] = {}
        self.site['categories'] = collections.defaultdict(list)
        self.site['tags'] = collections.defaultdict(list)

    def init_jinja(self):
        self.TEMPLATE_DIR = absjoin(self.ROOT_DIR, '_layouts')
        self.jinja_loader = FileSystemLoader(self.TEMPLATE_DIR)
        self.jinja_env = Environment(loader=self.jinja_loader)
        self.jinja_env.filters['datetimeformat'] = lambda x, y: x.strftime(y)
        self.jinja_env.globals = {'site': self.site}

    def render(self, content):
        return self.md2html(content)

    def walk(self, func):
        for root, dirs, files in os.walk(self.ROOT_DIR):
            if self.is_dir_ignored(root): continue
            for fname in files:
                fpath = absjoin(root, fname)
                if self.is_allowed(fname) and not self.is_ignored(fname):
                    func(fname, fpath)

    def index(self, fname, fpath):
        meta, text = self._extract(fpath)
        page_id = os.path.relpath(fpath, self.ROOT_DIR)
        category = os.path.dirname(page_id)
        meta.update({'text': text, 'content': self.render(text), 'category': category, 'slug': os.path.splitext(fname)[0]})
        self.site['pages'].update({ page_id: meta })
        self.site['categories'][category].append(page_id)
        for tag in meta.get('tags', []):
            self.site['tags'][tag].append(page_id)

    def build(self, fname, fpath):
        page = self.site['pages'][os.path.relpath(fpath, self.ROOT_DIR)]
        template = page.get('layout', self.default_template) + '.html'
        templater = self.jinja_env.get_template(template)
        info = self.config.copy()
        info['content'] = page['content']
        info.update(page)
        with open(os.path.splitext(fpath)[0] + '.html', 'w') as fp:
            # TODO: Logging
            fp.write(templater.render(info))

    def _extract(self, fpath):
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

    def main(self):
        self.walk(self.index)
        self.walk(self.build)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('ROOT_DIR', help='Stab this directory')
    opts = parser.parse_args()
    stab = Stab(opts.ROOT_DIR)
    t_start = time.time()
    stab.main()
    print("Site built in \033[43m\033[31m{:0.3f}\033[0m\033[49m seconds. That's quite fast, ain't it?".format(time.time() - t_start))
    print("Built: {} pages.".format(len(stab.site['pages'])))


if __name__ == '__main__':
    cli()
