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
def links():
    return [link for req, (reqstring, link) in common.REQ_FIXTURES if link]
