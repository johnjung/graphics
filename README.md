# Graphics

A collection of scripts for making diagrams and graphics. Most scripts produce
SVG output which can then be opened in software like Adobe Illustrator for
further editing.

## beer_flavor_wheel

Plot out a beer flavor wheel for further editing. This kind of diagram was first 
developed by M.C. Meilgaard in the 1970's to standardize the descriptive terms
brewers use for beer.

### Usage

```console
$ beer_flavor_wheel > wheel.svg
```

## two_by_two

A script to make attractive 2x2 diagrams. Accepts CSV data as input and
produces a SVG as output.

### Parameters

--x int
  place records horizontally using this field.
--xmin float
  records with this x value will be plotted at the left edge of the diagram.
--xmax float
  records with this x value will be plotted at the right edge of the diagram.
--y int
  place records vertically using this field.
--ymin float
  records with this x value will be plotted at the bottom edge of the diagram.
--ymax float
  records with this x value will be plotted at the top edge of the diagram.

### Example

```console
$ cat nutrition_information.csv | two_by_two --x=24 --y=25 - > two_by_two.svg
```

## update_thumbnails.sh

Resize a set of images to update thumbnails on a website. 

## venn

Produce proportionate venn diagrams, where the size of each circle and the
amount of overlap between circles accurately represents the amounts in each 
group.

## working with map data

A small python script to escape queries, deal with errors and get responses
back.

```python
endpoint = 'https://overpass.kumi.systems/api/interpreter'

try:
    response = urllib.request.urlopen(
        '{}?data={}'.format(
            endpoint,
            urllib.parse.quote(query)
        )
    )
except urllib.error.HTTPError as e:
    sys.stderr.write(str(e.code) + '\n')
    sys.stderr.write(str(e.headers) + '\n')
    sys.stderr.write(str(e.reason) + '\n')
    sys.exit()

sys.stdout.write(response.read().decode('utf-8'))
```

Get the number of relations in a bounding box. You can also get the number of
areas, nodes, and ways. nwr returns nodes, ways and relations all at once.

```console
[out:csv(::count)]
[bbox:41.7,-87.7,41.75,-87.65];
relation;
out count;
```

Get the names of relations in the bounding box. pipe the output of this
command into sort | uniq -c to get a report.

```console
[out:csv(name)]
[bbox:41.7,-87.7,41.75,-87.65];
relation;
out;
```

Get information about nodes named "Illinois".

```console
[out:csv(::id,::type,name)];
node[name="Illinois"];
out;
```

Get nodes for Illinois or Indiana.
```console
node[name~"(Illinois|Indiana)"][place="state"];
out;
```

Get a single relation.

```console
[out:csv(::id,name,::type,::count)]
[bbox:41.7,-87.7,41.75,-87.65];
relation[name="Mount Greenwood"];
out;
out count;
```

Get named nodes within 10km of South Holland. 

```console
[out:csv(::id,name,::type,::lat,::lon)]
[bbox:41,-88,42,-87];
node[name="South Holland"]->.south_holland;
(
    node[name](around.south_holland:10000);
);
out;
```

Get the latitude and longitude of South Holland. 

```console
[out:csv(::id,name,::type,::lat,::lon,::count)]
[maxsize:100]
[bbox:40,-90,43,-87];
(
    node[name="South Holland"];
);
out;
out count;
```

Get nodes near that latitude and longitude.

```console
[out:csv(::id,name,::type,::lat,::lon)]
[bbox:41,-88,42,-87];
node(around:100,41.587030,-87.582490);
out;
```

Get information about a single relation and all its pieces:

```console
[out:csv(::id,name,::type,::count)]
[bbox:41.7,-87.7,41.75,-87.65];
(
    relation[name="Mount Greenwood"];
    >;
);
out;
out count;
```

Get a list of bars in a bounding box. XML output can be opened in QGIS as
points on a map.

```console
[out:csv(::id,name,::type,::count)]
[bbox:41.7,-87.7,41.9,-87.5];
node["amenity"="bar"];
out;
```

Get information about roads in a bounding box.

```console
[out:csv(::id,name,::type,::count)]
[bbox:41.7,-87.7,41.9,-87.5];
(
    way["highway"];
    >;
);
out;
out count;
```

Get the roads themselves, in a format that I can open in QGIS:

```console
[bbox:41.7,-87.7,41.9,-87.5];
(
    way["highway"];
    >;
);
out;
```

Get I94. Note that this includes each lane separately. 

```console
[bbox:40,-89,43,-87];
(
    relation[name="I 94 (IL)"];
    >;
);
out;
```

Get "motorways" (highways like I94) in a bounding box. Note that each lane is
separate, but this is in a format that I can easily manipulate in QGIS. There
are also some parts of roads missing...I'll have to deal with that. 

```console
[bbox:40,-90,43,-87];
(
    way[highway~"(motorway|trunk)"];
    >;
);
out;
```

Get counties near Chicago.

```console
(
    (
        rel(122576);  // Cook County, IL
        rel(1800060); // DuPage County, IL
        rel(963483);  // Will County, IL
        rel(963485);  // Lake County, IN
    );
    >;
);
```

Get "motorways" (highways like I94) in a bounding box. Note that each lane is
separate, but this is in a format that I can easily manipulate in QGIS. There
are also some parts of roads missing...I'll have to deal with that. 

```console
[bbox:40,-90,43,-87];
(
    way[highway~"^(motorway|trunk)$"];
    >;
);
out;
```

Get the outline for Lake Michigan. 

```console
[out:csv(::id,name,::type,::count)]
[bbox:40,-90,43,-87];
(
    rel[name="Lake Michigan"];
    >;
);
out;
```

Get outlines for Illinois, Indiana and Michigan.

```console
(
    (
        rel[name="Michigan"];
        >;
    );
    (
        rel(122586);
        >;
    );
    (
        rel(161816);
        >;
    );
);
out;
```

Get the outline for Chicago.

```console
[bbox:40,-90,43,-87];
(
    (
        rel[place="city"][name="Chicago"];
        >;
    );
);
out;
```

Get neighborhoods (in Chicago). There are about 60 or so neighborhoods in
Chicago- but this list returns 500 nodes. I can easily "crop" the nodes to only
include things in Chicago, but what I actually want are a set of labels in the
city limits for neighborhoods that are a mix of large, well-populated,
well-known, and evenly spaced. Is that too much of a challenge? 

```console
[bbox:40,-90,43,-87];
node[place="neighbourhood"];
out;
```
