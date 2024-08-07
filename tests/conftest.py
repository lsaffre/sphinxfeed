"""Pytest config for testing with SphinxTestApp

Notes on testing setup:
* A Sphinx test app is provided via `app` fixture from `sphinx.testing.fixtures`.
* The `sources` dir contains source files and config to use for tests
    * Set via the `rootdir` fixture
* A subdirectory to use for a specific test can be set by a pytest marker:
    * `@pytest.mark.sphinx("html", testroot="...")
    * This subdirectory must contain a conf.py and source files
* The `outputs` dir contains expected output files
* Test build output is located under `/tmp/pytest*`
"""

import shutil
from pathlib import Path

import pytest

collect_ignore = ["sources", "outputs"]
pytest_plugins = "sphinx.testing.fixtures"

OUTPUT_DIR = Path(__file__).parent.resolve() / "outputs"
SOURCE_DIR = Path(__file__).parent.resolve() / "sources"


@pytest.fixture(scope="session")
def rootdir():
    """This fixture overrides the root directory used by SphinxTestApp. Also patches in a
    Path.copytree() method for compatibility with sphinx.testing.path.path in older Sphinx versions.
    """

    class PatchedPath(type(Path())):
        def __new__(cls, *args):
            return super().__new__(cls, *args)

        def copytree(src, dest):
            shutil.copytree(src, dest, symlinks=True)

    yield PatchedPath(SOURCE_DIR)
