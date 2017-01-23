#!/usr/bin/env python
import codecs
import os.path
from setuptools import setup, find_packages
from versiontag import get_version, cache_git_tag


packages = find_packages()


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return codecs.open(fpath(fname), encoding='utf-8').read()


cache_git_tag()

setup(
    name='versiontag',
    description='Simple git tag based version numbers',
    version=get_version(pypi=True),
    long_description=read(fpath('README.rst')),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    author='Craig Weber',
    author_email='crgwbr@gmail.com',
    url='https://github.com/thelabnyc/python-versiontag',
    packages=packages,
    license='ISC'
)
