import csv, io, networkx, sys
import xml.etree.ElementTree as ElementTree
from matplotlib import pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

f = io.StringIO(''',peppers,cucumbers,celery,tomatoes,onions,spinach,lettuce,limes,lemons,pineapples,oranges,grapefruit,potatoes,cabbage,squash,corn,peas,beans,carrots,broccoli,avocados,bananas,apples,pears,peaches
peppers,3,,,,,,,,,,,,,,,,,,,,,,,,
cucumbers,3,3,,,,,,,,,,,,,,,,,,,,,,,
celery,3,3,3,,,,,,,,,,,,,,,,,,,,,,
tomatoes,3,3,2,3,,,,,,,,,,,,,,,,,,,,,
onions,1,,1,1,3,,,,,,,,,,,,,,,,,,,,
spinach,1,,,1,1,3,,,,,,,,,,,,,,,,,,,
lettuce,1,,1,1,1,2,3,,,,,,,,,,,,,,,,,,
limes,,,,,,,,3,,,,,,,,,,,,,,,,,
lemons,,,,,,,,3,3,,,,,,,,,,,,,,,,
pineapples,,,,,,,,1,1,3,,,,,,,,,,,,,,,
oranges,,,,,,,,1,1,1,3,,,,,,,,,,,,,,
grapefruit,,,,,,,,1,1,2,3,3,,,,,,,,,,,,,
potatoes,,,,,1,,,,,,,,3,,,,,,,,,,,,
cabbage,,,,,,1,1,,,,,,1,3,,,,,,,,,,,
squash,,,,,,1,,,,,,,1,,3,,,,,,,,,,
corn,1,,,1,1,1,,,,,,,,,2,3,,,,,,,,,
peas,2,1,1,1,1,1,1,,,,,,,,,1,3,,,,,,,,
beans,1,1,1,1,,,,,,,,,,,,,2,3,,,,,,,
carrots,2,1,1,1,1,1,,,,,,,,,,1,2,2,3,,,,,,
broccoli,2,1,1,1,1,1,1,,,,,,,,,1,3,2,3,3,,,,,
avocados,,,,,,,,,,1,,,,,,,,,,,3,,,,
bananas,,,,,,,,,,2,1,1,,,,,,,,,1,3,,,
apples,,,,,,,,,,1,,1,,,,,,,,,,2,3,,
pears,,,,,,,,,,1,,1,,,,,,,,,,2,2,3,
peaches,,,,,,,,,,1,,,,,,,,,,,,1,2,3,3
''')

cutoff = 0.5

if __name__=='__main__':
    reader = csv.reader(f)
    labels = next(reader)[1:]
    data = {}
    for l1 in labels:
        data[l1] = {}
        for l2 in labels:
            if l1 == l2:
                data[l1][l2] = 1.0
            else:
                data[l1][l2] = 0.0

    for a, row in enumerate(reader):
        for b, label in enumerate(labels):
            if row[b+1] != '':
                data[labels[a]][labels[b]] = float(row[b+1]) / 3.0
                data[labels[b]][labels[a]] = float(row[b+1]) / 3.0

    g = networkx.Graph()
    for a in range(len(labels)):
        g.add_node(labels[a])
        for b in range(a):
            if data[labels[a]][labels[b]] >= cutoff:
                g.add_edge(labels[a], labels[b])
                g.add_edge(labels[b], labels[a])

    pos = graphviz_layout(g, prog='neato')

    networkx.draw_networkx_nodes(g, pos, node_color='#ffffff')
    networkx.draw_networkx_labels(g, pos)
    networkx.draw_networkx_edges(g, pos)

    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.savefig('out.svg', bbox_inches='tight', edgecolor='w', facecolor='w', pad_inches=0)
    # the outline is ugly, and I'd like to change the font.
    
    # code to output a dendrogram. 
    #l = linkage(data, 'complete')
    #d = dendrogram(
    #    l,  
    #    above_threshold_color='k', 
    #    color_threshold=0, 
    #    labels=headings_1,
    #    orientation='left'
    #)   

    #plt.subplots_adjust(right=0.66)
    #plt.savefig('out2.svg')
