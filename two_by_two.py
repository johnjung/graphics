"""Usage:
   two_by_two (--x=<x>) [--xmin=<xmin>] [--xmax=<xmax>] (--y=<y>) [--ymin=<ymin>] [--ymax=<ymax>] -
"""

import csv
import sys
from docopt import docopt
import xml.etree.ElementTree as ElementTree


if __name__ == "__main__":
    arguments = docopt(__doc__)

    width = height = 612

    for a in ('--x', '--y'):
        arguments[a] = int(arguments[a])
    for a in ('--xmin', '--xmax', '--ymin', '--ymax'):
        if not arguments[a] == None:
            arguments[a] = float(arguments[a])

    reader = csv.reader(sys.stdin)
    next(reader)

    records = []
    for r in reader:
        if not any(r):
            break
        else:
            record = []
            for f in r:
                try:
                    record.append(float(f))
                except ValueError:
                    record.append(0.0)
            records.append(record)

    if arguments['--xmin'] == None:
        arguments['--xmin'] = min([float(r[arguments['--x']])
                                   for r in records])
    if arguments['--xmax'] == None:
        arguments['--xmax'] = max([float(r[arguments['--x']])
                                   for r in records])
    if arguments['--ymin'] == None:
        arguments['--ymin'] = min([float(r[arguments['--y']])
                                   for r in records])
    if arguments['--ymax'] == None:
        arguments['--ymax'] = max([float(r[arguments['--y']])
                                   for r in records])

    ElementTree.register_namespace('', 'http://www.w3.org/2000/svg')

    svg = ElementTree.Element(
        '{http://www.w3.org/2000/svg}svg',
        width='612',
        height='612',
        version='1.1'
    )

    # <style/>
    ElementTree.SubElement(
        svg,
        '{http://www.w3.org/2000/svg}style'
    ).text = 'text { font-family: Helvetica, sans-serif; font-size: 12px; }'

    # <rect/>
    ElementTree.SubElement(
        svg,
        '{http://www.w3.org/2000/svg}rect',
        attrib={
            'fill':   '#f3f3f3',
            'width':  '612',
            'height': '612',
            'x':      '0',
            'y':      '0'
        }
    )

    # <circle/>
    for r in records:
        x = (r[arguments['--x']] - arguments['--xmin']) / \
            (arguments['--xmax'] - arguments['--xmin']) * width
        y = (r[arguments['--y']] - arguments['--ymin']) / \
            (arguments['--ymax'] - arguments['--ymin']) * height
        ElementTree.SubElement(
            svg,
            '{http://www.w3.org/2000/svg}circle',
            attrib={
                'fill':   'black',
                'cx':      str(x),
                'cy':      str(height - y),
                'r':      '2'
            }
        )

    print(ElementTree.tostring(svg, encoding='utf8', method='xml').decode('UTF-8'))
