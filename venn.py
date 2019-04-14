import math
import sys

import xml.etree.ElementTree as ElementTree

from trianglesolver import solve


def get_area(radius):
    return math.pi * math.pow(radius, 2)


def get_radius(area):
    return math.sqrt(area / math.pi)


def get_segment_area(radius, radians):
    degrees = (180 / math.pi) * radians

    area_of_sector = math.pi * \
        (radius * radius) * \
        (degrees / 360)

    area_of_triangle = 0.5 * \
        (radius * radius) * \
        math.sin((degrees * math.pi) / 180)

    return area_of_sector - area_of_triangle


def get_overlap_area(radius_a, radius_b, distance):
    ''' 
       radius_a, radius_b and distance form a triangle: a, b, c. 
    '''

    if distance <= abs(radius_a - radius_b):
        return get_area(min(radius_a, radius_b))
    if distance >= radius_a + radius_b:
        return 0.0
    else:
        _, _, _, A, B, _ = solve(a=radius_a, b=radius_b, c=distance)
        return get_segment_area(radius_a, B * 2) + get_segment_area(radius_b, A * 2)


def get_lookup_table(radius_a, radius_b, steps):
    start_distance = abs(radius_a - radius_b)
    stop_distance = radius_a + radius_b
    step_size = (stop_distance - start_distance) / steps

    offsets = []
    s = 0
    while s <= steps:
        distance = start_distance + (step_size * s)
        overlap_area = get_overlap_area(radius_a, radius_b, distance)
        smaller_area = get_area(min(radius_a, radius_b))
        offsets.append((overlap_area / smaller_area, distance))
        s = s + 1
    return offsets

#
# MAIN
#


chart_width = 576
chart_height = 288

area_a = 14000
area_b = 12800
# overlap as a percentage of circle b.
overlap = 0.97

radius_a = get_radius(area_a)
radius_b = get_radius(area_b)

offsets = get_lookup_table(radius_a, radius_b, 100)
overlap_found, distance = min(offsets, key=lambda x: abs(x[0] - overlap))

illustration_width = radius_a + distance + radius_b

ElementTree.register_namespace('', 'http://www.w3.org/2000/svg')

svg = ElementTree.Element(
    '{http://www.w3.org/2000/svg}svg',
    width=str(chart_width),
    height=str(chart_height),
    version='1.1'
)

ElementTree.SubElement(
    svg,
    '{http://www.w3.org/2000/svg}circle',
    cx=str(((chart_width - illustration_width) / 2) + radius_a),
    cy=str(chart_height / 2),
    r=str(radius_a),
    fill='none',
    stroke='black',
    width='3',
)

ElementTree.SubElement(
    svg,
    '{http://www.w3.org/2000/svg}circle',
    cx=str(((chart_width + illustration_width) / 2) - radius_b),
    cy=str(chart_height / 2),
    r=str(radius_b),
    fill='none',
    stroke='black',
    width='3'
)

print(ElementTree.tostring(svg, encoding='utf8', method='xml').decode('UTF-8'))
