# This application is derived from Dan Mackinlay's sphinxcontrib.feed package.
# The original can be found at http://bitbucket.org/birkenfeld/sphinx-contrib/src/tip/feed/
"""
See https://github.com/lsaffre/sphinxfeed
"""

import os.path
import time
from datetime import datetime
from dateutil.tz import tzlocal
from logging import getLogger

from feedgen.feed import FeedGenerator
from feedgen.feed import FeedEntry

import rstgen

USE_ATOM = True

doc_trees = []  # for atelier
logger = getLogger(__name__)


def parse_pubdate(pubdate):
    # tz = "+0002"
    # chunks = pubdate.split()
    # if len(chunks) == 1:
    #     chunks.append("23:59")
    # if len(chunks) == 2:
    #     chunks.append(tz)
    # fmt = '%Y-%m-%d %H:%M %Z'
    # return time.strptime(' '.join(chunks), fmt)
    fmt = '%Y-%m-%d %H:%M'
    try:
        date = time.strptime(pubdate, fmt)
    except ValueError:
        date = time.strptime(pubdate + " 23:59", fmt)
    return date


def setup(app):
    """ see: http://sphinx.pocoo.org/ext/appapi.html
        this is the primary extension point for Sphinx
    """
    from sphinx.application import Sphinx
    if not isinstance(app, Sphinx): return
    app.add_config_value('feed_base_url', '', 'html')
    app.add_config_value('feed_description', '', 'html')
    app.add_config_value('feed_author', '', 'html')
    app.add_config_value('feed_field_name', 'Publish Date', 'env')
    app.add_config_value('feed_filename', 'rss.xml', 'html')
    # app.add_config_value('use_dirhtml', False, 'html')

    app.connect('html-page-context', create_feed_item)
    app.connect('build-finished', emit_feed)
    app.connect('builder-inited', create_feed_container)

    #env.process_metadata deletes most of the docinfo, and dates
    #in particular.


def create_feed_container(app):
    #from feedformatter import Feed
    feed = FeedGenerator()
    feed.title(app.config.project)
    feed.link(href=app.config.feed_base_url)
    if USE_ATOM:
        feed.id(app.config.feed_base_url)
    feed.author(dict(name=app.config.feed_author))
    feed.description(app.config.feed_description)

    if app.config.language:
        feed.language(app.config.language)
    if app.config.copyright:
        feed.copyright(app.config.copyright)
    app.builder.env.feed_feed = feed
    if not hasattr(app.builder.env, 'feed_items'):
        app.builder.env.feed_items = {}


def create_feed_item(app, pagename, templatename, ctx, doctree):
    """ Here we have access to nice HTML fragments to use in, say, an RSS feed.
    """

    env = app.builder.env
    metadata = app.builder.env.metadata.get(pagename, {})

    pubDate = metadata.get(app.config.feed_field_name, None)
    if not pubDate:
        return

    pubDate = parse_pubdate(pubDate)

    if pubDate > time.localtime():
        logger.warning("Skipping %s, publish date is in the future: %s", pagename, pubDate)
        return

    if not ctx.get('body') or not ctx.get('title'):
        return

    pubDate = datetime.fromtimestamp(time.mktime(pubDate))
    pubDate = pubDate.replace(tzinfo=tzlocal())

    item = FeedEntry()
    item.title(ctx.get('title'))
    href = app.config.feed_base_url + '/' + ctx['current_page_name']
    if not rstgen.get_config_var('use_dirhtml'):
        href += ctx['file_suffix']
    item.link(href=href)
    if USE_ATOM:
        item.id(href)
    item.description(ctx.get('body'))
    item.published(pubDate)

    if 'author' in metadata:
        item.author(metadata['author'])

    if cat := metadata.get("category", None):
        item.category(term=cat)
    if tags := metadata.get("tags", None):
        for tag in tags.split():
            item.category(term=tag)

    env.feed_items[pagename] = item

    #Additionally, we might like to provide our templates with a way to link to the rss output file
    ctx['rss_link'] = app.config.feed_base_url + '/' + app.config.feed_filename


def emit_feed(app, exc):
    ordered_items = list(app.builder.env.feed_items.values())
    feed = app.builder.env.feed_feed
    # ordered_items.sort(key=lambda x: x['pubDate'], reverse=True)
    ordered_items.sort(key=lambda x: x.published())
    for item in ordered_items:
        feed.add_entry(item)  # prepends the item
        # for k, v in item.items():
        #     getattr(e, k)(v)

    path = os.path.join(app.builder.outdir, app.config.feed_filename)
    # print(20190315, path)
    if USE_ATOM:
        feed.atom_file(path)
    else:
        feed.rss_file(path)

    return
    # LS 20180204 The following code (pickle the environment and check
    # consistency at this point) caused an error when also bibtex was
    # installed. I deactivated it since I don't know why it's needed.

    from os import path
    from sphinx.application import ENV_PICKLE_FILENAME
    from sphinx.util.console import bold
    # save the environment
    builder = app.builder
    builder.info(bold('pickling environment... '), nonl=True)
    builder.env.topickle(path.join(builder.doctreedir, ENV_PICKLE_FILENAME))
    builder.info('done')

    # global actions
    builder.info(bold('checking consistency... '), nonl=True)
    builder.env.check_consistency()
    builder.info('done')


## Tests

# ... TODO

if __name__ == '__main__':
    import unittest
    unittest.main()
