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

Features added
==============

- Support Python 3 (by using feedgen instead of feedformatter).
- Don't publish items having a publication datetime in the future.
- Ability to write
  `ATOM <https://validator.w3.org/feed/docs/atom.html>`__ instead of RSS.

- Detect ``category`` and ``tags`` fields in the `page metadata
  <https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html>`__
  and if either or both is present, call the `feedgen.FeedEntry.category()`
  method to add ``<category>`` elements to the feed item.  The difference
  between ``category`` and ``tags`` is that  the ``category`` of a blog post may
  contain whitespace while the ``tags`` metadata field is a space-separated list
  of tags, so each tag must be a single word. Both the category and each tag
  will become a ``<category>`` element in the feed item.

- Additional Sphinx config variables:

  - ``feed_field_name`` to change the name of the
    metadata field to use for specifying the publication date.

  - ``use_dirhtml`` to specify whether `dirhtml` instead of `html` builder is
    used when calculating the url

  - ``feed_use_atom`` to generate an Atom feed instead of RSS


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

Manuael release to PyPI without GitHub::

  $ hatch build
  $ twine check --strict dist/*
  $ twine upload dist/*

The ``twine upload`` step requires authentication credentials in your
`~/.pypirc` file.
