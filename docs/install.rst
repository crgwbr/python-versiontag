Getting Started
===============

Dependencies
------------

Versiontag does not require any python libraries apart from the standard
library. It does, however, require `git <https://git-scm.com/>`_ be installed and executable from
the system path.


Installation
------------

Install python-versiontag using pip.

.. code:: bash

    pip install versiontag

Add version.txt to your .gitignore file. This file is used by versiontag to
cache the current version, in case the ``.git`` folder disappears at some point.
Because it is just a cache, you should not check it into VCS.

.. code:: bash

    echo "version.txt" >> .gitignore

Add versiontag to your package's setup.py file.

.. code:: python

    from setuptools import setup, Distribution

    # Make sure versiontag exists before going any further. This won't actually install
    # the package. It will just download the egg file into `.eggs` so that it can be used
    # henceforth in setup.py.
    Distribution().fetch_build_eggs('versiontag')

    # Import versiontag components
    from versiontag import get_version, cache_git_tag

    # This caches for version in version.txt so that it is still accessible if
    # the .git folder disappears, for example, after the slug is built on Heroku.
    cache_git_tag()

    # If you want to use versiontag anywhere outside of the setup.py script, you should
    # also add it to `install_requires`. This makes sure to actually install it, instead of
    # just downloading the egg.
    install_requires = [
        …
        'versiontag>=1.1.1',
        …
    ]

    # Do all your normal setup.py stuff.
    setup(name='my-awesome-package',
          version=get_version(pypi=True))
    …


Usage
-----

Now setup.py knows about your current version.

.. code:: bash

    $ git tag r1.2.3
    $ python setup.py --version
    r1.2.3


You can also use versiontag where ever you want to access the version number
from inside your project.

.. code:: python

    >>> from versiontag import get_version
    >>> print( get_version() )
    'r1.2.3'
    >>> print( get_version(pypi=True) )
    '1.2.3'
