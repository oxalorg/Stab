#!/usr/bin/sh
proj='dystic'
python3 setup.py sdist bdist_wheel &&\
twine upload dist/* &&\
mkdir dist/$1 &&\
mv dist/$proj-$1* dist/$1 || "Failed"
