__all__ = ('set_options', 'add_options', 'get_options',
           'set_classpath', 'add_classpath', 'get_classpath',
           'expand_classpath')

import platform
if platform.system() == 'Windows':
    split_char = ';'
else:
    split_char = ':'

vm_running = False
options = []
classpath = None

def set_options(*opts):
    "Sets the list of options to the JVM. Removes any previously set options."
    if vm_running:
        raise ValueError("VM is already running, can't set options")
    globals()['options'] = opts

def add_options(*opts):
    "Appends options to the list of VM options."
    if vm_running:
        raise ValueError("VM is already running, can't set options")
    global options
    options.extend(opts)

def get_options():
    "Retrieves the current list of VM options."
    global options
    return list(options)


def set_classpath(*path):
    """
    Sets the classpath for the JVM to use. Replaces any existing classpath, overriding the CLASSPATH environment variable.
    """
    if vm_running:
        raise ValueError("VM is already running, can't set classpath")
    global classpath
    classpath = path

def add_classpath(*path):
    """
    Appends items to the classpath for the JVM to use.
    Replaces any existing classpath, overriding the CLASSPATH environment variable.
    """
    if vm_running:
        raise ValueError("VM is already running, can't set classpath")
    global classpath
    if classpath is None:
        classpath = list(path)
    else:
        classpath.extend(path)

def get_classpath():
    "Retrieves the classpath the JVM will use."
    from os import environ
    from os.path import realpath
    global classpath

    if classpath is not None:
        return list(classpath)

    if 'CLASSPATH' in environ:
        return environ['CLASSPATH'].split(split_char)

    return [realpath('.')]

def expand_classpath(classpath):
    from glob import glob
    paths = []
    # deal with wildcards
    for path in classpath:
        if not path.endswith('*'):
            paths.append(path)
        else:
            paths.extend(glob(path + '.[Jj][Aa][Rr]'))
    return split_char.join(paths)
