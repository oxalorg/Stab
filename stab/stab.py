#!/usr/bin/env python3
import os, sys, yaml, mistune, importlib, collections
from jinja2 import Environment, FileSystemLoader

class Plugin:
    def __init__(self, stab):
        """
        The plugin is passed an instance of Stab object
        """
        self.stab = stab


class Render(Plugin):
    def __init__(self, stab):
        super().__init__(stab)

    def to_html(self, content):
        return self.markdown(content)


class Walker(Plugin):
    def __init__(self, stab, func):
        for root, dirs, files in os.walk(stab.ROOT_DIR):
            if is_dir_ignored(root): continue
            for fname in files:
                fpath = absjoin(root, fname)
                if is_allowed(fname) and not is_ignored(fname):
                    func(root, fname, fpath, markdown)


class Builder(Plugin):
    # def __init__(self, root, fname, fpath, markdown):
    def __init__(self, stab, fname, fpath):
        page = stab.site['pages'][os.path.relpath(fpath, stab.ROOT_DIR)]
        template = page.get('layout', default_template) + '.html'
        templater = stab.jinja_env.get_template(template)
        info = stab.config.copy()
        info['content'] = page['content']
        info.update(page)
        with open(absjoin(root, os.path.splitext(fname)[0] + '.html'), 'w') as fp:
            fp.write(templater.render(info))


class Indexer(Plugin):
    def __init__(self, stab, fpath):
        self.stab = stab
        meta, text = self.extract(fpath)
        page_id = os.path.relpath(fpath, self.stab.ROOT_DIR)
        category = os.path.dirname(page_id)
        meta.update({'text': text, 'content': renderer.to_html(text), 'category': category, 'slug': os.path.splitext(fname)[0]})
        site['pages'].update({ page_id: meta })
        site['categories'][category].append(page_id)
        for tag in meta.get('tags', []):
            site['tags'][tag].append(page_id)

    def extract(self, fpath):
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


class Stab:
    is_allowed = lambda x: os.path.splitext(x)[1] in self.ALLOWED
    is_ignored = lambda x: x in self.IGNORED
    is_dir_ignored = lambda x: any(os.path.basename(x).startswith(y) for y in self.DIR_IGNORED)

    absjoin = lambda x, y: os.path.abspath(os.path.join(x, y))

    def __init__(self, ROOT_DIR)
        self.ROOT_DIR = os.path.abspath(ROOT_DIR)
        self.set_defaults()
        self.init_site()
        self.init_jinja()
        self.markdown = mistune.Markdown()

    def set_defaults(self):
        self.config = yaml.load(open(absjoin(self.ROOT_DIR, '_config.yml')).read())
        self.default_template = self.config.get('default_layout')
        self.ALLOWED = {'.md', '.mkd', '.markdown'} + set(config.get('allowed', []))
        self.IGNORED = {'README.md'} + set(config.get('ignored', [])
        # All directories starting with the pattern in DIR_IGNORED is ignored.
        self.DIR_IGNORED = {'_', '.'} + set(config.get('dir_ignored', []))

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
        self.jinja_env.globals = {'site': site}

    def init_plugins(self):
        self.plugins_dir = absjoin(self.ROOT_DIR, '_plugins')
        self.plugins = self.config.get('plugins', [])
        self.active_plugins = {'render': Render, 'walker': Walker, 'indexer': Indexer, 'builder': Builder}
        self.inject_plugin = lambda module, inject, typ: active_plugins.update({typ: getattr(module, inject)})

        sys.path.append(self.plugins_dir)
        for plugin in self.plugins:
            m = importlib.import_module(plugin)
            inject_plugin(module=m, **m.load_plugin())

    def render(self, content):
        return self.markdown(content)

        # for ptype, plugin in self.active_plugins:
        #     if isinstance(plugin, Render):
        #         renderers.append(Render)

    def walk(self, func):
        return Walker(this, func)

    def main():
        self.walk(index)
        self.walk(build)

