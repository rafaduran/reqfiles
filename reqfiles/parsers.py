"""Python requirement files parsers."""
from distutils import version
import logging
from pip import req as pipreq

from . import exceptions as exc

LOG = logging.getLogger(__name__)


class Options(object):
    default_vcs = ''
    skip_requirements_regex = ''


class Parser(object):
    """Provide the requirement files parsing."""
    def parse_file(self, filename, options=None):
        """Parse given file by name.

        Params:
            ``filename``: filename (with path) of the file to being parsed

        Returns:
            ``req_links``: iterable of two-tuple where the first element is the
            string representation of the given requeriment and the second is a
            find link or ``None``.
        """
        if not options:
            options = Options()

        reqs = []
        links = []
        for req in pipreq.parse_requirements(filename, options=options):
            reqstr, link = self.parse(req)
            if link:
                links.append(link)

            reqs.append(reqstr)
        return reqs, links

    def parse(self, req):
        """Parse ``req`` and return requirement string and find link.

        ``req`` is a :py:class:`pip.req.InstallRequirement` and returns
        Params:
            ``req``: :py:class:`pip.req.InstallRequirement` instance

        Returns:
            ``req_link``: two tuple where the first element is the string
            representation of the given requeriment and the second is a find
            link or ``None``.
        """
        if not req.editable:
            if not req.req:
                raise exc.ParserError
            return str(req.req), None

        req_ver = self._get_editable_version(req)
        if req_ver:
            return '{0}=={1}'.format(req.req, req_ver), req.url
        return str(req.req), req.url

    def _get_editable_version(self, req):
        """Parse version for an editable ``req``.

        ``req`` is an instance of :py:class:`pip.req.InstallRequirement` from
        :py:staticmethod:`pip.req.InstallRequirement.from_editable`. Version
        string is parserd based on
        http://pythonhosted.org/setuptools/setuptools.html#dependencies-that-aren-t-in-pypi
        """
        ver_string = req.url.split('-')[-1]
        try:
            req_ver = str(version.StrictVersion(ver_string))
        except ValueError as exc:
            LOG.exception(exc)
            req_ver = None

        return req_ver
