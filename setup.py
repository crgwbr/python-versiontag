#!/usr/bin/env python
import codecs
import os.path
from distutils.core import setup
from versiontag import get_version, cache_git_tag

packages = [
    'versiontag',
]

def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)

def read(fname):
    return codecs.open(fpath(fname), encoding='utf-8').read()

cache_git_tag()

setup(
    name='versiontag',
    version=get_version(pypi=True),
    description='Simple git tag based version numbers',
    long_description=read(fpath('README.rst')),
    author='Craig Weber',
    author_email='crgwbr@gmail.com',
    url='https://github.com/crgwbr/python-versiontag',
    packages=packages,
    license='LICENSE.md'
)
