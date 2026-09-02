author = 'Jonathan Dung'  # ruff: ignore[undocumented-public-module]
copybutton_exclude = '.linenos, .gp, .go'
copybutton_prompt_text = '>>> '
copyright = '2026 Jonathan Dung'  # ruff: ignore[builtin-variable-shadowing]
extensions = [
    'notfound.extension',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_argparse_cli',
    'sphinx_copybutton',
]
release = '1.2.1'
html_short_title = f'check-empty {release} docs'
html_theme = 'furo'
html_theme_options = {
    'source_repository': 'https://github.com/jonathandung/check-empty',
    'source_branch': 'main',
    'source_directory': 'docs/source/',
    'top_of_page_buttons': ['view', 'edit'],
}
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
napoleon_google_docstring = True
need_sphinx = '9.1.0'
project = 'check-empty'
pygments_style = 'sphinx'
version = '1.2'
