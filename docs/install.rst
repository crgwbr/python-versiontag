Getting Started
===============

Dependencies
------------

Versiontag does not require any python libraries apart from the standard
library. It does, however, require the ``git`` be installed and executable from
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

    from versiontag import get_version, cache_git_tag

    # This caches for version in version.txt so that it is still accessible if
    # the .git folder disappears, for example, after the slug is built on Heroku.
    cache_git_tag()

    setup_requires = [
        'versiontag>=1.1.0',
    ]

    setup(name='My Package',
          version=get_version(pypi=True),
          setup_requires=setup_requires)
    ...


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
