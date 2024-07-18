from setuptools import setup

requires = ['Sphinx>=0.6', 'feedgen', 'python-dateutil']

# long_desc = open('README.rst').read()
long_desc = """

This repository is published on https://github.com/lsaffre/sphinxfeed

This Sphinx extension is a fork of Fergus Doyle's `sphinxfeed package
<https://github.com/junkafarian/sphinxfeed>`__ which itself is derived from Dan
Mackinlay's `sphinxcontrib.feed
<http://bitbucket.org/birkenfeld/sphinx-contrib/src/tip/feed/>`_ package.  It
relies on Lars Kiesow's `python-feedgen <https://feedgen.kiesow.be>`__ package
instead of the defunct `feedformatter
<http://code.google.com/p/feedformatter/>`_ package or of Django utils to
generate the feed.

Features added by Luc Saffre & Jason Cook:

- 20190315 : Support Python 3 (by using feedgen instead of feedformatter).
  feed_description is no longer optional.

- new config variable ``feed_field_name`` to change the name of the
  metadata field to use for specifying the publication date.
- don't publish items whose publication datetime is in the future.
- respect `use_dirhtml` option from `rstgen` when calculating the url
- 20240530 : add support to write
  `ATOM <https://validator.w3.org/feed/docs/atom.html>`__ instead of RSS.

- 20240601 : look for two new fields ``category`` and ``tags`` in the `page
  metadata
  <https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html>`__
  and if either field or both is present, call the
  :meth:`feedgen.FeedEntry.category` method to add ``<category>`` elements to
  the feed item. The difference between ``category`` and ``tags`` is that  the
  ``category`` of a blog post may contain whitespace while the ``tags`` metadata
  field is a space-separated list of tags, so each tag must be a single word.
  Both the category and each tag will become a ``<category>`` element in the
  feed item.

- 20240718 : merged 7 commits with minor fixes and config updates from `pull
  request suggested by JWCook <https://github.com/lsaffre/sphinxfeed/pull/1>`__


Usage
-----

#. Install ``sphinxfeed`` using something like the following::

    git clone https://github.com/lsaffre/sphinxfeed.git
    pip install -e sphinxfeed


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

#. Sphinxfeed will include only `.rst` file that have a ``:date:`` field with a
   date that does not lie in the future.

N.B.: The README.rst file    

"""

SETUP_INFO = dict(name='sphinxfeed',
                  version='0.3',
                  license='BSD-2-Clause',
                  author='Luc Saffre',
                  author_email='luc.saffre@gmail.com',
                  url='https://github.com/lsaffre/sphinxfeed',
                  description='Sphinx extension for generating RSS feeds',
                  long_description=long_desc,
                  classifiers=[
                      'Development Status :: 4 - Beta',
                      'Environment :: Console',
                      'Environment :: Web Environment',
                      'Intended Audience :: Developers',
                      'License :: OSI Approved :: BSD License',
                      'Operating System :: OS Independent',
                      'Programming Language :: Python',
                      'Topic :: Documentation',
                      'Topic :: Utilities',
                  ],
                  platforms='any',
                  py_modules=['sphinxfeed'],
                  include_package_data=True,
                  install_requires=requires,
                  test_suite='tests',
                  tests_require=['atelier'])

if __name__ == '__main__':
    setup(**SETUP_INFO)
