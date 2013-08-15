'''pytest conftest moduele'''
import pytest

from . import common


@pytest.fixture
def reqfile():
    from reqfiles import core
    return core.Reqfiles(eager=False)


@pytest.fixture
def parser():
    from reqfiles import core
    return core.Parser()


@pytest.fixture
def classifier():
    from reqfiles import classifiers
    return classifiers.BaseClassifier()


@pytest.fixture
def reqs():
    return [req for req, _ in common.REQ_FIXTURES]


@pytest.fixture
def reqstrings():
    return [rstring for _ , (rstring, _) in common.REQ_FIXTURES]


@pytest.fixture
def links():
    return [link for req, (reqstring, link) in common.REQ_FIXTURES if link]


@pytest.fixture
def sreqfile(reqfile, reqstrings, links):
    reqfile._data['install_requires'] = reqstrings[:2]
    reqfile._data['tests_require'] = reqstrings[3:4]
    reqfile._data['extras_require']['ci'] = reqstrings[4:]
    reqfile._data['dependency_links'] = links
    return reqfile
