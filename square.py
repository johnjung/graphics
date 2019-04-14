import xml.etree.ElementTree as ElementTree

#
# variables
#

output_width = 100
output_height = 100

set_a_size = 1000
set_b_size = 1150
intersection_size = 950

#
# main
#

svg = ElementTree.Element(
    'svg',
    width=str(output_width),
    height=str(output_height),
    version='1.1'
)

a_width = output_width / 2
a_height = output_height / 2
a_x = 0
a_y = output_height - a_height

ElementTree.SubElement(
    svg,
    'rect',
    fill='none',
    stroke='black',
    x=str(a_x),
    y=str(a_y),
    width=str(a_width),
    height=str(a_height)
)

b_width = a_width
b_height = set_b_size / set_a_size * a_height
b_x = a_width - (intersection_size / min((set_a_size, set_b_size)) * a_width)
b_y = output_height - b_height

ElementTree.SubElement(
    svg,
    'rect',
    fill='none',
    stroke='black',
    x=str(b_x),
    y=str(b_y),
    width=str(b_width),
    height=str(b_height)
)

print(ElementTree.tostring(svg).decode('utf-8'))
