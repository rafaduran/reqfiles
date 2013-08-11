'''Python requirement files helper utils.'''
import glob
import logging
import os

__all__ = ('find_req_files', 'REQ_PATTERNS')

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
