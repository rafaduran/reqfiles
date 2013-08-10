'''Python requirement files core.'''
import collections

import six

from . import utils

__all__ = ('Reqfiles', 'SETUPTOOLS_KEYS')

SETUPTOOLS_KEYS = (
    ('install_requires', []),
    ('tests_require', []),
    ('setup_requires', []),
    ('extra_require', {}),
)


class Reqfiles(collections.Mapping):
    '''
    :py:class:`reqfiles.core.Reqfiles` looks for requirements files, parses
    them and provides requirements definitions in a setup.py friendly way.
    '''
    def __init__(self, root=None, finder=utils.find_req_files, eager=True):
        '''Look up for reqfiles and parses them.

        Params:
            ``root``: Directory where search reqfiles.
            ``finder``: Callable who actually does the the search.
        '''
        self._data = dict(SETUPTOOLS_KEYS)
        self._reqfiles = set()
        self.finder = finder
        if eager:
            self.search_and_parse(root)

    def parse(self, reqfiles):
        '''
        Parse reqfiles and sources internal data with requirements found.
        '''

    def search(self, root):
        '''Search for requirement files.'''
        return set(self.finder(root))

    def search_and_parse(self, root):
        '''
        This method is where all starts, thought all the heavy work is done by
        :py:meth:`search` and :py:meth:`parse`.
        '''
        self._reqfiles |= self.search(root)
        self.parse(self._reqfiles)
        return self

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return six.iterkeys(self._data)
