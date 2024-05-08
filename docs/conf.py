extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]
source_suffix = ".rst"
master_doc = "index"
project = "xbrl-us"
year = "2023"
author = "hamid-vakilzadeh"
copyright = f"{year}, {author}"
version = release = "0.0.43"

pygments_style = "emacs"
highlight_language = "python"
templates_path = ["."]
extlinks = {
    "issue": ("https://github.com/hamid-vakilzadeh/python-xbrl-us/issues/%s", "#"),
    "pr": ("https://github.com/hamid-vakilzadeh/python-xbrl-us/pull/%s", "PR #"),
}
html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/hamid-vakilzadeh/python-xbrl-us/",
}

html_use_smartypants = True
html_last_updated_fmt = "%b %d, %Y"
html_split_index = False
html_sidebars = {
    "**": ["sidebar/search.html", "sidebar/navigation.html", "sidebar/ethical-ads.html"],
}
html_short_title = f"{project}-{version}"

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False
