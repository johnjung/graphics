#!/usr/bin/env python

import csv, math, numpy, random, sys
import xml.etree.ElementTree as ElementTree

# random.seed(44) # for testing

def setup_svg(width, height):
    # SVG output.
    ElementTree.register_namespace('', 'http://www.w3.org/2000/svg')

    svg = ElementTree.Element(
        '{http://www.w3.org/2000/svg}svg',
        width=str(width),
        height=str(height),
        version='1.1'
    )

    # <style/>
    ElementTree.SubElement(
        svg,
        '{http://www.w3.org/2000/svg}style'
    ).text = 'text { font-family: Helvetica, sans-serif; font-size: 12px; }'

    # <defs><marker><path/>
    ElementTree.SubElement(
        ElementTree.SubElement(
            ElementTree.SubElement(
                svg,
                '{http://www.w3.org/2000/svg}defs'
            ),
            '{http://www.w3.org/2000/svg}marker',
            attrib={
                'id': 'arrow',
                'markerHeight': '10',
                'markerWidth': '10',
                'markerUnits': 'strokeWidth',
                'orient': 'auto',
                'refX': '0',
                'refY': '3'
            }
        ),
        '{http://www.w3.org/2000/svg}path',
        attrib={
            'd': 'M0,0 L0,6 L9,3 z',
            'fill': 'black'
        },
    )
    return svg

def add_nodes_to_svg(svg, nodes):
    for i, n in enumerate(nodes):
        # <circle/>
        ElementTree.SubElement(
            svg,
            '{http://www.w3.org/2000/svg}circle',
            attrib={
                'fill':   '#ff0000',
                'cx':     str(n[1]),
                'cy':     str(n[0]),
                'r':      '5'
            }
        )
        # <text/>
        ElementTree.SubElement(
            svg,
            '{http://www.w3.org/2000/svg}text',
            attrib={
                'alignment-baseline': 'middle',
                'dominant-baseline':  'middle',
                'x':                  str(n[1] + 10),
                'y':                  str(n[0])
            }
        ).text = headers[i]

def vector_to_distance(v):
    """ start of vector is at 0, 0 """
    return math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))

def scale_vector(v, s):
    return numpy.array((v[0] * s, v[1] * s))

def gravity_force(v):
    c3 = 5.0 # a constant
    d = vector_to_distance(v)
    force = c3 / math.pow(d, 2)

    return scale_vector(v, force)

def repel_force(v):
    """ Returns the amount of repelling force at a certain distance.

    params: v (numpy.array), the y, x coordinates for a vector starting at 0, 0
    """
    c3 = 25.0 # a constant
    d = vector_to_distance(v)
    force = -1.0 * c3 / math.pow(d, 2)

    return scale_vector(v, force)

def get_force_delta_list(nodes, node, force):
    """ Get a list of "force deltas", e.g. for a line from 4, 1 to 6, 3, the
        delta is 2, 2.

    If you're pulling the parameters from a list of nodes, you can call it
    like: ...(nodes[:2] + nodes[3:], nodes[2])
 
    params: nodes (list), a list of node Arrays
            node (Array), x,y coordinates for the node we're calculating forces
            on.
            force (function), a function like spring_force() or repel_force(),
            that takes a distance and returns a new distance. 
    """
    return [force(numpy.subtract(n, node)) for n in nodes]

def calculate_forces_on_a_node(nodes, node, force):
    """ Calculate the total amount of repelling force on a node.

    Center the node we're working with at 0, 0 and then build a list of vectors
    to all other nodes that have been scaled by a repelling force. Sum all of
    those vectors together and return the result.

    If you're pulling the parameters from a list of nodes, you can call it
    like: ...(nodes[:2] + nodes[3:], nodes[2])
 
    params: nodes (list), a list of node Arrays
            node (Array), x,y coordinates for the node we're calculating forces
            on.
            force (function), a function like spring_force() or repel_force(),
            that takes a distance and returns a new distance. 
    """
    return numpy.sum([force(numpy.subtract(n, node)) for n in nodes], 0)

def get_connected_nodes(edges, n):
    nodes = set()
    for e in edges:
        if e[0] == n:
            nodes.add(e[1])
    return list(nodes)

if __name__=='__main__':
    width = 612
    height = 612

    svg = setup_svg(width, height)

    # load matrix.
    mat = []
    with open('fruits.csv') as f:
        reader = csv.reader(f)
        headers = next(reader)[1:]
        for row in reader:
            mat.append(row[1:])

    # jej
    headers = headers[:2]

    # fill in the upper triangle and convert to integers.
    for y in range(len(mat)):
        for x in range(y):
            mat[x][y] = mat[y][x] = int(mat[y][x])
        mat[y][y] = int(mat[y][y])

    # every node gets a random position in 2d space. 
    nodes = []
    for i in range(len(headers)):
        nodes.append([random.random() * height, random.random() * width])

    # if the node is at a certain cutoff create an edge.
    edges = []
    for a in range(len(headers)):
        for b in range(a):
            if mat[a][b] <= 1:
                 edges.append((a, b))

    # add a <circle/> for each node. 
    add_nodes_to_svg(svg, nodes)

    rounds = 0
    while rounds < 10000:
        new_nodes = []
        for n in range(len(nodes)):
            repel_forces = calculate_forces_on_a_node(
                nodes[:n] + nodes[n+1:], 
                nodes[n], 
                repel_force
            )

            gravity_forces = calculate_forces_on_a_node(
                [nodes[i] for i in get_connected_nodes(edges, n)],
                nodes[n],
                gravity_force
            )

            print(type(gravity_forces))
            sys.exit()

            # <line/>
            if rounds % 100 == 0:
                ElementTree.SubElement(
                    svg,
                    '{http://www.w3.org/2000/svg}line',
                    attrib={
                        'marker-end':   'url(#arrow)',
                        'stroke':       'black',
                        'stroke-width': '1',
                        'x1':           str(nodes[n][1]),
                        'y1':           str(nodes[n][0]),
                        'x2':           str(nodes[n][1] + gravity_forces[1]),
                        'y2':           str(nodes[n][0] + gravity_forces[0])
                    }
                )

            new_nodes.append(
                numpy.sum(
                    [
                        nodes[n],
                        gravity_forces
                    ],
                    0
                )
            )
        nodes = new_nodes
        rounds += 1

    print(ElementTree.tostring(svg, encoding='utf8', method='xml').decode('UTF-8'))
