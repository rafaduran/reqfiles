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
    expected = dict(core.SETUPTOOLS_KEYS)
    expected.update({
        'install_requires': [
            'foo',
            'spam==2.0',
            'bacon>=1.3.1,<2.0',
            'project==1.2.3a4',
            'project-name',
        ],
    })
    assert dict(reqfile) == expected


def test_reqfiles_parse_extras(reqfile, reqs, links):
    '''Tests parse sources internal data.'''
    reqfiles = ['requirements/ci.txt']
    with mock.patch('pip.req.parse_requirements') as mocked:
        mocked.return_value = reqs
        reqfile.parse(reqfiles)
    expected = dict(core.SETUPTOOLS_KEYS)
    expected.update({
        'extras_require': {
            'ci': [
                'foo',
                'spam==2.0',
                'bacon>=1.3.1,<2.0',
                'project==1.2.3a4',
                'project-name',
            ],
        },
    })
    assert dict(reqfile) == expected


def test_reqfile_eager():
    '''Test eager search and parsing.'''
    with mock.patch('reqfiles.core.Reqfiles.search_and_parse') as mocked:
        core.Reqfiles('root')
    mocked.assert_called_once_with('root')
