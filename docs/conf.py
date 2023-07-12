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
    "sphinx_rtd_theme",
	'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
    'sphinx_tabs.tabs',
	'notfound.extension',
    'sphinxext.remoteliteralinclude',
	"sphinxext.opengraph",
	"sphinxcontrib.ghcontributors",
    "sphinx_design"
]

ogp_site_url = "https://docs.hydra.org/en/latest/"
ogp_site_name = "Hydra Documentation"
ogp_image = "https://raw.githubusercontent.com/JeffersonLab/HydraDocumentation/blob/Development/docs/img/hydra_small_logo.png"

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

templates_path = ['_templates']

hoverxref_roles = ['term']

intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

html_static_path = ['_static']
def setup(app):
    app.add_css_file('theme_overrides.css')

pygments_style = "sphinx"

# -- Options for HTML output

html_title = "Hydra Docs"
html_favicon = "img/hydra_small_logo.png"

html_theme = 'furo'
html_logo = 'img/hydra_logo.png'
html_theme_options = {
    "sidebar_hide_name": True,
    "light_css_variables": {
        "font-stack": '-apple-system, BlinkMacSystemFont, avenir next, avenir, segoe ui, helvetica neue, helvetica, Ubuntu, roboto, noto, arial, sans-serif;',
        "admonition-font-size": "1rem",
        "admonition-title-font-size": "1rem",
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f7f7f7",
        "color-background-hover": "#efeff400",
        "color-background-hover--transparent": "#efeff400",
        "color-brand-primary": "#006492",
        "color-brand-content": "#006492",
        "color-foreground-primary": "#2d2d2d",
        "color-foreground-secondary": "#39a4d5",
        "color-foreground-muted": "#2d2d2d",
        "color-foreground-border": "#ffffff",
        "color-background-border": "ffffff",
        "color-api-overall": "#101010",
        },
    "dark_css_variables" : {
        # Background color of pages
        "color-background-primary": "#242c37",
        "color-background-secondary": "#0f3e3e",
        "color-background-hover": "#efeff400",
        "color-background-hover--transparent": "#efeff400",
        "color-brand-primary": "#53c653",
        "color-brand-secondary": "#39a4d5",
        "color-brand-content": "#53c653",
        "color-foreground-primary": "#ffffff",
        "color-foreground-secondary": "#ffffff",
        "color-foreground-muted": "#ffffff",
        "color-foreground-border": "transparent",
        "color-background-border": "transparent",
        "color-api-overall": "#101010",
        "color-inline-code-background": "#0d0d0d",
    },
}
html_show_sphinx = False
html_show_sourceLink = False




# -- Options for EPUB output
epub_show_urls = 'footnote'

suppress_warnings = ['epub.unknown_project_files']

sphinx_tabs_valid_builders = ['epub', 'linkcheck']
