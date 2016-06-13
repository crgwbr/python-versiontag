import os
import subprocess
import re
import logging


__default_version__ = 'r0.0.0'
logger = logging.getLogger(__name__)


def __get_git_tag():
    with open(os.devnull, 'wb') as devnull:
        version = subprocess.check_output(['git', 'describe', '--tags'], stderr=devnull)
        version = version.rstrip()
    if hasattr(version, 'decode'):
        version = version.decode('utf-8')
    return version


def __get_cache_file():
    return os.path.join(os.getcwd(), 'version.txt')


def __open_cache_file(mode):
    return open(__get_cache_file(), mode)


def cache_git_tag():
    try:
        version = __get_git_tag()
        with __open_cache_file('w') as vf:
            vf.write(version)
    except:
        version = __default_version__
    return version


def convert_to_pypi_version(version):
    # See https://www.python.org/dev/peps/pep-0440/
    # Convert to pypi valid version:
    #   * Normal Releases:   r1.0.1 => 1.0.1
    #   * Dev Releases:      r1.0.1-dev1 => 1.0.1.dev1
    #   * Alpha Releases:    r1.0.1-a1 => 1.0.1a1
    #   * Beta Releases:     r1.0.1-b4 => 1.0.1b4
    #   * RC Releases:       r1.0.1-rc2 => 1.0.1rc2
    #   * Post Releases:     r1.0.1-12-geaea7b6 => 1.0.1.post12
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
