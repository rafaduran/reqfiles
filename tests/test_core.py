'''Python requirement files core tests.'''
from reqfiles import core


def test_reqfiles_mapping(reqfile):
    '''Tests Reqfiles mapping implementation.'''
    for key, default in core.SETUPTOOLS_KEYS:
        assert reqfile[key] == default

    assert len(reqfile) == len(core.SETUPTOOLS_KEYS)
    assert sorted(reqfile) == sorted([key for key, default in core.SETUPTOOLS_KEYS])
    assert dict(**reqfile) == dict(core.SETUPTOOLS_KEYS)
