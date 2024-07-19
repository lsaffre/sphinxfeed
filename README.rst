==========================
The ``sphinxfeed`` package
==========================

This Sphinx extension is a fork of Fergus Doyle's `sphinxfeed package
<https://github.com/junkafarian/sphinxfeed>`__ which itself is derived from Dan
Mackinlay's `sphinxcontrib.feed
<http://bitbucket.org/birkenfeld/sphinx-contrib/src/tip/feed/>`_ package.  It
relies on Lars Kiesow's `python-feedgen <https://feedgen.kiesow.be>`__ package
instead of the defunct `feedformatter
<https://code.google.com/archive/p/feedformatter/>`_ package or of Django utils to
generate the feed.


Installation
============

Soon you can install it using pip::

  pip install sphinxfeed-lsaffre

How to test whether the right version of sphinxfeed is installed:

>>> import sphinxfeed
>>> sphinxfeed.__version__
'0.3.1'


Usage
=====

#. Add ``sphinxfeed`` to the list of extensions in your ``conf.py``::

       extensions = [..., 'sphinxfeed']

#. Customise the necessary configuration options to correctly generate
   the feed::

       feed_base_url = 'https://YOUR_HOST_URL'
       feed_author = 'YOUR NAME'
       feed_description = "A longer description"

       # optional options
       feed_field_name = 'date'  # default value is "Publish Date"
       feed_use_atom = False
       use_dirhtml = False

#. Optionally use the following metadata fields:

   - date (or any other name configured using feed_field_name)
   - author
   - tags
   - category

#. Sphinxfeed will include only `.rst` files that have a ``:date:`` field with a
   date that does not lie in the future.


Maintenance
===========

See also the files `LICENSE` and `CHANGELOG.rst`.

Install a developer version::

  git clone https://github.com/lsaffre/sphinxfeed.git
  pip install -e ".[dev]"

Run the test suite::

  $ pytest

Release a new version to PyPI::

  $ git tag v$(hatch version)
  $ git push --tags
