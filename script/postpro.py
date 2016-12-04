import os
import sys
from numpy import *

base_path = os.path.abspath(sys.argv[1])
foam_path = os.path.join(base_path, 'foam')

nu = loadtxt(os.path.join(base_path, 'params/physics'))
alpha, beta, phi = loadtxt(os.path.join(base_path, 'params/geom'))
nx, ny, nz = loadtxt(os.path.join(base_path, 'params/grid'), dtype=int)

D = 2 * alpha * (alpha/beta) / (alpha + alpha/beta)  # Hydrolic diameter

dp = 1
dT = 1

fT, fP, fU = (
        open(os.path.join(foam_path, 'postProcessing', 'probes', '0', f))
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

figure()
plot(T.reshape([ny, nz]))
figure()
plot(U.reshape([ny, nz]))
