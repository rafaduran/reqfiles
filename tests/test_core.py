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
    assert len(links) > 0
    mocked.assert_called_once_with(reqfiles[0])
    expected = dict(core.SETUPTOOLS_KEYS)
    expected.update({
        'install_requires': [
            'foo',
            'spam==2.0',
            'bacon>=1.3.1,<2.0',
            'project==1.2.3a4',
            'project-name',
        ],
        'dependency_links': set(links),
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


def test_reqfile_search_and_parse(reqfile):
    '''Test search_and_parse searchs and parses.'''
    with mock.patch.object(reqfile, 'search') as search:
        with mock.patch.object(reqfile, 'parse') as parse:
            found = set(('a', 'b'))
            search.return_value = found
            # check it returns itself
            assert reqfile == reqfile.search_and_parse('root')
        search.assert_called_once_with('root')
        parse.assert_called_once_with(found)
        assert reqfile._reqfiles == found


def test_reqfile_search_and_parse_chaining(reqfile):
    '''Test search_and_parse searchs and parses.'''
    with mock.patch.object(reqfile, 'search') as search:
        with mock.patch.object(reqfile, 'parse') as parse:
            found1 = set(('a', 'b'))
            found2 = set(('c', 'b'))
            search.side_effect = (found1, found2)
            # check it returns itself
            reqfile == reqfile.search_and_parse('root1').search_and_parse('root2')
        assert search.call_count == 2
        assert parse.call_count == 2
        assert reqfile._reqfiles == set(('a', 'b', 'c'))
