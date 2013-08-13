'''Python requirement files core tests.'''
import mock

from reqfiles import core


def test_reqfiles_mapping(reqfile):
    '''Tests Reqfiles mapping implementation.'''
    for key, default in core.SETUPTOOLS_KEYS:
        assert reqfile[key] == default

    assert len(reqfile) == len(core.SETUPTOOLS_KEYS)
    assert sorted(reqfile) == sorted([key for key, default in core.SETUPTOOLS_KEYS])
    assert dict(**reqfile) == dict(core.SETUPTOOLS_KEYS)


def test_reqfiles_search(reqfile):
    '''Tests search returns a set with found filenames.'''
    with mock.patch.object(reqfile, 'finder') as finder:
        finder.return_value = ['foo.txt', 'spam.txt']
        assert set(['foo.txt', 'spam.txt']) == reqfile.search('root')
    finder.assert_called_once_with('root')


def test_reqfiles_parse(reqfile, reqs, links):
    '''Tests parse sources internal data.'''
    reqfiles = ['requirements/base.txt']
    with mock.patch('pip.req.parse_requirements') as mocked:
        mocked.return_value = reqs
        reqfile.parse(reqfiles)
    mocked.assert_called_once_with(reqfiles[0])
    assert 2 == len(reqfile.links)
    assert sorted(links) == sorted(reqfile.links)
