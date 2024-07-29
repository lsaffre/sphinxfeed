# This application is derived from Dan Mackinlay's sphinxcontrib.feed package.
# The original can be found at http://bitbucket.org/birkenfeld/sphinx-contrib/src/tip/feed/
"""
See https://github.com/lsaffre/sphinxfeed
"""

__version__ = '0.3.5'

import os.path
from datetime import datetime
from uuid import NAMESPACE_URL, uuid5

from dateutil.parser import parse as parse_date
from dateutil.tz import tzlocal
from feedgen.feed import FeedEntry, FeedGenerator
from sphinx.util.logging import getLogger


doc_trees = []  # for atelier
logger = getLogger(__name__)


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
    app.add_config_value('feed_entry_permalink', False, 'html')
    app.add_config_value('feed_use_atom', False, 'html')
    app.add_config_value('use_dirhtml', False, 'html')

    app.connect('html-page-context', create_feed_item)
    app.connect('build-finished', emit_feed)
    app.connect('builder-inited', create_feed_container)

    #env.process_metadata deletes most of the docinfo, and dates
    #in particular.


def create_feed_container(app):
    feed = FeedGenerator()
    feed.title(app.config.project)
    feed.link(href=app.config.feed_base_url)
    if app.config.feed_use_atom:
        feed.id(app.config.feed_base_url)
    feed.author({'name': app.config.feed_author})
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

    pubdate = metadata.get(app.config.feed_field_name, None)
    if not pubdate:
        return

    # Default to local timezone, unless one is explicitly provided
    pubdate = parse_date(pubdate)
    if not pubdate.tzinfo:
        pubdate = pubdate.replace(tzinfo=tzlocal())
    if pubdate > datetime.now(tzlocal()):
        logger.info("Skipping %s, publish date is in the future: %s", pagename, pubdate)
        return

    if not ctx.get('body') or not ctx.get('title'):
        return

    item = FeedEntry()
    item.title(ctx.get('title'))
    href = app.config.feed_base_url + '/' + ctx['current_page_name']
    if not app.config.use_dirhtml:
        href += ctx['file_suffix']
    item.link(href=href)
    item.description(ctx.get('body'))
    item.published(pubdate)

    # Entry ID option 1: Use a GUID as a permalink. Also sets item.id for Atom.
    if app.config.feed_entry_permalink:
        if not (guid :=  metadata.get('guid')):
            guid = uuid5(NAMESPACE_URL, href)
        item.guid(str(guid), permalink=True)
    # Entry ID option 2: Use the URL as the ID. Also sets item.guid (non-permalink) for RSS.
    else:
        item.id(href)

    if author := metadata.get('author'):
        # author may be a str (in field list/frontmatter) or a dict (expected by feedgen)
        if isinstance (author, str):
            author = {'name': author}
        item.author(author)
    if cat := metadata.get("category", None):
        item.category(term=cat)
    if tags := metadata.get("tags", None):
        # tags may be a str (in field list/frontmatter), or a list (from sphinx-tags extension)
        if isinstance(tags, str):
            tags = tags.split()
        for tag in tags:
            item.category(term=tag)

    env.feed_items[pagename] = item

    #Additionally, we might like to provide our templates with a way to link to the rss output file
    ctx['rss_link'] = app.config.feed_base_url + '/' + app.config.feed_filename


def emit_feed(app, exc):
    ordered_items = list(app.builder.env.feed_items.values())
    feed = app.builder.env.feed_feed
    ordered_items.sort(key=lambda x: x.published())
    for item in ordered_items:
        feed.add_entry(item)  # prepends the item

    path = os.path.join(app.builder.outdir, app.config.feed_filename)

    if app.config.feed_use_atom:
        feed.atom_file(path)
    else:
        feed.rss_file(path)
