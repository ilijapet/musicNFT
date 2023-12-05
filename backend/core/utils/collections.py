def deep_update(base_dict, update_with):
    """
    Deep update of a dictionary used to update produciton setting with developer settings
    """
    # iterate over all key, value pairs from update_with
    for key, value in update_with.items():
        # if value is dict then we need to go deeper
        if isinstance(value, dict):
            # if base_dict has key from update_with then we need to go deeper
            base_dict_value = base_dict.get(key)

            # if base_dict has key from update_with and value is dict then we need to go deeper
            if isinstance(base_dict_value, dict):
                deep_update(base_dict_value, value)
            else:
                # if base_dict has key from update_with and value is not dict then we can just assigne value
                base_dict[key] = value
        else:
            # if value is not dict then we can just assigne value
            base_dict[key] = value
    # return updated base_dict
    return base_dict
