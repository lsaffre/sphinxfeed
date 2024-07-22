# Copyright 2018-2024 Rumma & Ko Ltd
"""
Runs sphinx builds using SphinxTestApp to generate RSS and Atom feeds, and compares them to expected
output one element at a time. Shows detailed output on failure.
"""

from io import StringIO
from pathlib import Path
from textwrap import dedent
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import pytest
from sphinx.testing.util import SphinxTestApp

from tests.conftest import OUTPUT_DIR

RSS_ITEM_ATTRIBUTES = ["title", "link", "description", "pubDate"]
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
    "author/name",
    "generator",
    "link",
    "rights",
    "title",
]
ATOM_ITEM_ATTRIBUTES = [
    "id",
    "content",
    "link",
    "published",
    "title",
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
        _compare_attrs(attr, feed_contents_1, feed_contents_2)

    # Compare all feed items
    feed_items_1 = feed_contents_1.findall("item")
    feed_items_2 = feed_contents_2.findall("item")
    assert len(feed_items_1) == len(feed_items_2)
    for item_1, item_2 in zip(feed_items_1, feed_items_2):
        for attr in RSS_ITEM_ATTRIBUTES:
            _compare_attrs(attr, item_1, item_2)


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
        _compare_attrs(attr, feed_contents_1, feed_contents_2, atom=True)

    # Compare all feed items
    feed_items_1 = feed_contents_1.findall(f"{{{ATOM_SCHEMA}}}entry")
    feed_items_2 = feed_contents_2.findall(f"{{{ATOM_SCHEMA}}}entry")
    assert len(feed_items_1) == len(feed_items_2)
    for entry_1, entry_2 in zip(feed_items_1, feed_items_2):
        for attr in ATOM_ITEM_ATTRIBUTES:
            _compare_attrs(attr, entry_1, entry_2, atom=True)


def _parse_xml(file: Path):
    return ElementTree.fromstring(file.read_text())


def _compare_attrs(attr: str, e1: Element, e2: Element, atom: bool = False):
    """Compare attribute values in two XML elements, handle variations in formatting, and print
    comparison to show on test failure.
    """
    print(f"[{attr}]:")

    # For Atom feeds, we need to append the Atom schema to the attribute name
    if atom:
        if attr == "author/name":
            attr = f"{{{ATOM_SCHEMA}}}author/{{{ATOM_SCHEMA}}}name"
        else:
            attr = f"{{{ATOM_SCHEMA}}}{attr}"

    # Handle one or both values missing
    if (val_1 := e1.find(attr)) is None or (val_2 := e2.find(attr)) is None:
        raise ValueError(f"Attribute {attr} missing")
    # Handle link attribute
    if atom and attr.endswith("link"):
        text_1 = val_1.attrib["href"]
        text_2 = val_2.attrib["href"]
    # Handle whitespace differences in HTML content
    else:
        text_1 = dedent(val_1.text).strip()
        text_2 = dedent(val_2.text).strip()
    # Handle different phrasing in Sphinx <=7.1
    text_1 = text_1.replace('Permalink', 'Link')
    text_2 = text_2.replace('Permalink', 'Link')

    print(f"  expected: {text_1}\n  actual: {text_2}")
    assert text_1 == text_2
