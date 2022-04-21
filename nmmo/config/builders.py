def build_from_dict(config_dict):
    class CustomClass(*config_dict["presets_list"]):
        pass

    config = CustomClass()
    for key, value in config_dict["parameters"].items():
        setattr(config, key, value)

    return config
