# Copyright 2018-2024 Rumma & Ko Ltd
"""
Run a sphinx build using SphinxTestApp to generate an RSS feed, and compare each element in the
output to the expected output.
"""

from pathlib import Path
import pytest
from io import StringIO
from sphinx.testing.util import SphinxTestApp
from xml.etree import ElementTree
from textwrap import dedent

from tests.conftest import OUTPUT_DIR

RSS_ITEM_ATTRIBUTES = ["title", "link", "pubDate"]
RSS_META_ATTRIBUTES = [
    "copyright",
    "description",
    "docs",
    "generator",
    "language",
    "link",
    "title",
]

@pytest.mark.sphinx("html", testroot="rss")
def test_build_rss(app: SphinxTestApp, status: StringIO):
    app.build(force_all=True)
    assert "build succeeded" in status.getvalue()

    build_dir = Path(app.srcdir) / "_build" / "html"
    compare_rss_feeds((build_dir / "rss.xml"), (OUTPUT_DIR / "rss.xml"))


def compare_rss_feeds(file_1: Path, file_2: Path):
    """Compare XML contents of two RSS feeds, ignoring formatting, whitespace, and build date.
    Shows detailed output on failure.
    """
    feed_contents_1 = ElementTree.fromstring(file_1.read_text()).find("channel")
    feed_contents_2 = ElementTree.fromstring(file_2.read_text()).find("channel")

    # compare metadata
    for attr in RSS_META_ATTRIBUTES:
        assert feed_contents_1.find(attr).text == feed_contents_1.find(attr).text

    # Compare all feed items
    feed_items_1 = feed_contents_1.findall("item")
    feed_items_2 = feed_contents_2.findall("item")
    for item_1, item_2 in zip(feed_items_1, feed_items_2, strict=True):
        for attr in RSS_ITEM_ATTRIBUTES:
            assert item_1.find(attr).text == item_2.find(attr).text
        # compare post contents
        post_1 = dedent(item_1.find("description").text).strip()
        post_2 = dedent(item_2.find("description").text).strip()
        assert post_1 == post_2
