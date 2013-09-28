'''pytest conftest moduele'''
import os

import pytest

from . import common

ROOT = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def reqfile():
    from reqfiles import core
    return core.Reqfiles(eager=False)


@pytest.fixture
def parser():
    from reqfiles import parsers
    return parsers.Parser()


@pytest.fixture
def classifier():
    from reqfiles import classifiers
    return classifiers.BaseClassifier()


@pytest.fixture
def reqs():
    return [req for req, _ in common.REQ_FIXTURES]


@pytest.fixture
def reqstrings():
    return [rstring for _, (rstring, _) in common.REQ_FIXTURES]


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


@pytest.fixture
def rfc_classifier():
    from reqfiles import classifiers
    return classifiers.RequirementsFilesClassifier()


@pytest.fixture
def pyver():
    from reqfiles import system
    return system.PythonVersion()


@pytest.fixture
def oscollector():
    from reqfiles import system
    return system.OS()


@pytest.fixture
def pythonfilter():
    from reqfiles import filters
    return filters.PythonVersionFilter()


@pytest.fixture
def filename_firstline():
    return (os.path.join(ROOT, 'fixtures/requirements.txt'),
            "# reqfiles: py_version>'26', os_family==centos\n")
