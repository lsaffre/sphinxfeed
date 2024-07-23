# General sphinx config
source_suffix = '.rst'
master_doc = 'index'
project = "First sphinxfeed tester"
copyright = '2018 Joe Doe'
language = 'en'
html_title = "Joe's website"
html_short_title = u"Home"
html_last_updated_fmt = '%Y-%m-%d'
use_dirhtml = True

# Sphinxfeed config
extensions = ['sphinxfeed']
feed_base_url = 'http://news.example.com'
feed_author = 'Joe Dow'
feed_title = "Joe's blog"
feed_field_name = 'date'
feed_description = "Joe's blog"
feed_filename = 'atom.xml'
feed_use_atom = True