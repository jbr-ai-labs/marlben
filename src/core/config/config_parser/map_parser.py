from src.core.map_generator import CustomMapGenerator



def parse_map_configuration(map_cfg):
    parameters = {}
    
    height = map_cfg['height']
    width = map_cfg['width']
    larger_side = max(height, width)
    # the center part of the map will be h x w, 
    # with one lava layer and one rock layer surrounding the center
    # the rock layer is required to prevent the agent from leaving the center
    center = larger_side + 4

    # the border needs to be at least max(h, w) - 1
    # if nstim will be equal to max(h, w), 
    # the agent needs to be able to look over the rock border
    border = larger_side - 1
    # now it is possible for the agent to see the entire map
    nstim = map_cfg.get('nstim', larger_side)
    nstim = min(nstim, larger_side)

    # top left corner of the main part of the map is at least at point 
    # (larger_side + 2, larger_side + 2)
    top_left_corner = [larger_side + 2, larger_side + 2]
    if height > width:
        top_left_corner[1] += larger_side // 2
    elif height < width:
        top_left_corner[0] += larger_side // 2

    parameters["FORCE_MAP_GENERATION"] = False
    parameters["TERRAIN_CENTER"] = center
    parameters["TERRAIN_BORDER"] = border
    parameters["NSTIM"] = nstim
    parameters["MAP_HEIGHT"] = height
    parameters["MAP_WIDTH"] = width
    parameters["TOP_LEFT_CORNER"] = top_left_corner
    parameters["MAP_GENERATOR"] = CustomMapGenerator
    parameters["GENERATE_MAP_PREVIEWS"] = False

    return parameters
