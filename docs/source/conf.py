# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../pylunix'))

project = 'PyLunix'
copyright = '2025, magicoldeier19'
author = 'magicoldeier19'
release = '0.2.0.alpha3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx_autodoc_typehints',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    "sphinx_inline_tabs",
    'sphinx.ext.autosummary',
    "sphinx_design",
    "sphinx_copybutton",
]

autosummary_generate = True

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# 翻譯存檔位置
locale_dirs = ['locale/']
gettext_compact = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

master_doc = 'index'

html_theme_options = {
    "sidebar_hide_name": False,  # 確保顯示專案名稱
}
html_sidebars = {
    "**": [
        "sidebar/brand.html",      # 原本的 Logo 和標題
        "lang_switch.html",       # 插入我們新做的按鈕檔案
        "sidebar/search.html",     # 原本的搜尋框
        "sidebar/scroll-start.html",
        "sidebar/navigation.html", # 原本的導覽目錄
        "sidebar/scroll-end.html",
    ]
}