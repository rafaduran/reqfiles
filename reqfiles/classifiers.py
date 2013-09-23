"""Python requirement files classifiers."""
import abc
import re
import os

from . import utils

__all__ = ('classify', 'Classifier', 'RegexClassifierMixin',
           'RequirementsDirectoryClassifier', 'NamesClassifierMixin',
           'RequirementsFilesClassifier', 'Requirements')


class BaseClassifier(object):
    """Given a ``reqfile`` filename it tries to classify it.

    Classification will be done based on setup.py requirement keywords:
    install_requires, tests_require,.... Some examples:

    +------------------------+------------------+-----+
    | reqfile                | setup.py keyword | key |
    +========================+==================+=====+
    | requirements/base.txt  | install_requires |     |
    +------------------------+------------------+-----+
    | requirements.txt       | install_requires |     |
    +------------------------+------------------+-----+
    | requirements/setup.txt | setup_requires   |     |
    +------------------------+------------------+-----+
    | test-requirements/.txt | tests_require    |     |
    +------------------------+------------------+-----+
    | requirements/ci.txt    | extras_require   | ci  |
    +------------------------+------------------+-----+
    | dev-requirements.txt   | extras_require   | dev |
    +------------------------+------------------+-----+
    """

    def get(self, name):
        """Given a name returns the setup keyword and a key.

        Key is only used for ``extras_require`` keyword.
        """
        if name == 'setup':
            return 'setup_requires', None
        elif name.startswith('test'):
            return 'tests_require', None
        elif name.startswith('require') or name in ('install', 'base'):
            return 'install_requires', None
        else:
            return 'extras_require', name


def check(self, filename):
    """Returns the setup keyword if the given filename match criteria or None.

    Criteria is the classification rules that provide all classifiers.

    Params:
        ``filename``: File name to be classified.

    Returns:
        ``keyword``: setup keyword or ``None``.
    """


def classify(filename):
    """Given a filename will test all plugins, returning  first match.

    This function is also provided as
    :py:staticmeth:`reqfiles.classifiers.Classifier.classify` static method.

    Params:
        ``filename``: File name to be classified.

    Returns:
        ``keyword_key``: Two-tuple with first argument as setup.py keyword and
        a key (``extras_require`` only). Returns ``None`` if not match.
    """
    for plugin in Classifier.plugins:
        keyword = plugin().check(filename)
        if keyword:
            return keyword


Classifier = utils.PluginMetaClass('Classifier',
                                   BaseClassifier,
                                   __doc__=BaseClassifier.__doc__,
                                   cassify=staticmethod(classify),
                                   check=abc.abstractmethod(check))


class RegexClassifierMixin(object):
    """Provide regex based classification."""
    regex = None

    def get_regex(self):
        if not self.regex:
            raise ValueError
        return self.regex

    def check(self, filename):
        match = self.get_regex().match(filename)
        if match:
            return self.get(match.groupdict()['name'])


class NamesClassifierMixin(object):
    """Provide list based classification."""
    names = None
    key_keyword = None

    def check(self, filename):
        if not (self.names and self.key_keyword):
            raise ValueError
        if os.path.basename(filename) in self.names:
            return self.key_keyword


class RequirementsDirectoryClassifier(RegexClassifierMixin, Classifier):
    """Match requirements/*.txt"""
    regex = re.compile(r'.*requirements/(?P<name>\w+).txt')


class RequirementsFilesClassifier(RegexClassifierMixin, Classifier):
    """Match *[-_]requirements.txt"""
    regex = re.compile(r'(.*[\\/])?(?P<name>[a-zA-Z]+)[-_]requirements.txt')


class Requirements(NamesClassifierMixin):
    """Match requires.txt, requirements.txt"""
    names = ('requirements.txt', 'requires.txt')
    key_keyword = ('install_requires', None)
