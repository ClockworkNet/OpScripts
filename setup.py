# vim: set fileencoding=utf-8 :
"""python-optscrpits setup
"""
# Standard library
import re
# Third-party
from setuptools import setup

re_info = re.compile("""
        ^" " "(?P<description>.+)                   # description docstring
        ^" " ".*
        __version__\s*=\s*"(?P<version>[^"]+)".*    # version variable
        __url__\s*=\s*"(?P<url>[^"]+)".*            # url variable
        __license__\s*=\s*"(?P<license>[^"]+)".*    # license variable
        """, re.DOTALL | re.MULTILINE | re.VERBOSE)
with open("opscripts/__init__.py", "rb") as f:
    results = re_info.search(f.read().decode("utf-8"))
    description, version, url, license = results.groups()
with open("README.rst", "rb") as f:
    long_description = f.read().decode("utf-8")
install_requires = ["ConfigArgParse"]
classifiers = ["License :: OSI Approved :: MIT License",
               "Natural Language :: English",
               "Programming Language :: Python :: 2",
               "Programming Language :: Python :: 2.6",
               "Programming Language :: Python :: 2.7",
               "Programming Language :: Python :: Implementation :: CPython"]

setup(name="python-opscripts",
      version=version,
      license=license,
      description=description,
      long_description=long_description,
      url=url,
      keywords="CLI, DevOps, Ops, sysadmin, Systems administration",
      classifiers=classifiers)
