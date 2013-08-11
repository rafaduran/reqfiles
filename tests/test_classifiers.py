'''Python requirement files classifiers tests.'''
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
