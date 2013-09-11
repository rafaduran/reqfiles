"""Python requirement files core."""
import collections

from . import parsers
from . import classifiers
from . import utils

__all__ = ('Parser', 'Reqfiles', 'SETUPTOOLS_KEYS')

SETUPTOOLS_KEYS = (
    ('install_requires', []),
    ('tests_require', []),
    ('setup_requires', []),
    ('extras_require', collections.defaultdict(list)),
    ('dependency_links', set()),
)


class Reqfiles(collections.Mapping):
    """Provide requirements files integration for setuptools.

    :py:class:`reqfiles.core.Reqfiles` looks for requirements files, parses
    them and provides requirements definitions in a setup.py friendly way.
    """
    def __init__(self, root=None,
                 finder=utils.find_req_files,
                 parser=parsers.Parser,
                 classifier=classifiers.classify,
                 eager=True):
        """Look up for reqfiles and parses them.

        Params:
            ``root``: Directory where search reqfiles.

            ``finder``: Callable who actually does the the search.
        """
        self._data = dict(SETUPTOOLS_KEYS)
        self._reqfiles = set()
        self.finder = finder
        self.parser = parser()
        self.classifier = classifier
        if eager:
            self.search_and_parse(root)

    def parse(self, reqfiles):
        """Parse reqfiles and sources internal data with requirements found."""
        for filename in reqfiles:
            # classify
            keyword, key = self.classifier(filename)
            reqstrs, links = self.parser.parse_file(filename)
            [self._data['dependency_links'].add(link) for link in links]
            # update self._data
            if keyword == 'extras_require':
                self._data['extras_require'][key].extend(reqstrs)
            else:
                self._data[keyword].extend(reqstrs)

    def search(self, root):
        """Search for requirement files."""
        return set(self.finder(root))

    def search_and_parse(self, root):
        """Search and parse reqfiles.

        This method is where all starts, thought all the heavy work is done by
        :py:meth:`search` and :py:meth:`parse`.
        """
        found = self.search(root)
        self.parse(found - self._reqfiles)
        self._reqfiles |= found
        return self

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)
