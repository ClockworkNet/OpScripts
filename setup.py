# vim: set fileencoding=utf-8 :
"""python-opscripts setup
"""
# Standard library
import os.path
import re
import site
import sys
# Third-party
from setuptools import find_packages, setup

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
with open("opscripts/__init__.py", "rb") as f:
    results = re_info.search(f.read().decode("utf-8"))
    metadata = results.groupdict()
with open("README.rst", "rb") as f:
    long_description = f.read().decode("utf-8")
install_requires = ["ConfigArgParse"]
classifiers = ["License :: OSI Approved :: MIT License",
               "Natural Language :: English",
               "Programming Language :: Python :: 2",
               "Programming Language :: Python :: 2.6",
               "Programming Language :: Python :: 2.7",
               "Programming Language :: Python :: Implementation :: CPython"]
packages = find_packages(".")
print "--"
from pprint import pprint
pprint(packages)
print "--"
# Install config file appropriately
etc_path = "etc/opscripts"
examples_path = "examples"
if hasattr(sys, "real_prefix"):
    etc_path = os.path.join(sys.prefix, etc_path)
    examples_path = os.path.join(sys.prefix, examples_path)
elif "--user" in sys.argv:
    etc_path = os.path.join(site.USER_BASE, etc_path)
    examples_path = os.path.join(site.USER_BASE, examples_path)
else:
    etc_path = os.path.join("/", etc_path)

setup(name="OpScripts",
      version=metadata["version"],
      maintainer=metadata["maintainer"],
      maintainer_email=metadata["maintainer_email"],
      license=metadata["license"],
      description=metadata["description"],
      long_description=long_description,
      url=metadata["url"],
      packages=packages,
      data_files=[(examples_path, ["script_template.py"]),
                  (etc_path, [".placeholder"])],
      keywords="CLI, DevOps, Ops, sysadmin, Systems administration",
      classifiers=classifiers,
      download_url="https://github.com/ClockworkNet/OpScripts/releases",
      zip_safe=True)
