import yaml


def yaml_coerce(value):
    # if value is string then convert to yaml and return value
    if isinstance(value, str):
        # So, in summary, this code snippet takes a value, wraps it in a YAML-formatted string as
        # the value of a dummy key, parses the string into a Python dictionary, and then returns
        # the original value.
        return yaml.load(f"dummy: {value}", Loader=yaml.SafeLoader)["dummy"]
    return value
