alpha = 0.1;
beta = 0.5;
phi = Pi / 3;

R = 0.25 / Sin(phi);
Ri = R - alpha / 2;
Ro = R + alpha / 2;

nx = 120;
ny = 40;
nz = 50;

Point(1) = {0, 0, 0};
Point(2) = {1/2, (Ro+Ri)*Cos(phi), 0};
Point(3) = {Ri*Sin(phi), Ri*Cos(phi), 0};
Point(4) = {Ro*Sin(phi), Ro*Cos(phi), 0};
Point(5) = {1-Ri*Sin(phi), Ri*Cos(phi), 0};
Point(6) = {1-Ro*Sin(phi), Ro*Cos(phi), 0};
Point(7) = {-Ri*Sin(phi), Ri*Cos(phi), 0};
Point(8) = {-Ro*Sin(phi), Ro*Cos(phi), 0};
Circle(1) = {7, 1, 3};
Circle(2) = {8, 1, 4};
Circle(3) = {4, 2, 6};
Circle(4) = {3, 2, 5};
Line(5) = {8, 7};
Line(6) = {4, 3};
Line(7) = {6, 5};

Transfinite Line {1,2,3,4} = nx/2;
Transfinite Line {5,6,7} = ny Using Bump 0.5;

Line Loop(8) = {2, 6, -1, -5};
Plane Surface(9) = {8};
Line Loop(10) = {6, 4, -7, -3};
Plane Surface(11) = {10};

Transfinite Surface {9,11};
Recombine Surface {9,11};

Extrude {0, 0, alpha/beta} {
Surface{9,11};
Layers{nz};
Recombine;
}

Physical Surface("wall") = {20, 28, 9, 33, 54, 11, 46, 55};
Physical Surface("inlet") = {32};
Physical Surface("outlet") = {50};
Physical Volume("fluid") = {1, 2};
