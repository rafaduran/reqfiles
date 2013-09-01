'''Python requirement parsers tests.'''
from pip import req
import pytest

from reqfiles import exceptions as exc

from . import common


@pytest.mark.parametrize(('req', 'expected'), common.REQ_FIXTURES)
def test_parser_parse(parser, req, expected):
    '''Tests Parser parsing.'''
    assert parser.parse(req) == expected


def test_parser_error(parser):
    """Tests parser sad path."""
    require = req.InstallRequirement.from_line('https://host/url')
    with pytest.raises(exc.ParserError):
        parser.parse(require)
