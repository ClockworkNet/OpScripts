# vim: set fileencoding=utf-8 :

"""Unit Tests
"""

# Standard Library
from __future__ import absolute_import, division, print_function
try:
    from collections import OrderedDict     # Python 2.7+
except ImportError:
    from ordereddict import OrderedDict     # Python 2.6

# Third-party
import yaml

# Local/library specific
from opscripts.yaml import v1 as ops_yaml


YAML_DOC = """---
one: alfa
two:
- bravo
- charlie
- delta
three: echo
four:
    apple: fruit
    bear: mammal
    carrot: vegetable
"""


def test_odict_dumper():
    # GIVEN an OrderedDict data structure
    odict = OrderedDict()
    odict["one"] = "alfa"
    odict["two"] = ["bravo", "charlie", "delta"]
    odict["three"] = "echo"
    odict["four"] = {"apple": "fruit", "bear": "mammal", "carrot": "vegetable"}
    # WHEN the custom representer is loaded
    yaml.SafeDumper.add_representer(OrderedDict, ops_yaml.odict_rep)
    # THEN a yaml dump of the OrderedDict should complete without error and it
    #      should match the expected structure.
    doc = yaml.safe_dump(odict, default_flow_style=False, explicit_start=True,
                         indent=4)
    assert doc == YAML_DOC
