import math
import unittest

from graphics.venn import solve

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
        self.tests = ((7, 8, 9), (5, 6, 10), (5, 10, 6), (10, 5, 6), 
                      (5, 12, 13), (12, 5, 13), (12, 13, 5))

    def test_triangle_solver(self):
        """ Test that the program works, for a triangle of sides a,b,c."""

        for a, b, c in self.tests:
            # SSS
            a1, b1, c1, A, B, C = solve(a=a, b=b, c=c)
            self.assertAlmostEqual(a, a1, places=7)
            self.assertAlmostEqual(b, b1, places=7)
            self.assertAlmostEqual(c, c1, places=7)

            self.assertAlmostEqual(a / math.sin(A), b / math.sin(B), places=7)
            self.assertAlmostEqual(a / math.sin(A), c / math.sin(C), places=7)
            self.assertAlmostEqual(a / math.sin(A), c / math.sin(C), places=7)

            self.assertAlmostEqual(math.pow(c, 2), math.pow(a, 2) + math.pow(b, 2) - 2 * a * b * math.cos(C), places=7)
            self.assertAlmostEqual(math.pow(a, 2), math.pow(b, 2) + math.pow(c, 2) - 2 * b * c * math.cos(A), places=7)
            self.assertAlmostEqual(math.pow(b, 2), math.pow(c, 2) + math.pow(a, 2) - 2 * c * a * math.cos(B), places=7)

            tri = (a, b, c, A, B, C)
    
            # SAS
            a1, b1, c1, A1, B1, C1 = solve(a=a, b=b, C=C)
            self.assertAlmostEqual(a, a1, places=7) 
            self.assertAlmostEqual(b, b1, places=7) 
            self.assertAlmostEqual(C, C1, places=7) 
            
            a1, b1, c1, A1, B1, C1 = solve(a=a, c=c, B=B)
            self.assertAlmostEqual(a, a1, places=7) 
            self.assertAlmostEqual(c, c1, places=7) 
            self.assertAlmostEqual(B, B1, places=7) 

            a1, b1, c1, A1, B1, C1 = solve(b=b, c=c, A=A)
            self.assertAlmostEqual(b, b1, places=7) 
            self.assertAlmostEqual(c, c1, places=7) 
            self.assertAlmostEqual(A, A1, places=7) 

            # SAA / ASA
            a1, b1, c1, A1, B1, C1 = solve(a=a, A=A, B=B)
            self.assertAlmostEqual(a, a1, places=7)
            self.assertAlmostEqual(A, A1, places=7)
            self.assertAlmostEqual(B, B1, places=7)

            a1, b1, c1, A1, B1, C1 = solve(a=a, A=A, C=C)
            self.assertAlmostEqual(a, a1, places=7)
            self.assertAlmostEqual(A, A1, places=7)
            self.assertAlmostEqual(C, C1, places=7)

            a1, b1, c1, A1, B1, C1 = solve(a=a, B=B, C=C)
            self.assertAlmostEqual(a, a1, places=7)
            self.assertAlmostEqual(B, B1, places=7)
            self.assertAlmostEqual(C, C1, places=7)

            a1, b1, c1, A1, B1, C1 = solve(b=b, A=A, B=B)
            self.assertAlmostEqual(b, b1, places=7)
            self.assertAlmostEqual(A, A1, places=7)
            self.assertAlmostEqual(B, B1, places=7)

            a1, b1, c1, A1, B1, C1 = solve(b=b, A=A, C=C)
            self.assertAlmostEqual(b, b1, places=7)
            self.assertAlmostEqual(A, A1, places=7)
            self.assertAlmostEqual(C, C1, places=7)

            a1, b1, c1, A1, B1, C1 = solve(b=b, B=B, C=C)
            self.assertAlmostEqual(b, b1, places=7)
            self.assertAlmostEqual(B, B1, places=7)
            self.assertAlmostEqual(C, C1, places=7)

            a1, b1, c1, A1, B1, C1 = solve(c=c, A=A, B=B)
            self.assertAlmostEqual(c, c1, places=7)
            self.assertAlmostEqual(A, A1, places=7)
            self.assertAlmostEqual(B, B1, places=7)

            a1, b1, c1, A1, B1, C1 = solve(c=c, A=A, C=C)
            self.assertAlmostEqual(c, c1, places=7)
            self.assertAlmostEqual(A, A1, places=7)
            self.assertAlmostEqual(C, C1, places=7)

            a1, b1, c1, A1, B1, C1 = solve(c=c, B=B, C=C)
            self.assertAlmostEqual(c, c1, places=7)
            self.assertAlmostEqual(B, B1, places=7)
            self.assertAlmostEqual(C, C1, places=7)
    
            Atype = 'acute' if A < pi/2 else 'obtuse'
            Btype = 'acute' if B < pi/2 else 'obtuse'
            Ctype = 'acute' if C < pi/2 else 'obtuse'

            # SSA tests
            '''
            assert float_tuples_are_equal(tri, solve(a=a, b=b, A=A, ssa_flag=Btype))
            assert float_tuples_are_equal(tri, solve(a=a, b=b, B=B, ssa_flag=Atype))
            assert float_tuples_are_equal(tri, solve(a=a, c=c, A=A, ssa_flag=Ctype))
            assert float_tuples_are_equal(tri, solve(a=a, c=c, C=C, ssa_flag=Atype))
            assert float_tuples_are_equal(tri, solve(b=b, c=c, B=B, ssa_flag=Ctype))
            assert float_tuples_are_equal(tri, solve(b=b, c=c, C=C, ssa_flag=Btype))
            '''

if __name__=='__main__':
    unittest.main()
