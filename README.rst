==========================
The ``sphinxfeed`` package
==========================





This repository is published on https://github.com/lsaffre/sphinxfeed

This Sphinx extension is a fork of Fergus Doyle's `sphinxfeed
package <https://github.com/junkafarian/sphinxfeed>`__
which itself is derived from Dan Mackinlay's
`sphinxcontrib.feed
<http://bitbucket.org/birkenfeld/sphinx-contrib/src/tip/feed/>`_
package.  It relies on
Lars Kiesow's `python-feedgen <https://feedgen.kiesow.be>`__ package
instead of the defunct `feedformatter
<http://code.google.com/p/feedformatter/>`_ package or of Django
utils to generate the feed.

Features added by Luc Saffre:

- 20190315 : Support Python 3 (by using feedgen instead of feedformatter).
  feed_description is no longer optional.

- new config variable feed_field_name to change the name of the field
  to use for specifying the publication date.
- don't publish items whose publication datetime is in the future.
- respect use_dirhtml option from rstgen when calculating the url
- 20240530 : add support to temporarily write
  `ATOM <https://validator.w3.org/feed/docs/atom.html>`__ instead of RSS.


Usage
-----

#. Install ``sphinxfeed`` using ``easy_install`` / ``pip`` /
   ``python setup.py install``

#. Add ``sphinxfeed`` to the list of extensions in your ``conf.py``::

       extensions = [..., 'sphinxfeed']

#. Customise the necessary configuration options to correctly generate
   the feed::

       feed_base_url = 'http://YOUR_HOST_URL'
       feed_author = 'YOUR NAME'
       feed_description = "A longer description"

       # optional options
       feed_field_name = 'date'  # default value is "Publish Date"


