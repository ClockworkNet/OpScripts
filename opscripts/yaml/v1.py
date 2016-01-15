# vim: set fileencoding=utf-8 :

"""OpScripts PyYAML utility functions.
"""

# Standard library
from __future__ import absolute_import, division, print_function

# Third-party
import yaml


def represent_odict(dump, tag, mapping, flow_style=None):
    """Like BaseRepresenter.represent_mapping, but does not issue the sort().

    http://blog.elsdoerfer.name/2012/07/26/make-pyyaml-output-an-ordereddict/
    """
    value = list()
    node = yaml.MappingNode(tag, value, flow_style=flow_style)
    if dump.alias_key is not None:
        dump.represented_objects[dump.alias_key] = node
    best_style = True
    if hasattr(mapping, "items"):
        mapping = mapping.items()
    for item_key, item_value in mapping:
        node_key = dump.represent_data(item_key)
        node_value = dump.represent_data(item_value)
        if not (isinstance(node_key, yaml.ScalarNode) and not node_key.style):
            best_style = False
        if not (isinstance(node_value, yaml.ScalarNode) and
                not node_value.style):
            best_style = False
        value.append((node_key, node_value))
    if flow_style is None:
        if dump.default_flow_style is not None:
            node.flow_style = dump.default_flow_style
        else:
            node.flow_style = best_style
    return node


def odict_rep(dumper, data):
    return represent_odict(dumper, u"tag:yaml.org,2002:map", data)
