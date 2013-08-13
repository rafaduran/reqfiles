'''Python requirement files classifiers.'''
import abc
import re

from . import utils

__all__ = ('classify', 'Classifier', 'RegexClassifierMixin',
           'RequirementsDirectoryClassifier')


class BaseClassifier(object):
    '''
    Given a ``reqfile`` filename it tries to classify it based on setup.py
    requirement keywords: install_requires, tests_require,.... Some examples:

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
    '''
    def get(self, name):
        '''
        Given a name returns the setup keyword and key (only for
        ``extras_require``).
        '''
        if name == 'setup':
            return 'setup_requires', None
        elif name.startswith('test'):
            return 'tests_require', None
        elif name.startswith('require') or name in ('install', 'base'):
            return 'install_requires', None
        else:
            return 'extras_require', name


def check(self, filename):
    '''
    Returns the setup keyword if the given filename matchs this classification
    rule or None.

    Params:
        ``filename``: File name to be classified.

    Returns:
        ``keyword``: setup keyword or ``None``.
    '''


def classify(filename):
    '''
    Given a filename will test all plugins, returning plugin setup keyword on
    first match; ``None`` if there is no match.

    This function is also provided as
    :py:staticmeth:`reqfiles.classifiers.Classifier.classify` static method.
    '''
    for plugin in Classifier.plugins:
        keyword = plugin().check(filename)
        if keyword:
            return keyword


# Metaclass trick to get python2/3 compat. Abstract methods must be defined
# into the mataclass instead of the base classes, so that ABCMeta can do it's
# magic. See http://goo.gl/azOTtq for further information about metaclasses in
# Python 2 and Python 3.
Classifier = utils.PluginMount('Classifier',
                               (BaseClassifier,),
                               {
                                   '__doc__': BaseClassifier.__doc__,
                                   'classify': staticmethod(classify),
                                   'check': abc.abstractmethod(check),
                               })


class RegexClassifierMixin(object):
    regex = None

    def get_regex(self):
        if not self.regex:
            raise ValueError
        return self.regex

    def check(self, filename):
        match = self.get_regex().match(filename)
        if match:
            return self.get(match.groups()[0])


class RequirementsDirectoryClassifier(RegexClassifierMixin, Classifier):
    regex = re.compile(r'.*requirements/(?P<name>\w+).txt')
