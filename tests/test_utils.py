'''Python requirement files helper utils tests.'''
import abc
import os

import mock
import pytest

from reqfiles import utils

from . import common


@pytest.mark.parametrize(('root', 'files'), common.REQFILES_FIXTURES)
def test_find_req_dir(root, files):
    '''Tests :py:func:`find_req_dir`.'''
    if root is None:
        basedir = os.path.abspath(os.path.curdir)
    else:
        basedir = root
    targets = [os.path.join(basedir, pattern) for pattern in utils.REQ_PATTERNS]

    # Test it returns what we expect when both patterns find something
    with mock.patch('glob.glob', side_effect=(files[:1], files[1:], [])) as mocked:
        assert files == utils.find_req_files(root)
    assert mocked.call_args_list == [mock.call(target) for target in targets]

    # Test it returns what we expect when just one pattern finds something
    with mock.patch('glob.glob', side_effect=(files, [], [])) as mocked:
        assert files == utils.find_req_files(root)
    assert mocked.call_args_list == [mock.call(target) for target in targets]

    # Test it returns empty list if not reqfile is found
    with mock.patch('glob.glob', side_effect=([], [], [])) as mocked:
        assert [] == utils.find_req_files(root)
    assert mocked.call_args_list == [mock.call(target) for target in targets]


Meta = utils.PluginMount('Meta', (object,), {'test': abc.abstractmethod(lambda x: x)})


def test_plugin_mount():
    '''Tests PluginMount metaclass'''
    assert 0 == len(Meta.plugins)

    with pytest.raises(TypeError):
        class A(Meta): pass
        A()
    assert 1 == len(Meta.plugins)

    class B(Meta):
        def test(self, value):
            return value
    assert 2 == len(Meta.plugins)
    assert B().test(1) == 1
