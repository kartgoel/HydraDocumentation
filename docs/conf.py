# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Hydra'
copyright = '2023, Jefferson Lab'
author = 'Jefferson Lab'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_title = "Hydra Docs"
html_favicon = 'img/hydra_small_logo.png'

html_theme = 'sphinx_rtd_theme'
html_logo = 'img/hydra_logo.png'
html_theme_options = {
    'collapse_navigation': False,
    'display_version': False,
    'logo-only': True,
    'sticky-navigation': False,
    "sidebar_hide_name": True
}
html_show_sphinx = False
html_show_sourceLink = False

def setup(app):
    app.add_css_file('theme_overrides.css')


# -- Options for EPUB output
epub_show_urls = 'footnote'
