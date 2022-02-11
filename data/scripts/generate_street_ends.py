import json
from shapely.geometry import LineString, Polygon


"""generate simple polygon for street ends,
given coordinates of enclosing buildings"""


def generate_street_end(building_1_end_xy, building_1_start_xy,
                        building_2_end_xy, building_2_start_xy, id, type_object):
    """generate polygon for street end

    Args:
        building_1_end_xy ([type]): end point of building enclosings
        building_1_start_xy ([type]): start point of building enclosings
                                    - NOTE: start means at the street side,
                                    in the directions pedestrains will walk
        building_2_end_xy ([type]): end point of building enclosings
        building_2_start_xy ([type]): start point of building enclosings
                                    - NOTE: start means at the street side,
                                    in the directions pedestrains will walk
        id (int): id to give to generated object
        type_object (str): 'target', 'source' or 'target_changer'
    """

    # load template object polygon with 4 coordinates
    match (type_object):
        case 'target':
            with open('../input/files/vadere_templates/target.json', 'r') as file:
                object = json.load(file)
        case 'source':
            with open('../input/files/vadere_templates/source.json', 'r') as file:
                object = json.load(file)
        case 'target_changer':
            with open('../input/files/vadere_templates/target_changer.json', 'r') as file:
                object = json.load(file)

    # generate enclosing lines
    enc_line_start = LineString([(building_1_start_xy['x'], building_1_start_xy['y']),
                                 (building_2_start_xy['x'], building_2_start_xy['y'])])
    enc_line_end = LineString([(building_1_end_xy['x'], building_1_end_xy['y']),
                               (building_2_end_xy['x'], building_2_end_xy['y'])])

    # get area by removing 1% at begin and end of enclosing lines
    # so that area does not overlap with Vadere obstacle
    area_1_x = enc_line_start.interpolate(0.01, normalized=True).x
    area_1_y = enc_line_start.interpolate(0.01, normalized=True).y
    area_2_x = enc_line_end.interpolate(0.01, normalized=True).x
    area_2_y = enc_line_end.interpolate(0.01, normalized=True).y
    area_3_x = enc_line_end.interpolate(0.99, normalized=True).x
    area_3_y = enc_line_end.interpolate(0.99, normalized=True).y
    area_4_x = enc_line_start.interpolate(0.99, normalized=True).x
    area_4_y = enc_line_start.interpolate(0.99, normalized=True).y

    # replace id and coordinates in template
    object['id'] = id
    object['shape']['points'][0]['x'] = area_1_x
    object['shape']['points'][0]['y'] = area_1_y
    object['shape']['points'][1]['x'] = area_2_x
    object['shape']['points'][1]['y'] = area_2_y
    object['shape']['points'][2]['x'] = area_3_x
    object['shape']['points'][2]['y'] = area_3_y
    object['shape']['points'][3]['x'] = area_4_x
    object['shape']['points'][3]['y'] = area_4_y

    # save object in json format suitable for Vadere
    with open('../output/data_prep/street_ends/street_end_{}.json'.format(id), 'w') as file:
        json.dump(object, file)

    # report on polygon area
    poly = Polygon([
        [area_1_x, area_1_y],
        [area_2_x, area_2_y],
        [area_3_x, area_3_y],
        [area_4_x, area_4_y],
    ])
    print('area of created polygon is {} square meters'.format(poly.area))
    with open('../output/data_prep/street_ends/targetstreet_end_{}.txt'.format(id), 'w') as file:
        file.write(
            'area of created polygon is {} square meters'.format(poly.area))


if __name__ == '__main__':
    building_1_end_xy = {
        "x" : 114.78818151867017,
        "y" : 72.16359547525644
    }
    building_1_start_xy = {
        "x" : 108.59207844967023,
        "y" : 70.72224595956504
    }
    building_2_end_xy = {
        "x" : 116.32390714494977,
        "y" : 57.74714249651879
    }
    building_2_start_xy = {
        "x" : 109.90030781121459,
        "y" : 55.39898575376719
    }
    type_object = 'target_changer'
    id = 6004
    generate_street_end(building_1_end_xy, building_1_start_xy,
                        building_2_end_xy, building_2_start_xy, id,
                        type_object)
