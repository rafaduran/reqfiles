'''Python requirement files helper utils.'''
import abc
import glob
import logging
import os

__all__ = ('find_req_files', 'PluginMount', 'REQ_PATTERNS')

LOG = logging.getLogger(__name__)
REQ_PATTERNS = ('require*/*.txt', 'require*.txt', '*require*.txt')


def find_req_files(root=None):
    '''
    Find the requirement directory relative to the given root.

    Params:
        ``root``: root directory where look for requirements files. Current
        directory will be used as default if no root is given.

    Returns:
        ``reqfiles``: requirement files found or empty list.
    '''
    if root is None:
        # Suppose we are on setup.py and reqfiles are in the same directory
        root = os.path.abspath(os.path.curdir)

    files = []
    for pattern in REQ_PATTERNS:
        target = os.path.join(root, pattern)
        LOG.debug('Checking: "{0}" pattern'.format(target))
        files.extend(glob.glob(target))
    return files


class PluginMount(abc.ABCMeta):
    '''
    Meta class providing a pluggable interface inspired by Marty Alchin`s
    `A Simple Plugin Framework`_

    .. _A Simple Plugin Framework: http://martyalchin.com/2008/jan/10/simple-plugin-framework/
    '''
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)
