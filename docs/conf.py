"""
Sphinx documentation for cli-toolkit

To generate HTML documentation, run make doc in main level directory.
"""

from cli_toolkit import __version__

project = 'cli-toolkit'
author = 'Ilkka Tuohela'
# pylint: disable=redefined-builtin
copyright = '2020, Ilkka Tuohela'

version = __version__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'recommonmark',
]

templates_path = ['templates']
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

master_doc = 'index'
language = None

exclude_patterns = []
pygments_style = None

html_theme = 'sphinx_rtd_theme'
html_static_path = ['static']
# html_sidebars = {}
htmlhelp_basename = 'cli_toolkit'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
