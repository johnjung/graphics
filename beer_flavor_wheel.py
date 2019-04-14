import xml.etree.ElementTree as ElementTree

flavors = (
    ("Spicy",),
    ("Vinous",),
    ("Plastics",),
    ("Can-liner",),
    ("Laquer-like",),
    ("Isoamyl acetate",    "banana"),
    ("Ethyl hexanoate",    "apple or aniseed"),
    ("Ethyl acetate",      "fruity or pear-like in low amounts, solvent-like in high amounts"),
    ("Citrus",),
    ("Apple",),
    ("Banana",),
    ("Black currant",),
    ("Melony",),
    ("Pear",),
    ("Raspberry",),
    ("Strawberry",),
    ("Acetaldehyde",       "green apple"),
    ("2-Phenylethanol",    "initially slightly bitter then sweet and reminiscent of peach"),
    ("Geraniol",           "roses, floral, or citrus fruit"),
    ("Perfumy",),
    ("Kettle-hop",         "grassy, plantlike and green"),
    ("Dry-hop",            "citrusy, floral, minty, tropical or berrylike"),
    ("Hop oil",),
    ("Piney",),
    ("Woody",),
    ("Walnut",),
    ("Coconut",),
    ("Beany",),
    ("Almond",),
    ("Freshly cut grass",),
    ("Straw-like",),
    ("Husky",),
    ("Corn grits",),
    ("Mealy",),
    ("Malty",),
    ("Worty",),
    ("Molasses",),
    ("Licorice",),
    ("Bread crust",),
    ("Roast barley",),
    ("Smoky",),
    ("Tarry",              "a tarred road"),
    ("Bakelite",           "paint remover or varnish"),
    ("Carbolic",           "charcoal"),
    ("Chlorophenol",       "cardboard"),
    ("Iodoform",           "hospital smell"),
    ("Caprylic",           "goat hair or candle wax"),
    ("Cheesy",),
    ("Isovaleric",         "gym socks"),
    ("Butyric",            "baby vomit"),
    ("Diacetyl",           "artificial butter or butterscotch"),
    ("Rancid",),
    ("Vegetable oil",),
    ("Mineral oil",),
    ("Striking match",),
    ("Meaty",),
    ("Hydrogen Sulfide",   "sulphur"),
    ("Mercaptan",          "sulphuric and skunky"),
    ("Garlic",),
    ("Lightstruck",        "skunky"),
    ("Autolysed",          "meaty"),
    ("Burnt rubber",),
    ("Shrimp-like",),
    ("Parsnip/Celery",),
    ("Dimethyl sulfide",   "corn"),
    ("Cooked cabbage",),
    ("Cooked sweet corn",),
    ("Cooked tomato",),
    ("Cooked onion",),
    ("Yeasty",),
    ("Catty",              "cat urine"),
    ("Papery",),
    ("Leathery",),
    ("Earthy",),
    ("Musty",),
    ("Acetic",),
    ("Sour",),
    ("Honey",),
    ("Jam-like",),
    ("Vanilla",),
    ("Primings",           "sugar"),
    ("Syrupy",),
    ("Oversweet",),
    ("Salty",),
    ("Bitter",),
    ("Alkaline",           "pennies"),
    ("Mouthcoating",),
    ("Metallic",),
    ("Drying",),
    ("Tart",),
    ("Puckering",),
    ("Powdery",),
    ("Flat",),
    ("Gassy",),
    ("Alcoholic",),
    ("Piquant",),
    ("Watery",),
    ("Characterless",),
    ("Satiating",),
    ("Thick",)
)


if __name__ == "__main__":
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

    for i, f in enumerate(flavors):
        if i >= 26 and i < 76:
            anchor = 'start'
            transform = 'rotate({} 306 306) translate(-200 0) rotate(180.0 306 306)'.format(i * 3.6)
        else:
            anchor = 'end'
            transform = 'rotate({} 306 306) translate(-200 0)'.format(i * 3.6)

        # <text/>
        ElementTree.SubElement(
            svg,
            '{http://www.w3.org/2000/svg}text',
            attrib={
                'alignment-baseline': 'middle',
                'dominant-baseline':  'middle',
                'text-anchor':        anchor,
                'x':                  '306',
                'y':                  '306',
                'transform':          transform
            }
        ).text = f[0]

    print(ElementTree.tostring(svg, encoding='utf8', method='xml').decode('UTF-8'))
