import os
import sys
from numpy import *

base_path = os.path.abspath(sys.argv[1])

for line in open(os.path.join(base_path, 'constant', 'transportProperties')):
    line = line.strip()
    if line.startswith('nu ') and line.endswith(';'):
        nu = float(line[:-1].split()[-1])

D = 2 * 0.1 * 0.2 / (0.1 + 0.2)  # Hydrolic diameter

dp = 1
dT = 1

fT, fP, fU = (
        open(os.path.join(base_path, 'postProcessing', 'probes', '0', f))
        for f in ('T', 'p', 'U'))
for T, P, U in zip(fT, fP, fU):
    T = T.strip()
    P = P.strip()
    U = U.strip().replace('(', '').replace(')', '')
    if T.startswith('#'):
        continue
    T = array(T.split(), float)
    P = array(P.split(), float)
    U = array(U.split(), float)
    t = T[0]
    assert t == P[0] and t == U[0]
    T = T[1:]
    P = P[1:]
    U = U[1:].reshape([-1,3])[:,0]
    Umean = U.mean()
    Tmean = (T * U).mean() / U.mean()
    Re = Umean * D / nu
    f = dp * (2 * D) / Umean**2
    print(t, Re, f * Re)

t = pt[:,0]
dp = pt[:,1]
dt = pt[:,2]

fRe = dp * 2 * D * Re
plot(t, fRe)
ylim([50, 100])
