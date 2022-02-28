import json
from shapely.geometry import LineString, Polygon


"""generate simple polygon for terrace,
given original coordinates of store front"""


def generate_terrace(left_xy, right_xy, width, length, buffer,
                         orientation_terrace):
    """generate polygon for door given front of store

    Args:
        left_xy (dict): left point of store front xy coordinates
        right_xy (dict): right point of store front xy coordinates
        width (float): width of terrace in percentage of store front
        length (float): the length of the terrace in meter
        buffer (float): the distance between the terrace
                        and the store, in meters
        orientation_terrace (str): 'left' or 'right' depending on
                            orientation of the store
    """

    # load template obstacle polygon with 4 coordinates
    with open('../input/files/vadere_templates/obstacle.json', 'r') as file:
        obstacle = json.load(file)

    # generate new front coordinates for door
    store_front = LineString([(left_xy['x'], left_xy['y']),
                              (right_xy['x'], right_xy['y'])])
    center = store_front.interpolate(0.5, normalized=True)
    left_to_center = LineString([(left_xy['x'], left_xy['y']),
                                 (center.x, center.y)])
    center_to_right = LineString([(center.x, center.y),
                                  (right_xy['x'], right_xy['y'])])
    terrace_left = left_to_center.interpolate((1 - width) / 2, normalized=True)
    terrace_right = center_to_right.interpolate(1 - (1 - width) / 2, normalized=True)
    terrace_left_xy = (terrace_left.x, terrace_left.y)
    terrace_right_xy = (terrace_right.x, terrace_right.y)

    # get perpendicular line for new coordinates
    front = LineString([terrace_left_xy, terrace_right_xy])
    if orientation_terrace == 'left':
        right_par = front.parallel_offset(length + buffer, 'left')
        left_par = front.parallel_offset(buffer, 'left')
    elif orientation_terrace == 'right':
        left_par = front.parallel_offset(length + buffer, 'right')
        right_par = front.parallel_offset(buffer, 'right')
    else:
        raise ValueError('please provide a valid orientation (left or right)')

    # replace id and coordinates in template
    obstacle['id'] = id
    obstacle['shape']['points'][0]['x'] = right_par.boundary.geoms[0].x
    obstacle['shape']['points'][0]['y'] = right_par.boundary.geoms[0].y
    obstacle['shape']['points'][1]['x'] = right_par.boundary.geoms[1].x
    obstacle['shape']['points'][1]['y'] = right_par.boundary.geoms[1].y
    obstacle['shape']['points'][2]['x'] = left_par.boundary.geoms[1].x
    obstacle['shape']['points'][2]['y'] = left_par.boundary.geoms[1].y
    obstacle['shape']['points'][3]['x'] = left_par.boundary.geoms[0].x
    obstacle['shape']['points'][3]['y'] = left_par.boundary.geoms[0].y

    # save object in json format suitable for Vadere
    with open('../output/data_prep/tarrace/terrace_{}.json'.format(id), 'w') as file:
        json.dump(obstacle, file)

    # report on polygon area
    poly = Polygon([
        [right_par.boundary.geoms[0].x, right_par.boundary.geoms[0].y],
        [right_par.boundary.geoms[1].x, right_par.boundary.geoms[1].y],
        [left_par.boundary.geoms[0].x, left_par.boundary.geoms[0].y],
        [left_par.boundary.geoms[0].x, left_par.boundary.geoms[0].y],
    ])
    print('area of created polygon is {} square meters'.format(poly.area))
    with open('../output/data_prep/tarrace/terrace_area_{}.txt'.format(id), 'w') as file:
        file.write(
            'area of created polygon is {} square meters \n \
used store coordinates are \n \
left: {} \n \
right: {} \n \
length: {}'.format(poly.area, left_xy, right_xy, length)) 


if __name__ == '__main__':
    left_xy = {
        'x': 76.06078211113345, 'y': 43.76113685965538
    }
    right_xy = {
        'x': 100.1654009076301, 'y': 51.83540345635265
    }
    width = 1
    length = 6
    id = 8005
    buffer = 1.5
    orientation_terrace = 'left'
    generate_terrace(left_xy, right_xy, width, length, buffer,
                         orientation_terrace)
