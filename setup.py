# vim: set fileencoding=utf-8 :
"""python-opscripts setup
"""
# Standard library
import distutils.sysconfig
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
config_file_path = "etc/opscripts"
if hasattr(sys, "real_prefix"):
    config_file_path = os.path.join(sys.prefix, config_file_path)
elif "--user" in sys.argv:
    config_file_path = os.path.join(site.USER_BASE, config_file_path)
else:
    config_file_path = os.path.join(distutils.sysconfig.get_python_lib(),
                                 config_file_path)

setup(name="OpScripts",
      version=metadata["version"],
      maintainer=metadata["maintainer"],
      maintainer_email=metadata["maintainer_email"],
      license=metadata["license"],
      description=metadata["description"],
      long_description=long_description,
      url=metadata["url"],
      packages=packages,
      data_files=[(config_file_path, [".placeholder"])],
      keywords="CLI, DevOps, Ops, sysadmin, Systems administration",
      classifiers=classifiers,
      download_url="https://github.com/ClockworkNet/OpScripts/releases",
      zip_safe=True)
