'''Python requirement files classifiers tests.'''
import re

import mock
import pytest

from reqfiles import classifiers

from . import common


@pytest.mark.parametrize(('name', 'key_keyword'), common.KEY_FIXTURES)
def test_keyword_for(classifier, name, key_keyword):
    '''Tests :py:meth:`reqfiles.classifiers.Baseclassifier.keyword_for`.'''
    assert classifier.get(name) == key_keyword


def test_classify():
    expected = ('install_requires', None)
    p1 = mock.Mock(**{'return_value.check.return_value': None})
    p2 = mock.Mock(**{'return_value.check.return_value': expected})
    with mock.patch.object(classifiers, 'Classifier') as mocked:
        mocked.plugins = iter([p1, p2])
        assert expected == classifiers.classify('name')
    p1.assert_called_once_with()
    p1.check.asert_called_once_with('name')
    p2.assert_called_once_with()
    p2.check.asert_called_once_with('name')


class FooClassifier(classifiers.RegexClassifierMixin, object):
    regex = re.compile(r'requirements/(?P<name>foo).txt')

    def get(self, name):
        return 'install_requires', None


class TestsRegexClassifierMixin(object):
    def setup_method(self, name):
        self.classifier = FooClassifier()

    def test_check_match(self):
        '''Tests FooClassifier match.'''
        assert ('install_requires', None) == self.classifier.check('requirements/foo.txt')

    def test_check_no_match(self):
        assert None == self.classifier.check('requirements/spam.txt')

    def test_no_regex_raises(self):
        self.classifier.regex = None
        with pytest.raises(ValueError):
            self.classifier.check('something')


class TestNamesClassifierMixin(object):
    def setup_method(self, name):
        self.classifier = classifiers.Requirements()

    def test_check_match(self):
        """Tests FooClassifier match."""
        assert ('install_requires', None) == self.classifier.check('requirements.txt')
        assert ('install_requires', None) == self.classifier.check('requires.txt')
        assert ('install_requires', None) == self.classifier.check('directory/requires.txt')

    def test_check_no_match(self):
        assert None == self.classifier.check('requirementss.txt')

    def test_no_names_raises(self):
        self.classifier.names = None
        with pytest.raises(ValueError):
            self.classifier.check('something')

    def test_no_key_keyword_raises(self):
        self.classifier.key_keyword = None
        with pytest.raises(ValueError):
            self.classifier.check('something')


@pytest.mark.parametrize(
    ('filename', 'key_keyword'),
    (('directory/tests_requirements.txt', ('tests_require', None)),
     ('ci-requirements.txt', ('extras_require', 'ci')),
     ('directory\dev-requirements.txt', ('extras_require', 'dev')),)
)
def test_requirements_files_classifier(rfc_classifier, filename, key_keyword):
    """Tests RequirementsFilesClassifier classifier."""
    assert rfc_classifier.check(filename) == key_keyword
