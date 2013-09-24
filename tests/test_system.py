"""Tests for reqfiles.system"""
import mock


def test_python_version_26(pyver):
    """Tests PythonVersion for python2.6"""
    with mock.patch('sys.version_info') as ver_info:
        ver_info.major = 2
        ver_info.minor = 6
        assert pyver.collect() == {'py_version': '26'}


def test_python_version_27(pyver):
    """Tests PythonVersion for python2.7"""
    with mock.patch('sys.version_info') as ver_info:
        ver_info.major = 2
        ver_info.minor = 7
        assert pyver.collect() == {'py_version': '27'}


def test_python_version_33(pyver):
    """Tests PythonVersion for python3.3"""
    with mock.patch('sys.version_info') as ver_info:
        ver_info.major = 3
        ver_info.minor = 3
        assert pyver.collect() == {'py_version': '33'}


@mock.patch('platform.mac_ver')
@mock.patch('platform.dist')
def test_os_faminly_mac(dist, mac_ver, oscollector):
    """Tests OS Family for Mac"""
    dist.return_value = ('', '', '')
    mac_ver.return_value = ('10.8.5', ('', '', ''), 'x86_64')
    assert oscollector.collect()['os_family'] == 'mac'


@mock.patch('platform.dist')
def test_os_faminly_centos(dist, oscollector):
    """Tests OS Family for CentOS"""
    dist.return_value = ('centos', '6.3', 'Final')
    assert oscollector.collect()['os_family'] == 'redhat'


@mock.patch('platform.dist')
def test_os_faminly_ubuntu(dist, oscollector):
    """Tests OS Family for Ubuntu"""
    dist.return_value = ('Ubuntu', '12.04', 'precise')
    assert oscollector.collect()['os_family'] == 'debian'


@mock.patch('platform.mac_ver')
@mock.patch('platform.dist')
def test_os_version_mac(dist, mac_ver, oscollector):
    """Tests OS version for Mac"""
    dist.return_value = ('', '', '')
    mac_ver.return_value = ('10.8.5', ('', '', ''), 'x86_64')
    assert oscollector.collect()['os_version'] == '10.8.5'


@mock.patch('platform.dist')
def test_os_version_centos(dist, oscollector):
    """Tests OS version for CentOS"""
    dist.return_value = ('centos', '6.3', 'Final')
    assert oscollector.collect()['os_version'] == '6.3'


@mock.patch('platform.dist')
def test_os_version_ubuntu(dist, oscollector):
    """Tests OS version for Ubuntu"""
    dist.return_value = ('Ubuntu', '12.04', 'precise')
    assert oscollector.collect()['os_version'] == '12.04'
