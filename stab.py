#!/usr/bin/env python3
import os
import sys
import markdown
import yaml

absjoin = lambda x, y: os.path.abspath(os.path.join(x, y))
ROOT_DIR = os.getcwd()
OUTPUT_DIR = absjoin(ROOT_DIR, '_site')
config = yaml.load(open(absjoin(ROOT_DIR, '_config.yml')).read())
blog_dir = absjoin(ROOT_DIR, config.get('blog_dir', 'blog'))

def extract_meta(fpath):
    meta = []
    first_line = True
    with open(fpath) as fp:
        for line in fp:
            if line.strip() == '---' :
                if not first_line:
                    return yaml.load(''.join(meta))
                first_line = False
            meta.append(line)
        raise SystemExit('File with invalid yaml meta block: ' + fpath)
