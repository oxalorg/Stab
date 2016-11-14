"""
Watches for incremental changes and previously stored caches.
"""
import os, json, logging

absjoin = lambda x, y: os.path.abspath(os.path.join(x, y))


class Watchman():
    def __init__(self, ROOT_DIR, INCREMENTAL, default_template):
        logging.info("Watchman awakened.")
        self.ROOT_DIR = ROOT_DIR
        self.default_template = default_template
        self.inc_layout = INCREMENTAL
        open(absjoin(self.ROOT_DIR, '_mtime.cache'), 'a+').close()
        try:
            with open(absjoin(self.ROOT_DIR, '_mtime.cache'), 'r') as fp:
                self.prev_mtime = json.load(fp)
        except ValueError:
            self.prev_mtime = {}
        logging.info("Read mtime stored during the previous build.")


    def should_build(self, fpath, meta):
        """
        Checks if the file should be built or not
        Only skips layouts which are tagged as INCREMENTAL
        Rebuilds only those files with mtime changed since previous build
        """
        if meta.get('layout', self.default_template) in self.inc_layout:
            if self.prev_mtime.get(fpath, 0) == os.path.getmtime(fpath):
                return False
            else:
                return True
        return True


    def sleep(self, mtimes):
        with open(absjoin(self.ROOT_DIR, '_mtime.cache'), 'w') as fp:
            json.dump(mtimes, fp)
        logging.info("Wrote current mtime into $site_baseurl/_mtime.cache")
