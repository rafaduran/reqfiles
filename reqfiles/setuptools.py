'''Python requirement files setuptools integration.'''
from . import core


def reqfiles(dist, attr, value):
    '''Implements reqfiles setup() keyword.'''
    if not value:
        return

    reqfiles = core.Reqfiles()
    for keyword, _ in core.SETUPTOOLS_KEYS:
        setattr(dist, keyword, reqfiles[keyword])
