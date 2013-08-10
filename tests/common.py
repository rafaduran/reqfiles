'''Some common stuff to be used for all tests.'''
REQ_FIXTURES = (
    ('/full/path/', ['base.txt', 'tests.txt']),
    ('relative/path/', ['setup.txt', 'install.txt', 'ci.txt']),
    (None, ['base.txt', 'tests.txt']),
)
