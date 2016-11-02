import os
import subprocess
import re
import logging


__default_version__ = 'r0.0.0'
logger = logging.getLogger(__name__)


def __get_git_tag():
    """
    Read the Git project version by running ``git describe --tags`` in the current-working-directory.

    :return: Project version string
    """
    with open(os.devnull, 'wb') as devnull:
        version = subprocess.check_output(['git', 'describe', '--tags'], stderr=devnull)
        version = version.rstrip()
    if hasattr(version, 'decode'):
        version = version.decode('utf-8')
    return version


def __get_cache_file():
    """
    Get the path to the version cache file.

    :return: File path string
    """
    return os.path.join(os.getcwd(), 'version.txt')


def __open_cache_file(mode):
    """
    Open the version cache file in the given mode and return the file object.

    :param mode: Mode to open file. See `Python file modes <https://docs.python.org/3/library/functions.html#open>`_.
    :return: File object
    """
    return open(__get_cache_file(), mode)


def cache_git_tag():
    """
    Try to read the current version from git and, if read successfully, cache it into the version cache file. If
    the git folder doesn't exist or if git isn't installed, this is a no-op. I.E. it won't blank out a
    pre-existing version cache file upon failure.

    :return: Project version string
    """
    try:
        version = __get_git_tag()
        with __open_cache_file('w') as vf:
            vf.write(version)
    except:
        version = __default_version__
    return version


def convert_to_pypi_version(version):
    """
    Convert a git tag version string into something compatible with `PEP-440 <https://www.python.org/dev/peps/pep-0440/>`_.

    :param version: The input version string, normally directly out of git describe.
    :return: PEP-440 version string

    Usage::

      >>> convert_to_pypi_version('r1.0.1')  # Normal Releases
      1.0.1
      >>> convert_to_pypi_version('r1.0.1-dev1')  # Dev Releases
      1.0.1.dev1
      >>> convert_to_pypi_version('r1.0.1-a1')  # Alpha Releases
      1.0.1a1
      >>> convert_to_pypi_version('r1.0.1-b4')  # Beta Releases
      1.0.1b4
      >>> convert_to_pypi_version('r1.0.1-rc2')  # RC Releases
      1.0.1rc2
      >>> convert_to_pypi_version('r1.0.1-12-geaea7b6')  # Post Releases
      1.0.1.post12
    """
    v = re.search('^[r,v]{0,1}(?P<final>[0-9\.]+)(\-(?P<pre>(a|b|rc)[0-9]+))?(\-(?P<dev>dev[0-9]+))?(\-(?P<post>[0-9]+))?(\-.+)?$', version)
    if not v:
        return __default_version__

    # https://www.python.org/dev/peps/pep-0440/#final-releases
    version = v.group('final')

    # https://www.python.org/dev/peps/pep-0440/#pre-releases
    if v.group('pre'):
        version += v.group('pre')

    # https://www.python.org/dev/peps/pep-0440/#developmental-releases
    if v.group('dev'):
        version += '.%s' % v.group('dev')

    # https://www.python.org/dev/peps/pep-0440/#post-releases
    if v.group('post'):
        version += '.post%s' % v.group('post')

    return version


def get_version(pypi=False):
    """
    Get the project version string.

    Returns the most-accurate-possible version string for the current project.
    This order of preference this is:

    1. The actual output of ``git describe --tags``
    2. The contents of the version cache file
    3. The default version, ``r0.0.0``

    :param pypi: Default False. When True, returns a PEP-440 compatible version string.
    :return: Project version string
    """
    version = __default_version__

    try:
        with __open_cache_file('r') as vf:
            version = vf.read().strip()
    except:
        pass

    try:
        version = __get_git_tag()
    except:
        pass

    if pypi:
        version = convert_to_pypi_version(version)

    if version == __default_version__:
        logger.warning("versiontag could not determine package version using cwd %s. Returning default: %s" % (os.getcwd(), __default_version__))

    return version
