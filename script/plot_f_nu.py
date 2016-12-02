import os
import sys

base_path = os.path.abspath(sys.argv[1])

for line in open(os.path.join(base_path, 'constant', 'transportProperties')):
    line = line.strip()
    if line.startswith('nu ') and line.endswith(';'):
        nu = float(line[:-1].split()[-1])

D = 2 * 0.1 * 0.2 / (0.1 + 0.2)  # Hydrolic diameter
Re = D / nu

pt = loadtxt(os.path.join(base_path, 'postProcessing',
             'pTDrop', '0', 'fieldValueDelta_0.01.dat'))

t = pt[:,0]
dp = pt[:,1]
dt = pt[:,2]

fRe = dp * 2 * D * Re
plot(t, fRe)
ylim([50, 100])
