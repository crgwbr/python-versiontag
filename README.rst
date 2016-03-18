python-versiontag
=============================

.. image:: https://img.shields.io/pypi/v/versiontag.svg
    :target: https://pypi.python.org/pypi/versiontag

.. image:: https://img.shields.io/pypi/dm/versiontag.svg
        :target: https://pypi.python.org/pypi/versiontag

.. image:: https://travis-ci.org/crgwbr/python-versiontag.svg
    :target: https://travis-ci.org/crgwbr/python-versiontag

What?
-----

This is an ultra-simple library design to make accessing the current version number of
your software easy.

Why?
----

Version numbers are all too often duplicated among setup.py, git tags, and others sources
of truth. This library makes it possible to consolidate on git tags as a single source of
truth regarding version numbers.

How?
----

Install python-versiontag using pip.

.. code:: bash

    pip install versiontag

Add version.txt to your .gitignore file.

.. code:: bash

    echo "version.txt" >> .gitignore

Add versiontag to your package's setup.py file.

.. code:: python

    from versiontag import get_version, cache_git_tag

    # This caches for version in version.txt so that it is still accessible if
    # the .git folder disappears, for example, after the slug is built on Heroku.
    cache_git_tag()

    setup(name='My Package',
          version=get_version(pypi=True),
    ...


Use versiontag where ever you want to access the version number.

.. code:: python

    >>> from versiontag import get_version
    >>> print( get_version() )
    'r1.2.3'
