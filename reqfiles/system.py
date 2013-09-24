"""Provide information about current system."""
import abc
import platform
import sys

from . import utils

__all__ = ('Collector',)


class BaseCollector(object):
    """Collect information about the current host."""


def collect(self):
    """Collect current plugin information and return it as a dict."""


def collect_all(data=None):
    """Collect all plugin information and return it as a dict.

    This method is provided also as
    :py:classmethod:`reqfiles.system.Collect.collect_all."""
    if not data:
        data = {}

    for plugin in Collector.plugins:
        plugin().collect(data)

    return data


Collector = utils.PluginMetaClass('Collector',
                                  BaseCollector,
                                  __doc__=BaseCollector.__doc__,
                                  collect_all=staticmethod(collect_all),
                                  collect=abc.abstractmethod(collect))


class PythonVersion(Collector):
    """Collects information about the Python version."""
    def collect(self, data):
        data['py_version'] = '{ver.major}{ver.minor}'.format(ver=sys.version_info)
        return data


class OS(Collector):
    """Collects information about the OS"""
    os_to_family = {
        'centos': 'redhat',
        'redhat': 'redhat',
        'ubuntu': 'debian',
        'debian': 'debian',
    }

    def collect(self, data):
        dist = platform.dist()
        mac_ver = platform.mac_ver()
        if dist[0]:
            data['os_family'] = self.os_to_family.get(dist[0].lower(), None)
            data['os_version'] = dist[1]
        elif mac_ver[0]:
            data['os_family'] = 'mac'
            data['os_version'] = mac_ver[0]

        return data
