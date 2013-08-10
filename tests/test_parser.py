'''Python requirement parsers tests.'''
import pytest

from . import common


@pytest.mark.parametrize(('req', 'expected'), common.REQ_FIXTURES)
def test_parser_parse(parser, req, expected):
    '''Tests Parser parsing.'''
    assert parser.parse(req) == expected
