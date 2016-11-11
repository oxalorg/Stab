from setuptools import setup
from stab import __version__

proj = 'stab'
desc = 'Start blogging with this simple static site generator'
deps = ['pyyaml', 'mistune', 'jinja2']

setup(
    name=proj,
    packages=[proj],
    version=__version__,
    description=desc,
    long_description='Please visit https://github.com/oxalorg/stab for more details.',
    author='oxalorg',
    author_email='rogue@oxal.org',
    url='https://github.com/oxalorg/'+proj,
    download_url='https://github.com/oxalorg/'+proj+'/tarball/' + __version__,
    keywords=['python', 'static', 'site', 'website', 'generator'],
    classifiers=[],
    install_requires=deps,
    entry_points={
        'console_scripts': [
            'stab=stab:cli'
        ],
    })
