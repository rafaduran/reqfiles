'''pytest conftest moduele'''
import pytest


@pytest.fixture
def reqfile():
    from reqfiles import core
    return core.Reqfiles(eager=False)


@pytest.fixture
def parser():
    from reqfiles import core
    return core.Parser()
