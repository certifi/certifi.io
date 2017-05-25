# -*- coding: utf-8 -*-
from __future__ import absolute_import, division

from twisted.application import service, strports
from twisted.python import usage
from twisted.web import vhost
from twisted.web.client import HTTPConnectionPool
from twisted.web.server import Site

from .static_proxy_site import (
    RProxyResource, RedirectResource
)


__all__ = ['makeService']


HTTPS_PORT = '443'
HTTP_PORT = '80'


# The rProxy hosts configuration.
hosts = {
    "certifi.io": {
        "port": 443,
        "host": "certifiio.readthedocs.io",
        "scheme": "https",
    },
}

customHeaders = [
    (
        b'Strict-Transport-Security',
        [b'max-age=31536000; includeSubDomains; preload'],
    ),
    (
        b'X-Clacks-Overhead',
        [b'GNU Terry Pratchett'],
    )
]


class Options(usage.Options):
    optParameters = []


def makeService(config):
    """
    Create the service serving the mkcert data.
    """
    from twisted.internet import reactor

    # We need a HTTP connection pool for rproxy.
    pool = HTTPConnectionPool(reactor)

    proxyResource = RProxyResource(
        hosts=hosts,
        pool=pool,
        customHeaders=customHeaders,
        reactor=reactor
    )
    redirectResource = RedirectResource()

    secureSite = Site(proxyResource)
    insecureSite = Site(redirectResource)

    multiService = service.MultiService()
    multiService.addService(
        strports.service('le:/certs:tcp:' + HTTPS_PORT, secureSite)
    )
    multiService.addService(
        strports.service("tcp:" + HTTP_PORT, insecureSite)
    )
    return multiService
