import os
import sys
import string
from numpy import *

template = string.Template(file('wavy.geo.template').read())

path = sys.argv[1]
alpha, beta, phi = loadtxt(os.path.join(path, 'geom'))
nx, ny, nz = loadtxt(os.path.join(path, 'grid'))

content = template.substitute(
        ALPHA=alpha,
        BETA=beta,
        PHI=phi,
        NX=nx,
        NY=ny,
        NZ=nz)
with open('wavy.geo', 'wt') as f:
    f.write(content)
