import os
import subprocess
import re


__default_version__ = 'r0.0.0'


def __get_git_tag():
    with open(os.devnull, 'wb') as devnull:
        version = subprocess.check_output(['git', 'describe', '--tags'], stderr=devnull)
        version = version.rstrip()
    if hasattr(version, 'decode'):
        version = version.decode('utf-8')
    return version


def __get_cache_file():
    return os.path.join(os.getcwd(), 'version.txt')


def cache_git_tag():
    try:
        version = __get_git_tag()
    except:
        version = __default_version__
    with open(__get_cache_file(), 'w') as vf:
        vf.write(version)
    return version


def get_version(pypi=False):
    version = __default_version__

    try:
        with open(__get_cache_file(), 'r') as vf:
            version = vf.read().strip()
    except:
        pass

    try:
        version = __get_git_tag()
    except:
        pass

    if pypi:
        # Convert to pypi valid version:
        # 1. Drop the r prefix we use on git tags: r1.0.1-12-geaea7b6 => 1.0.1-12-geaea7b6
        # 2. Drop the commit hash from the end:    1.0.1-12-geaea7b6 => 1.0.1-12
        v = re.search('^[r,v]{0,1}(([0-9\.]+)(\-[0-9]+)?)(\-.+)?$', version)
        version = v.group(1) if v else __default_version__
    return version
