# vim: set fileencoding=utf-8 :

"""python-opscripts setup
"""

# Standard library
from __future__ import absolute_import, division, print_function
import os.path
import re
import site
import sys
import glob

# Third-party
from setuptools import find_packages, setup


setup_path = os.path.dirname(os.path.realpath(__file__))
re_info = re.compile("""
        # Description docstring
        ^" " "(?P<description>.+)
        ^" " ".*
        # Version variable
        __version__\s*=\s*"(?P<version>[^"]+)".*
        # Maintainer variable
        __maintainer__\s*=\s*"(?P<maintainer>[^"]+)".*
        # Maintainer_email variable
        __maintainer_email__\s*=\s*"(?P<maintainer_email>[^"]+)".*
        # URL variable
        __url__\s*=\s*"(?P<url>[^"]+)".*
        # License variable
        __license__\s*=\s*"(?P<license>[^"]+)".*
        """, re.DOTALL | re.MULTILINE | re.VERBOSE)
with open(os.path.join(setup_path, "opscripts/__init__.py"), "rb") as f:
    results = re_info.search(f.read().decode("utf-8"))
    metadata = results.groupdict()
with open(os.path.join(setup_path, "README.rst"), "rb") as f:
    long_description = f.read().decode("utf-8")
install_requires = ["ConfigArgParse"]
classifiers = ["Environment :: Console",
               "Intended Audience :: System Administrators",
               "License :: OSI Approved :: MIT License",
               "Natural Language :: English",
               "Operating System :: POSIX :: Linux",
               "Programming Language :: Python :: 2",
               "Programming Language :: Python :: 2.6",
               "Programming Language :: Python :: 2.7",
               "Programming Language :: Python :: 3",
               "Programming Language :: Python :: 3.4",
               "Programming Language :: Python :: Implementation :: CPython",
               "Topic :: Software Development :: Libraries :: Python Modules",
               "Topic :: System :: Systems Administration"]
packages = find_packages(".")

# Install config file appropriately
examples_path = "examples"
if hasattr(sys, "real_prefix"):
    examples_path = os.path.join(sys.prefix, examples_path)
elif "--user" in sys.argv:
    examples_path = os.path.join(site.USER_BASE, examples_path)
examples = glob.glob(os.path.join(setup_path, "example_*.py"))
examples += [os.path.join(setup_path, "script_template.py")]

setup(name="OpScripts",
      version=metadata["version"],
      maintainer=metadata["maintainer"],
      maintainer_email=metadata["maintainer_email"],
      license=metadata["license"],
      description=metadata["description"],
      long_description=long_description,
      url=metadata["url"],
      packages=packages,
      data_files=[(examples_path, examples)],
      keywords="CLI, DevOps, Ops, sysadmin, Systems administration",
      classifiers=classifiers,
      download_url="https://github.com/ClockworkNet/OpScripts/releases",
      zip_safe=True)
