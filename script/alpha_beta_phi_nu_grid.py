from __future__ import print_function
import os
import sys
import shutil
import subprocess
import itertools
import StringIO
from numpy import *

my_path = os.path.dirname(__file__)

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
    nx, ny, nz = '120', '40', '50'
    if not os.path.exists(os.path.join(path, 'foam', 'processor0')):
        T = '10'
        print(path, 'not exists')
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        subprocess.check_call([
            'python', 'runcase.py', path,
            alpha, beta, phi_over_pi,
            nu, T, nx, ny, nz])
    else:
        try:
            out = subprocess.check_output(['python', os.path.join(my_path, 'postpro.py'), path])
            out = loadtxt(StringIO.StringIO(out.decode()))
            T = out[-1,0]
            out = out[-200:,1:]
            Re, Re_std = out[:,0].mean(), out[:,0].std()
            fR, fR_std = out[:,1].mean(), out[:,1].std()
            Nu, Nu_std = out[:,2].mean(), out[:,2].std()
            print(path, ' has run to T = ', T)
            print(alpha, beta, phi_over_pi, nu, Re, fR, Nu, Re_std, fR_std, Nu_std)
            tol = 0.001
        except:
            T = 0
        if T == 0 or Re_std > Re * tol or fR_std > fR * tol or Nu_std > Nu * tol:
            T = str(int(T) + 10)
            print('Running further to T = ', T)
            sys.stdout.flush()
            subprocess.check_call([
                'python', 'runcase.py', path,
                alpha, beta, phi_over_pi,
                nu, T, nx, ny, nz])
