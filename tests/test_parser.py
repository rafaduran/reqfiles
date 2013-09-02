'''Python requirement parsers tests.'''
import mock
from pip import req as pipreq
import pytest

from reqfiles import exceptions as exc

from . import common


@pytest.mark.parametrize(('req', 'expected'), common.REQ_FIXTURES)
def test_parser_parse(parser, req, expected):
    '''Tests Parser parsing.'''
    assert parser.parse(req) == expected


def test_parser_error(parser):
    """Tests parser sad path."""
    require = pipreq.InstallRequirement.from_line('https://host/url')
    with pytest.raises(exc.ParserError):
        parser.parse(require)


def test_parse_filename(parser):
    """Test parser filename parsing."""
    requires = []
    links = []
    requirements = []
    for req, (reqstring, link) in common.REQ_FIXTURES:
        requires.append(reqstring)
        if link:
            links.append(link)
        requirements.append(req)

    with mock.patch.object(pipreq, 'parse_requirements') as pip:
        pip.return_value = requirements
        reqs_result, links_result = parser.parse_file('requirements.txt')
    pip.assert_called_once_with('requirements.txt')
    assert sorted(reqs_result) == sorted(requires)
    assert sorted(links_result) == sorted(links)
