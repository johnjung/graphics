import math
import unittest

'''
get_area(2) == math.pi * math.pow(2, 2)
2 == get_radius(math.pi * math.pow(2, 2))
0 == get_sector_area(2, 0)
get_sector_area(2, math.pi * 0.5) == get_area(2) * .25
get_sector_area(2, math.pi) == get_area(2) * 0.5
get_sector_area(2, math.pi * 1.5) == get_area(2) * .75
get_sector_area(2, math.pi * 2) == get_area(2)
0 == get_triangle_opposite(1, 0.0)
1.0 == get_triangle_opposite(1, math.pi * 0.4999)
4 == get_chord_length(5, 0.823)
4 == get_triangle_height(5, 1.288)
3 == get_triangle_height(5, 1.854)
12 == get_triangle_area(5, 1.288)
get_segment_area(5, math.pi * 0.9999), math.pi * math.pow(5, 2) / 2
get_segment_area(5, 1.288), get_sector_area(5, 1.288) - 12
0 == get_segment_area_from_offset(5, 5)
0 == get_segment_area_from_offset(5, 4.999)
get_segment_area_from_offset(5, 0) == math.pi * math.pow(5, 2) / 2
get_segment_area_from_offset(5, -4.999) == math.pi * math.pow(5, 2)
get_radians_from_radius_and_offset(5, 0.00001) == math.pi / 2
0 == get_radians_from_radius_and_offset(5, 4.99999)
get_overlap_area(5, 5, 0) == math.pi * math.pow(5, 2)
0 == get_overlap_area(5, 5, 10)
'''

class TestVenn(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for a, b, c in ((7, 8, 9), (5, 6, 10), (5, 10, 6), (10, 5, 6), (5, 12, 13),
                        (12, 5, 13), (12, 13, 5)):
    def floats_are_equal(x, y):
        return abs(x - y) <= 100 * EPSILON * (abs(x) + abs(y))
    
    def float_tuples_are_equal(x, y):
        return all(floats_are_equal(x[i], y[i]) for i in range(len(x)))
    
    def test_triangle(a, b, c, A, B, C):
        """ Check that the triangle satisfies the law of cosines and law of
        sines"""
        assert floats_are_equal(a/sin(A), b/sin(B))
        assert floats_are_equal(a/sin(A), c/sin(C))
        assert floats_are_equal(c**2, a**2 + b**2 - 2 * a * b * cos(C))
        assert floats_are_equal(a**2, b**2 + c**2 - 2 * b * c * cos(A))
        assert floats_are_equal(b**2, c**2 + a**2 - 2 * c * a * cos(B))
    
    def test_solver(a, b, c):
        """ Test that the program works, for a triangle of sides a,b,c."""
        # first find the angles, testing SSS
        a1, b1, c1, A, B, C = solve(a=a, b=b, c=c)
        assert float_tuples_are_equal((a, b, c), (a1, b1, c1))
        test_triangle(a, b, c, A, B, C)
        tri = (a, b, c, A, B, C)
    
        # SAS tests
        assert float_tuples_are_equal(tri, solve(a=a, b=b, C=C))
        assert float_tuples_are_equal(tri, solve(a=a, c=c, B=B))
        assert float_tuples_are_equal(tri, solve(b=b, c=c, A=A))
    
        # SAA / ASA tests
        assert float_tuples_are_equal(tri, solve(a=a, A=A, B=B))
        assert float_tuples_are_equal(tri, solve(a=a, A=A, C=C))
        assert float_tuples_are_equal(tri, solve(a=a, B=B, C=C))
        assert float_tuples_are_equal(tri, solve(b=b, A=A, B=B))
        assert float_tuples_are_equal(tri, solve(b=b, A=A, C=C))
        assert float_tuples_are_equal(tri, solve(b=b, B=B, C=C))
        assert float_tuples_are_equal(tri, solve(c=c, A=A, B=B))
        assert float_tuples_are_equal(tri, solve(c=c, A=A, C=C))
        assert float_tuples_are_equal(tri, solve(c=c, B=B, C=C))
    
        Atype = 'acute' if A < pi/2 else 'obtuse'
        Btype = 'acute' if B < pi/2 else 'obtuse'
        Ctype = 'acute' if C < pi/2 else 'obtuse'
    
        # SSA tests
        assert float_tuples_are_equal(tri, solve(a=a, b=b, A=A, ssa_flag=Btype))
        assert float_tuples_are_equal(tri, solve(a=a, b=b, B=B, ssa_flag=Atype))
        assert float_tuples_are_equal(tri, solve(a=a, c=c, A=A, ssa_flag=Ctype))
        assert float_tuples_are_equal(tri, solve(a=a, c=c, C=C, ssa_flag=Atype))
        assert float_tuples_are_equal(tri, solve(b=b, c=c, B=B, ssa_flag=Ctype))
        assert float_tuples_are_equal(tri, solve(b=b, c=c, C=C, ssa_flag=Btype))
    
    def run_lots_of_tests():
        for a, b, c in ((7, 8, 9), (5, 6, 10), (5, 10, 6), (10, 5, 6), (5, 12, 13),
                        (12, 5, 13), (12, 13, 5)):
            test_solver(a, b, c)
        print('All tests pass!')
