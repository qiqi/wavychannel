import os
import re
import string
from numpy import *

def controlDict():
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

def boundary():
    boundary_file = 'constant/polyMesh/boundary'
    if not os.path.exists(boundary_file):
        return
    boundary = open(boundary_file).read()
    subs = {
         'inlet': '''
            type            cyclic;
            neighbourPatch  outlet;''',
         'outlet': '''
            type            cyclic;
            neighbourPatch  inlet;''',
         'wall': '''
            type            wall;'''
    }
    regex = '[\s]*{0}[\s]+{{[\s]+type[\s]+patch;[\s]+physicalType[\s]+patch;'
    repl = '\n    {0}\n    {{{1}'
    for patch_name, content in subs.items():
        boundary = re.sub(regex.format(patch_name),
                          repl.format(patch_name, content),
                          boundary)
    with open(boundary_file, 'wt') as f:
        f.write(boundary)

def decomposePar():
    content = '''
    /*--------------------------------*- C++ -*------------------------------*\
    | =========                 |                                             |
    | \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox       |
    |  \\    /   O peration     | Version:  4.0                               |
    |   \\  /    A nd           | Web:      www.OpenFOAM.org                  |
    |    \\/     M anipulation  |                                             |
    \*-----------------------------------------------------------------------*/
    FoamFile
    {{
        version     2.0;
        format      ascii;
        class       dictionary;
        location    "system";
        object      decomposeParDict;
    }}
    // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

    numberOfSubdomains {0};

    method          scotch;

    // ********************************************************************* //
    '''.format(open('../params/mpi_size').read())

    with open('system/decomposeParDict', 'wt') as f:
        f.write(content)

def transportProperties():
    template = string.Template(
            open('constant/transportProperties.template').read())
    nu, = loadtxt('../params/physics')
    with open('constant/transportProperties', 'wt') as f:
        f.write(template.substitute(
            NU=nu
    ))

if __name__ == '__main__':
    decomposePar()
    controlDict()
    boundary()
