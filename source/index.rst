.. certifiio documentation master file, created by
   sphinx-quickstart on Thu Mar 20 16:10:07 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Trust Database for Humans
=========================

Certifi is a carefully curated collection of Root Certificates for
validating the trustworthiness of SSL certificates while verifying the
identity of TLS hosts. It has been extracted from the
`Requests <https://requests.readthedocs.io/>`_ project.

The internet is an untrusted place. Every HTTP request you make should have
verification on by default. This happens every time you access a website with
your web browser, without any knowledge to the user — there's no reason your
code should be any different.

Certifi is here to make this possible.


What is it?
-----------

This **MPL Licensed** CA Bundle is extracted from the `Mozilla Included CA
Certificate List`_.

.. _Mozilla Included CA Certificate List: https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/included/


How do I use it?
----------------

- `Download the raw CA Bundle <https://mkcert.org/generate/>`_ or one of our distributions packages for Ruby, Node, Python, or Go.
- Use an HTTP client of your choice that supports SNI Verification, Like `Requests <http://www.python-requests.org/en/latest/>`_ or Curl.
- Pass the path to the CA Bundle to the HTTP Client, and verify to your heart's content!
- Sign up for email notifications of new CA Bundle releases.

Testimonials
------------

**Hynek Schlawack**
    Unless you fully understand how system trust databases work (you probably don’t) and are capable to implement support for all relevant ones (you probably aren’t), I urge you: just use certifi

**Andrey Petrov**
    One of the first things people should ask when using a new toolset: How do I use Certifi with this?


Spread the Love
---------------

This is a base platform — you shouldn't have to care about this type of thing
when you're interacting with the web. That's why your web browser takes care of
this for you.

Go, and build better software that abstracts this away from the user so that
they don't need to download this bundle and be concerned with it when they're
building amazing things.

Developers are humans too.

ॐ
