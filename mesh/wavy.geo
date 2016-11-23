alpha = 0.1;
beta = 0.5;
phi = Pi / 3;

R = 0.25 / Sin(phi);
Ri = R - alpha / 2;
Ro = R + alpha / 2;

nx = 60;
ny = 24;
nz = 38;

Point(1) = {0, 0, 0};
Point(2) = {1/2, (Ro+Ri)*Cos(phi), 0};
Point(3) = {1, 0, 0};
Point(4) = {0, Ri, 0};
Point(5) = {0, Ro, 0};
Point(6) = {Ri*Sin(phi), Ri*Cos(phi), 0};
Point(7) = {Ro*Sin(phi), Ro*Cos(phi), 0};
Point(8) = {1-Ri*Sin(phi), Ri*Cos(phi), 0};
Point(9) = {1-Ro*Sin(phi), Ro*Cos(phi), 0};
Point(10) = {1, Ri, 0};
Point(11) = {1, Ro, 0};
Circle(1) = {4, 1, 6};
Circle(2) = {5, 1, 7};
Circle(3) = {7, 2, 9};
Circle(4) = {6, 2, 8};
Circle(5) = {8, 3, 10};
Circle(6) = {9, 3, 11};
Line(7) = {5, 4};
Line(8) = {11, 10};
Line(9) = {7, 6};
Line(10) = {9, 8};

Transfinite Line {1,2,5,6} = nx/4;
Transfinite Line {3,4} = nx/2;
Transfinite Line {7,8,9,10} = ny Using Bump 0.5;

Line Loop(11) = {7, 1, -9, -2};
Plane Surface(12) = {11};
Line Loop(13) = {9, 4, -10, -3};
Plane Surface(14) = {13};
Line Loop(15) = {10, 5, -8, -6};
Plane Surface(16) = {15};

Transfinite Surface {12,14,16};
Recombine Surface {12,14,16};

Extrude {0, 0, alpha/beta} {
Surface{12,14,16};
Layers{nz};
Recombine;
}
Physical Surface("wall") = {59, 81, 37, 29, 51, 73, 82, 16, 60, 14, 38, 12};
Physical Surface("inlet") = {25};
Physical Surface("outlet") = {77};
Physical Volume("fluid") = {1, 2, 3};
