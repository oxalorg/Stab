#!/usr/bin/sh
proj='stab'
python3 setup.py sdist bdist_wheel &&\
twine upload dist/$proj-$1* &&\
mkdir dist/$1 &&\
mv dist/$proj-$1* dist/$1 || "Failed"
