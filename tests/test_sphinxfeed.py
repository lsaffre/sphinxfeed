# Copyright 2018-2024 Rumma & Ko Ltd
"""
Runs sphinx builds using SphinxTestApp to generate RSS and Atom feeds, and compares them to expected
output one element at a time. Shows detailed output on failure.
"""

from io import StringIO
from pathlib import Path
from textwrap import dedent
from xml.etree import ElementTree

import pytest
from sphinx.testing.util import SphinxTestApp

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

ATOM_SCHEMA = "http://www.w3.org/2005/Atom"
ATOM_META_ATTRIBUTES = [
  "id",
  "author",
  "generator",
  "link",
  "rights",
  "title",
  "updated",
]
ATOM_ITEM_ATTRIBUTES = [
  "id",
  "author",
  "link",
  "published",
  "title",
  "updated",
]


@pytest.mark.sphinx("html", testroot="rss")
def test_build_rss(app: SphinxTestApp, status: StringIO):
    app.build(force_all=True)
    assert "build succeeded" in status.getvalue()

    build_dir = Path(app.srcdir) / "_build" / "html"
    _compare_rss_feeds((build_dir / "rss.xml"), (OUTPUT_DIR / "rss.xml"))


def _compare_rss_feeds(file_1: Path, file_2: Path):
    """Compare XML contents of two RSS feeds, ignoring formatting, whitespace, and build date."""
    feed_contents_1 = _parse_xml(file_1).find("channel")
    feed_contents_2 = _parse_xml(file_2).find("channel")

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
        post_1 = _normalize_html(item_1.find("description"))
        post_2 = _normalize_html(item_2.find("description"))
        assert post_1 == post_2


@pytest.mark.sphinx("html", testroot="atom")
def test_build_atom(app: SphinxTestApp, status: StringIO):
    app.build(force_all=True)
    assert "build succeeded" in status.getvalue()

    build_dir = Path(app.srcdir) / "_build" / "html"
    _compare_atom_feeds((build_dir / "atom.xml"), (OUTPUT_DIR / "atom.xml"))


def _compare_atom_feeds(file_1: Path, file_2: Path):
    """Compare XML contents of two Atom feeds, ignoring formatting, whitespace, and build date."""
    feed_contents_1 = _parse_xml(file_1)
    feed_contents_2 = _parse_xml(file_2)

    # compare metadata
    for attr in ATOM_META_ATTRIBUTES:
        full_attr = f"{{{ATOM_SCHEMA}}}{attr}"
        assert feed_contents_1.find(full_attr).text == feed_contents_1.find(full_attr).text

    # Compare all feed items
    feed_items_1 = feed_contents_1.findall("entry")
    feed_items_2 = feed_contents_2.findall("entry")
    for entry_1, entry_2 in zip(feed_items_1, feed_items_2, strict=True):
        for attr in ATOM_ITEM_ATTRIBUTES:
            assert entry_1.find(attr).text == entry_2.find(attr).text
        # compare post contents
        post_1 = _normalize_html(entry_1.find("content"))
        post_2 = _normalize_html(entry_2.find("content"))
        assert post_1 == post_2

def _parse_xml(file: Path):
    return ElementTree.fromstring(file.read_text())

def _normalize_html(e: ElementTree.Element):
    return dedent(e.text).strip()
