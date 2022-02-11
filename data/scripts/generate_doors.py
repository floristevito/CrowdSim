import json
from shapely.geometry import LineString, Polygon


"""generate simple polygon for store doors,
given original coordiantes of store front"""


def generate_door_target(left_xy, right_xy, width, length,
                         orientation_door):
    """generate polygon for door given front of store

    Args:
        left_xy (dict): left point of store front xy coordinates
        right_xy (dict): right point of store front xy coordinates
        width (float): width of door in meter
        length (float): the height of the door in meter
        offset (float): the amount of meter the door
                        comes out of the store obstacle
        orientation_door (str): 'left' or 'right' depending on
                            orientation of the store
    """

    # load template target polygon with 4 coordinates
    with open('../input/files/vadere_templates/target.json', 'r') as file:
        target = json.load(file)

    # generate new front coordinates for door
    store_front = LineString([(left_xy['x'], left_xy['y']),
                              (right_xy['x'], right_xy['y'])])
    center = store_front.interpolate(0.5, normalized=True)
    left_to_center = LineString([(left_xy['x'], left_xy['y']),
                                 (center.x, center.y)])
    center_to_right = LineString([(center.x, center.y),
                                  (right_xy['x'], right_xy['y'])])
    door_left = left_to_center.interpolate(store_front.length / 2 - width / 2)
    door_right = center_to_right.interpolate(width / 2)
    door_left_xy = (door_left.x, door_left.y)
    door_right_xy = (door_right.x, door_right.y)

    # get perpendicular line for new coordinates
    front = LineString([door_left_xy, door_right_xy])
    if orientation_door == 'left':
        right_par = front.parallel_offset(length - 0.01, 'left')
        left_par = front.parallel_offset(0.01, 'left')
    elif orientation_door == 'right':
        left_par = front.parallel_offset(length - 0.01, 'right')
        right_par = front.parallel_offset(0.01, 'right')
    else:
        raise ValueError('please provide a valid orientation (left or right)')

    # replace id and coordinates in template
    target['id'] = id
    target['shape']['points'][0]['x'] = right_par.boundary.geoms[0].x
    target['shape']['points'][0]['y'] = right_par.boundary.geoms[0].y
    target['shape']['points'][1]['x'] = right_par.boundary.geoms[1].x
    target['shape']['points'][1]['y'] = right_par.boundary.geoms[1].y
    target['shape']['points'][2]['x'] = left_par.boundary.geoms[1].x
    target['shape']['points'][2]['y'] = left_par.boundary.geoms[1].y
    target['shape']['points'][3]['x'] = left_par.boundary.geoms[0].x
    target['shape']['points'][3]['y'] = left_par.boundary.geoms[0].y

    # save object in json format suitable for Vadere
    with open('../output/data_prep/store_targets/store_target_{}.json'.format(id), 'w') as file:
        json.dump(target, file)

    # report on polygon area
    poly = Polygon([
        [right_par.boundary.geoms[0].x, right_par.boundary.geoms[0].y],
        [right_par.boundary.geoms[1].x, right_par.boundary.geoms[1].y],
        [left_par.boundary.geoms[0].x, left_par.boundary.geoms[0].y],
        [left_par.boundary.geoms[0].x, left_par.boundary.geoms[0].y],
    ])
    print('area of created polygon is {} square meters'.format(poly.area))
    with open('../output/data_prep/store_targets/store_target_area_{}.txt'.format(id), 'w') as file:
        file.write(
            'area of created polygon is {} square meters \n \
used store coordinates are \n \
left: {} \n \
right: {}'.format(poly.area, left_xy, right_xy))


if __name__ == '__main__':
    left_xy = {
        "x" : 68.80787601287011,
        "y" : 85.2326849270612
    }
    right_xy = {
        "x" : 66.86139745032415,
        "y" : 89.7473910190165
    }
    width = 3
    length = 1
    id = 2026
    orientation_door = 'left'
    generate_door_target(left_xy, right_xy, width, length,
                         orientation_door)
