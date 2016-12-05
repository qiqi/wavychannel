import os
import shutil
import subprocess
import itertools
from numpy import *

Alpha = array([0.05, 0.1, 0.2])
Beta = array([0.5, 1.0])
Phi_over_pi = array([0.001, 1./12, 1./6, 1./4, 1./3])
Nu = array([0.0002, 0.0003, 0.0005, 0.001])

for alpha, beta, phi_over_pi, nu in itertools.product(Alpha, Beta, Phi_over_pi, Nu):
    alpha = str(alpha)
    beta = str(beta)
    phi_over_pi = str(phi_over_pi)
    nu = str(nu)
    path = '{0}/{1}/{2}/{3}'.format(alpha, beta, phi_over_pi, nu)
    T, nx, ny, nz = '10', '120', '40', '50'
    if not os.path.exists(os.path.join(path, 'proessor0', T)):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        subprocess.check_call([
            'python', 'runcase.py', path,
            alpha, beta, phi_over_pi,
            nu, T, nx, ny, nz])
