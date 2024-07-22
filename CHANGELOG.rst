========================
The sphinxfeed changelog
========================

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
  `feedgen.FeedEntry.category()` method to add ``<category>`` elements to the
  feed item. The difference between ``category`` and ``tags`` is that  the
  ``category`` of a blog post may contain whitespace while the ``tags`` metadata
  field is a space-separated list of tags, so each tag must be a single word.
  Both the category and each tag will become a ``<category>`` element in the
  feed item.

- 20240718 : merged 7 commits with minor fixes and config updates from `pull
  request suggested by JWCook <https://github.com/lsaffre/sphinxfeed/pull/1>`__

- 20240720 :  The message "Skipping %s, publish date is in the future" is now
  logged at level INFO instead of WARNING because we don't want the
  ``sphinx-build -W`` to fail in this situation.

- 20240720 : Removed dependency from ``atelier`` because it's easier to call 
  `subprocess.check_output()` directly here.

- 20240722 : Support additional timestamp formats (any format supported by
  `dateutil <https://dateutil.readthedocs.io/en/stable/examples.html#parse-examples>`__)
