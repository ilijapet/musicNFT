import os

from .misc import yaml_coerce


def get_settings_from_environment(prefix):
    prefix_len = len(prefix)
    return {
        # from the point where prefix is ended, take the rest of the string assigne as key
        # for value use use yaml_coerce (misc.py) to convert env string to python type
        # and return dict with key and value to deep_update (collections.py) to use to update
        # existing settings with new ones from envvars
        key[prefix_len:]: yaml_coerce(value) for key, value in os.environ.items() if key.startswith(prefix)
    }
