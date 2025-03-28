from atelier.invlib import setup_from_tasks

ns = setup_from_tasks(
    globals(),
    "sphinxfeed",
    blogref_url="https://luc.lino-framework.org",
    revision_control_system='git',
    test_command="pytest tests",  # more options in file pytest.ini
    # tolerate_sphinx_warnings=True,
    cleanable_files=[])
