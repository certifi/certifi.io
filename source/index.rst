.. bob-builder documentation master file, created by
   sphinx-quickstart on Thu Mar 20 16:10:07 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bob Builder: Binary Build Toolkit
=================================

Bob-Builder is an *MIT Licensed* binary build framework, written in Python for human beings.

It's effectively a miniaturized version of *Homebrew* — oriented around composable builds,
explicit dependencies, and shipping pre-built binaries for workflows like *Heroku buildpacks*.

Bob is powered by Python, Boto, Doctopt, Amazon S3, Bash, and good intentions.

::

    $ bob build runtimes/php-5.1.10
    Fetching dependencies... found 2:
      - libraries/zlib
      - libraries/libmemcached
    === Fetching PHP v5.1.10 source...
    === Compiling PHP v5.1.10...
    ...
    === Cleaning up...
    Done building runtimes/php-5.1.10.

Bob takes all the statefullnes and labor out of maintaining a collection of binaries.


And gives you the ability to carefully handcraft the experience.




Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

