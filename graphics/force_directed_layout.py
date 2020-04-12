#!/usr/bin/env python

import csv, math, numpy, random, sys
import xml.etree.ElementTree as ElementTree

random.seed(44) # for testing

def vector_to_distance(v):
    """ start of vector is at 0, 0 """
    return math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))

def scale_vector(v, s):
    return numpy.array((v[0] * s, v[1] * s))

def spring_force(v):
    c1 = 25.0 # a constant
    c2 = 1.0 # a constant
    d = vector_to_distance(v)
    force = c1 * math.log2(d / c2)

    return scale_vector(v, 1.0 / d)

def repel_force(v):
    """ Returns the amount of repelling force at a certain distance.

    params: v (numpy.array), the y, x coordinates for a vector starting at 0, 0
    """
    c3 = 25.0 # a constant
    d = vector_to_distance(v)
    force = -1.0 * c3 / math.pow(d, 2)

    return scale_vector(v, force)

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


if __name__=='__main__':
    width = 612
    height = 612

    # load matrix.
    mat = []
    with open('fruits.csv') as f:
        reader = csv.reader(f)
        headers = next(reader)[1:]
        for row in reader:
            mat.append(row[1:])

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
        for b in range(y):
            if mat[a][b] <= 1:
                 edges.append((a, b))

    rounds = 0
    while rounds < 10:
        new_nodes = []
        for n in range(len(nodes)):
            new_nodes.append(
                numpy.sum(
                    [
                        nodes[n],
                        calculate_forces_on_a_node(
                            nodes[:n] + nodes[n+1:], 
                            nodes[n], 
                            spring_force
                        )
                    ],
                    0
                )
            )
        nodes = new_nodes
        rounds += 1


    # SVG output.
    ElementTree.register_namespace('', 'http://www.w3.org/2000/svg')

    svg = ElementTree.Element(
        '{http://www.w3.org/2000/svg}svg',
        width=str(width + 100),
        height=str(height),
        version='1.1'
    )

    # <style/>
    ElementTree.SubElement(
        svg,
        '{http://www.w3.org/2000/svg}style'
    ).text = 'text { font-family: Helvetica, sans-serif; font-size: 12px; }'

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

    print(ElementTree.tostring(svg, encoding='utf8', method='xml').decode('UTF-8'))
