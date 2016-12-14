import os
import sys
import argparse
import subprocess
from numpy import *

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str)
parser.add_argument('alpha', type=float)
parser.add_argument('beta', type=float)
parser.add_argument('phi_over_pi', type=float)
parser.add_argument('nu', type=float)
parser.add_argument('T', type=float)
parser.add_argument('nx', type=int)
parser.add_argument('ny', type=int)
parser.add_argument('nz', type=int)
args = parser.parse_args()

my_path = os.path.dirname(os.path.abspath(__file__))
git_path = os.path.abspath(os.path.join(my_path, '..'))

if not os.path.exists(args.path):
    subprocess.check_call(['git', 'clone', git_path, args.path])
else:
    subprocess.check_call(['git', 'pull'], cwd=args.path)

params = os.path.join(args.path, 'params')

phi = args.phi_over_pi * pi
savetxt(os.path.join(params, 'geom'), (args.alpha, args.beta, phi))
savetxt(os.path.join(params, 'physics'), (args.nu,))
savetxt(os.path.join(params, 'endTime'), (args.T,))
savetxt(os.path.join(params, 'grid'), (args.nx, args.ny, args.nz), fmt='%d')
savetxt(os.path.join(params, 'mpi_size'),
        (loadtxt(os.path.join(git_path, 'params', 'mpi_size')),), fmt='%d')

subprocess.check_call('make', cwd=args.path)
subprocess.check_call(['make', 'run'], cwd=args.path)
