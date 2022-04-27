def parse_env_configuration(env_cfg):
    parameters = {}
    
    horizon = env_cfg["horizon"]

    # TODO: make tasks instead of this reward configuration
    individual_survival_reward = env_cfg["individual_survival_reward"]
    individual_death_penalty = env_cfg["individual_death_penalty"]
    common_survival_reward = env_cfg["common_survival_reward"]
    common_death_penalty = env_cfg["common_death_penalty"]

    parameters["HORIZON"] = horizon
    parameters["TRAIN_HORIZON"] = horizon
    parameters["EVAL_HORIZON"] = horizon
    parameters["INDIVIDUAL_SURVIVAL_REWARD"] = individual_survival_reward
    parameters["INDIVIDUAL_DEATH_PENALTY"] = individual_death_penalty
    parameters["COMMON_SURVIVAL_REWARD"] = common_survival_reward
    parameters["COMMON_DEATH_PENALTY"] = common_death_penalty
    
    return parameters
