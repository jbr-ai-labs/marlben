def parse_resources_configuration(resources_cfg):
    parameters = {}

    parameters["RESOURCE_BASE_RESOURCE"] = resources_cfg["resource_capacity"]
    parameters["RESOURCE_HARVEST_RESTORE_FRACTION"] = resources_cfg["restore_fraction"]
    parameters["RESOURCE_COOLDOWN"] = resources_cfg["cooldown"]

    return parameters