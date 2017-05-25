# -*- coding: utf-8 -*-
from __future__ import division, absolute_import

from six.moves.urllib.parse import urlparse

from twisted.internet.defer import Deferred, succeed
from twisted.internet.protocol import Protocol
from twisted.python.urlpath import URLPath
from twisted.web import server
from twisted.web.client import Agent
from twisted.web.http import MOVED_PERMANENTLY
from twisted.web.iweb import IBodyProducer
from twisted.web.resource import Resource
from twisted.web.static import File

from zope.interface import implementer


TRANSPORT_HEADERS = (
    b'content-length', b'connection', b'keep-alive', b'te', b'trailers',
    b'transfer-encoding', b'upgrade', b'proxy-connection'
)


class Downloader(Protocol):
    """
    This was obtained from Hawkowl's rproxy library
    (https://github.com/hawkowl/rproxy). It is used without change, and is made
    available under the MIT license, Copyright (c) 2016 Amber Brown.
    """
    def __init__(self, finished, write):
        self.finished = finished
        self._write = write

    def dataReceived(self, bytes):
        self._write(bytes)

    def connectionLost(self, reason):
        self.finished.callback(None)


@implementer(IBodyProducer)
class StringProducer(object):
    """
    This was obtained from Hawkowl's rproxy library
    (https://github.com/hawkowl/rproxy). It is used without change, and is made
    available under the MIT license, Copyright (c) 2016 Amber Brown.
    """
    def __init__(self, body):
        self.body = body.read()
        self.length = len(self.body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


class RProxyResource(Resource):
    """
    This is a variation of the RProxyResource provided by Hawkowl's rproxy
    library (https://github.com/hawkowl/rproxy). The original code is made
    available under the MIT License, and is Copyright (c) 2016 Amber Brown.

    Any changes are made available under the same license as this module.

    The changes included in this class are:

        - Removal of many of the general options to be much more specific.
        - Ability to add custom headers to all responses.
        - General simplification and removal of unneeded features.
    """
    isLeaf = True

    def __init__(self, hosts, pool, customHeaders, reactor):
        self._hosts = hosts
        self._agent = Agent(reactor, pool=pool)
        self._customHeaders = customHeaders

    def _addCustomHeaders(self, request):
        """
        Add custom headers to a given response.
        """
        for header, values in self._customHeaders:
            request.responseHeaders.setRawHeaders(header, values)

    def _rewritePathOutgoing(self, host, path):
        """
        Rewrite the path portion of the request, if needed.
        """
        rewriteRules = host.get("rewrite")
        if rewriteRules is None:
            return path

        for start, replace in rewriteRules:
            if path.startswith(start):
                return path.replace(start, replace, 1)

        return path

    def _rewriteUriResponse(self, originalHostname, host, url):
        """
        Rewrite the location header in the URL response.

        Makes two changes:

        - If the URL is absolute, we will change the hostname to the proxy
          hostname instead of the target hostname.
        - If there are URL rewrite rules, it will *undo* them.
        """
        targetHostname = host["host"]
        parsedURL = URLPath.fromString(url)
        if parsedURL.netloc == targetHostname:
            parsedURL.netloc = originalHostname

        rewriteRules = host.get("rewrite", [])
        path = parsedURL.path

        for replace, start in rewriteRules:
            if path.startswith(start):
                parsedURL.path = path.replace(start, replace, 1)
                break

        return str(parsedURL)

    def render(self, request):
        requestHostname = request.getRequestHostname().lower()
        host = self._hosts.get(requestHostname)

        if not host and requestHostname.startswith("www."):
            requestHostname = requestHostname[4:]
            host = self._hosts.get(requestHostname)

        if not host:
            request.code = 404
            self._addCustomHeaders(request)
            return b""

        path = self._rewritePathOutgoing(host, request.path)
        url = "{}://{}:{}{}".format(
            host["scheme"], host["host"], host["port"], path
        )

        urlFragments = urlparse(request.uri)

        if urlFragments.query:
            url += "?" + urlFragments.query

        for header in TRANSPORT_HEADERS:
            request.requestHeaders.removeHeader(header)

        prod = StringProducer(request.content)

        d = self._agent.request(request.method, url,
                                request.requestHeaders, prod)

        def write(res):
            request.code = res.code
            request.responseHeaders = res.headers
            self._addCustomHeaders(request)

            locationHeader = b"".join(
                request.responseHeaders.getRawHeaders("location", [])
            )
            if locationHeader:
                newLocation = self._rewriteUriResponse(
                    requestHostname, host, locationHeader
                )
                request.responseHeaders.setRawHeaders(
                    "location", [newLocation]
                )

            f = Deferred()
            res.deliverBody(Downloader(f, request.write))
            f.addCallback(lambda _: request.finish())
            return f

        def failed(res):
            request.code = 500
            self._addCustomHeaders(request)
            request.write(str(res))
            request.finish()

        d.addCallback(write)
        d.addErrback(failed)

        return server.NOT_DONE_YET


class RedirectResource(Resource):
    """
    A resource that forcibly redirects all traffic to HTTPS.
    """
    isLeaf = True

    def render(self, request):
        """
        All insecure requests are automatically redirected to HTTPS.
        """
        urlpath = request.URLPath()
        urlpath.scheme = "https"
        # This is dumb, but necessary: Twisted uses only the prepath for
        # request.URLPath, but we want to redirect the entire thing.
        urlpath.path = request.path

        # We want 301.
        request.setResponseCode(MOVED_PERMANENTLY)
        request.setHeader(b"location", str(urlpath))
        request.setHeader(
            "X-Clacks-Overhead",
            "GNU Terry Pratchett"
        )
        return b""
