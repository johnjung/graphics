import math
import venn

assert math.isclose(venn.get_area(2), math.pi * math.pow(2, 2))

assert math.isclose(venn.get_radius(math.pi * math.pow(2, 2)), 2)

'''
   when the sector is an infinitely thin pie slice, the area is 0.
   when the sector is the entire pie, the area is the same as the circle area.
'''
assert math.isclose(venn.get_sector_area(2, 0), 0)

assert math.isclose(venn.get_sector_area(
    2, math.pi * 0.5), venn.get_area(2) * .25)

assert math.isclose(venn.get_sector_area(2, math.pi), venn.get_area(2) * 0.5)

assert math.isclose(venn.get_sector_area(
    2, math.pi * 1.5), venn.get_area(2) * .75)

assert math.isclose(venn.get_sector_area(2, math.pi * 2), venn.get_area(2))

'''
   get the opposite side of a right triangle, given a hypotenuse and an angle
   in radians.
'''
assert math.isclose(venn.get_triangle_opposite(1, 0.0), 0)

assert math.isclose(venn.get_triangle_opposite(
    1, math.pi * 0.4999), 1.0, rel_tol=1e-02)

assert math.isclose(venn.get_chord_length(5, 0.823), 4, rel_tol=1e-02)

'''
   get triangle height
'''
assert math.isclose(venn.get_triangle_height(5, 1.288), 4, rel_tol=1e-02)

assert math.isclose(venn.get_triangle_height(5, 1.854), 3, rel_tol=1e-02)

assert math.isclose(venn.get_triangle_area(5, 1.288), 12, rel_tol=1e-02)

''' 
   get the segment area for a half circle.
'''
assert math.isclose(venn.get_segment_area(5, math.pi * 0.9999),
                    math.pi * math.pow(5, 2) / 2, rel_tol=1e-02)

assert math.isclose(venn.get_segment_area(5, 1.288),
                    venn.get_sector_area(5, 1.288) - 12, rel_tol=1e-02)

assert math.isclose(venn.get_segment_area_from_offset(5, 5), 0)

assert math.isclose(venn.get_segment_area_from_offset(
    5, 4.999), 0.0, abs_tol=.01)

assert math.isclose(venn.get_segment_area_from_offset(
    5, 0), math.pi * math.pow(5, 2) / 2)

assert math.isclose(venn.get_segment_area_from_offset(
    5, -4.999), math.pi * math.pow(5, 2), rel_tol=1e-02)

'''
   get radians from the radius and the offset.
'''
assert math.isclose(venn.get_radians_from_radius_and_offset(
    5, 0.00001), math.pi / 2, rel_tol=1e-02)

assert math.isclose(venn.get_radians_from_radius_and_offset(
    5, 4.99999), 0.0, abs_tol=0.01)

venn.get_radians_from_radius_and_offset(5, math.sin(math.pi / 4)),

assert math.isclose(venn.get_overlap_area(5, 5, 0), math.pi * math.pow(5, 2))

assert math.isclose(venn.get_overlap_area(5, 5, 10), 0)
