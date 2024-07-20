# -*- coding: UTF-8 -*-
# Copyright 2018-2024 Rumma & Ko Ltd
"""
Run a sphinx-build and then check whether the generated files (in
`tmp`) are the same as in `expected`.

The tests fail when the Sphinx version has changed.  In that case::

  $ diff tmp/ tests/docs1/expected

and if there is no other changes, update the expected files::

  $ cp tmp/*.html tmp/*.js tests/docs1/expected

"""

import filecmp
from unittest import TestCase
import subprocess


class AllTests(TestCase):

    def test_all(self):
        args = ['sphinx-build']
        args += ["-b"]
        args += ["html"]
        args += ["tests/docs1"]
        args += ["tmp"]
        subprocess.check_output(args, stderr=subprocess.STDOUT)

        common = [
            "index.html", "first.html", "search.html", "genindex.html",
            "searchindex.js"
        ]
        # common.append("rss.xml")

        match, mismatch, errors = filecmp.cmpfiles("tests/docs1/expected",
                                                   "tmp", common)

        self.assertEqual(mismatch, [])
        self.assertEqual(match, common)
