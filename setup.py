#!/usr/bin/env python
from setuptools import setup

short_desc = "a lightweight wiki system with Markdown/Graphviz/LaTeX support"

kwargs = dict(
    name = "zbox_wiki",
    description = short_desc,
    long_description = "ZBox Wiki is %s, it's easy to use, easy to read and easy to extend." % short_desc,

    version = "201203",

    author = "Shuge Lee",
    author_email = "shuge.lee@gmail.com",

    url = "https://github.com/shuge/zbox_wiki",

    license = "MIT License",

    platforms = ["Mac OS X"],


    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Software Development :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: Markup :: HTML",
        ],


    packages = [
        "zbox_wiki",
        "zbox_wiki.commons",
        "zbox_wiki.commons.markdown",
        "zbox_wiki.commons.markdown.extensions",
        "zbox_wiki.commons.web",
        "zbox_wiki.commons.web.contrib",
        "zbox_wiki.commons.web.wsgiserver",
        ],

    package_data = {
      "zbox_wiki" : [
          "pages/robots.txt",
          "pages/zbox-wiki/*.md",
          "pages/zbox-wiki/nginx-*.conf",
          "pages/zbox-wiki/apache2-*.conf",
          "scripts/*.py",
          "scripts/*.sh",
          "static/css/*.css",
          "static/js/*.js",
          "static/js/prettify/*.js",
          "static/js/prettify/*.css",
          "templates/*.tpl",
          ],
    },

    scripts = [
        "zbox_wiki/scripts/zwadmin.py",
        "zbox_wiki/scripts/zwd.py",
    ],
)

setup(**kwargs)
