---
title: Welcome to Stab
index: False
layout: index
---

Start blogging w/ this Simple static blog generator.

Stab w/ Stab in only **64 lines of code**.

**Check out other branches for advanced plugin features**.
Master branch is currently extremely minimal.

## RIGHT NOW.

***Setup***:

```
# Clone this repo
# This repo is both the blog and the blog generator
git clone https://github.com/oxalorg/Stab
cd Stab

# Create a virtualenv for Python 3
pyvenv venv
# or
# virtualenv venv
source venv/bin/activate

pip3 install pyyaml mistune jinja2 pygments
```

***Write some posts***:

* All your markdown posts go inside `./blog` directory.
* They must have valid ***yaml frontmatter*** as required
  by your templates.
* The one in this repo only required a `title` and `date`
  values.
* Find examples in the `./blog` directory of this repo.

***Build your blog***:

```
python3 stab.py
```

***Deploy it***:

```
rsync -avz --exclude '_*' --exclude '.git*' --exclude 'venv*' --exclude '*.md' `pwd`/ rogue@oxal.org:/var/www/website/public/
```

## TODO

* [ ] Try to reduce dependencies
* [ ] Add support for multiple build directories
* [ ] Add a plugin system
* [ ] Try for main script (w/o plugins) to be pure python

## Contributors

* oxalorg
    - https://oxal.org
    - rogue@oxal.org
