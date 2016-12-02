import string
from numpy import *

template = string.Template(open('system/controlDict.template').read())
nx, ny, nz = loadtxt('../params/grid')
y = ((arange(ny, dtype=float) + 0.5) / ny - 0.5) * 0.1
z = (arange(nz, dtype=float) + 0.5) / nz * 0.2
y, z = meshgrid(y, z, indexing='ij')
x = 0.5 * ones(y.size)
y = ravel(y)
z = ravel(z)
xyz = transpose([x, y, z])
fmt = '({0:24.18f} {1:24.18f} {2:24.18f})'
points = '\n\t\t\t'.join([fmt.format(x,y,z) for x,y,z in xyz])
endTime = loadtxt('../params/endTime')

with open('system/controlDict', 'wt') as f:
    f.write(template.substitute(
        POINTS=points,
        ENDTIME=endTime
    ))
