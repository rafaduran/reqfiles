import mock

from reqfiles import setuptools


def test_setup_keyword(sreqfile, reqstrings, links):
    '''Tests reqfiles setup keyword.'''
    dist = mock.Mock()
    with mock.patch('reqfiles.core.Reqfiles') as mocked:
        mocked.return_value = sreqfile
        setuptools.reqfiles(dist, 'reqfiles', True)
    assert dist.install_requires == reqstrings[:2]
    assert dist.tests_require == reqstrings[3:4]
    assert dist.extras_require == {'ci': reqstrings[4:]}
    assert dist.dependency_links == links
    assert mocked.called_once_with()


def test_setup_keyword_falsy(sreqfile, reqstrings, links):
    '''Tests reqfiles setup keyword for a falsy value.'''
    dist = mock.Mock()
    with mock.patch('reqfiles.core.Reqfiles') as mocked:
        setuptools.reqfiles(dist, 'reqfiles', False)
    assert mocked.called == False
