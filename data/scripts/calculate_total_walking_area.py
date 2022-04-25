import json
from shapely.geometry import LineString, Polygon


if __name__ == '__main__':
    # open measurement area from Vadere
    with open('../input/files/total_walking_area.json') as file:
        area = json.load(file)

    # create shapely polygon
    poly = Polygon([[point['x'], point['y']] for point in area['shape']['points']])

    # calculate area with shapely area function -> units are in meter (cartesian points)
    print('area in square meters is: {}'.format(poly.area))