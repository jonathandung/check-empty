project = 'check-empty'  # ruff: ignore[undocumented-public-module]
author = 'Jonathan Dung'
copyright = '2026 Jonathan Dung'  # ruff: ignore[builtin-variable-shadowing]
version = '1.1'
release = '1.1.3'
need_sphinx = '9.1.0'
pygments_style = 'sphinx'
extensions = [
    'sphinx_argparse_cli',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'notfound.extension',
]
default_role = 'py:obj'
html_theme = 'furo'
html_theme_options = {
    'top_of_page_buttons': ['view', 'edit'],
    'source_repository': 'https://github.com/jonathandung/check-empty',
    'source_branch': 'main',
    'source_directory': 'docs/source/',
}
html_short_title = f'check-empty {release} docs'
copybutton_exclude = '.linenos, .gp, .go'
copybutton_prompt_text = '>>> '
napoleon_google_docstring = True
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
