'''Some common stuff to be used for all tests.'''
from pip import req

REQFILES_FIXTURES = (
    ('/full/path/', ['base.txt', 'tests.txt']),
    ('relative/path/', ['setup.txt', 'install.txt', 'ci.txt']),
    (None, ['base.txt', 'tests.txt']),
)

REQ_FIXTURES = [(req.InstallRequirement.from_line(req_str), (req_str, None))
                for req_str in ('foo',
                                'spam==2.0',
                                'bacon>=1.3.1,<2.0',
                                )]
REQ_FIXTURES.extend((
    (req.InstallRequirement.from_editable('git+proto://host/path@revision#egg=project-1.2.3a4'),
     ('project==1.2.3a4', 'git+proto://host/path@revision#egg=project-1.2.3a4')),
    (req.InstallRequirement.from_editable('hg+proto://host/path#egg=project-name'),
     ('project-name', 'hg+proto://host/path#egg=project-name')),
))


KEY_FIXTURES = (
    # install requires keywords
    ('base', ('install_requires', None)),
    ('install', ('install_requires', None)),
    ('requirements', ('install_requires', None)),
    ('requires', ('install_requires', None)),
    # setup requires keywords
    ('setup', ('setup_requires', None)),
    # tests require keywords
    ('test', ('tests_require', None)),
    ('tests', ('tests_require', None)),
    # some extra examples
    ('ci', ('extras_require', 'ci')),
    ('dev', ('extras_require', 'dev')),
)
