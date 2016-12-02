import re

boundary_file = 'constant/polyMesh/boundary'
boundary = open(boundary_file).read()
# subs = {
#      'inlet': '''
#         type            mappedPatch;
#         sampleMode      nearestPatchFace;
#         samplePatch     outlet;
#         offsetMode      uniform;
#         offset          (1 0 0);''',
#      'outlet': '''
#         type            mappedPatch;
#         sampleMode      nearestPatchFace;
#         samplePatch     inlet;
#         offsetMode      uniform;
#         offset          (-1 0 0);''',
#      'wall': '''
#         type            wall;'''
# }
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
