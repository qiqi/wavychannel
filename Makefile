default:	foam/constant/polyMesh/boundary foam/system/decomposeParDict foam/processor0/constant/polyMesh/boundary

NP=$(shell cat mpi_size)

mesh/wavy.msh:	mesh/wavy.geo
	cd mesh; gmsh -3 wavy.geo > gmsh.out

foam/constant/polyMesh/boundary:	mesh/wavy.msh foam/boundary.py
	cd foam; gmshToFoam ../mesh/wavy.msh > gmshToFoam.out; python boundary.py

foam/system/decomposeParDict:	foam/decomposePar.py mpi_size
	cd foam; python decomposePar.py

foam/processor0/constant/polyMesh/boundary:	foam/constant/polyMesh/boundary foam/system/decomposeParDict
	cd foam; rm -rf processor*; decomposePar > decomposePar.out

run:	foam/constant/polyMesh/boundary foam/processor0/constant/polyMesh/boundary foam/system/decomposeParDict
	cd foam; rm -rf 0.* 1* 2* 3* 4* 5* 6* 7* 8* 9*; mpiexec -np $(NP) pisoFoam -parallel > pisoFoam.out

