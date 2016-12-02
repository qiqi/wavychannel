default:	foam/constant/polyMesh/boundary foam/system/decomposeParDict foam/processor0/constant/polyMesh/boundary 

#foam2/constant/polyMesh/boundary foam2/system/decomposeParDict foam2/processor0/constant/polyMesh/boundary pisoFoam/pisoFoam

NP=$(shell cat mpi_size)

pisoFoam/pisoFoam:	pisoFoam/*.H pisoFoam/*.C
	cd pisoFoam; wmake

mesh/wavy.msh:	mesh/wavy.geo
	cd mesh; gmsh -3 wavy.geo > gmsh.out

mesh/wavy2.msh:	mesh/wavy2.geo
	cd mesh; gmsh -3 wavy2.geo > gmsh2.out

foam/constant/polyMesh/boundary:	mesh/wavy.msh foam/boundary.py
	cd foam; gmshToFoam ../mesh/wavy.msh > gmshToFoam.out; python boundary.py

foam2/boundary.py:	foam
	mkdir -p foam2/constant; cp -n foam/*.py foam2/; cp -rf foam/system foam2/; cp -rf foam/0 foam2/; cp -n foam/constant/*Properties foam2/constant

foam2/decomposePar.py:	foam2/boundary.py

foam2/constant/polyMesh/boundary:	foam2/boundary.py mesh/wavy2.msh foam2/boundary.py
	cd foam2; gmshToFoam ../mesh/wavy2.msh > gmshToFoam.out; python boundary.py

foam/system/decomposeParDict:	foam/decomposePar.py mpi_size
	cd foam; python decomposePar.py

foam2/system/decomposeParDict:	foam2/decomposePar.py mpi_size
	cd foam2; python decomposePar.py

foam/processor0/constant/polyMesh/boundary:	foam/constant/polyMesh/boundary foam/system/decomposeParDict
	cd foam; rm -rf processor*; decomposePar > decomposePar.out

foam2/processor0/constant/polyMesh/boundary:	foam2/constant/polyMesh/boundary foam2/system/decomposeParDict
	cd foam2; rm -rf processor*; decomposePar > decomposePar.out

run:	foam/constant/polyMesh/boundary foam/processor0/constant/polyMesh/boundary foam/system/decomposeParDict pisoFoam/pisoFoam
	cd foam; rm -rf 0.* 1* 2* 3* 4* 5* 6* 7* 8* 9*; mpiexec -np $(NP) ../pisoFoam/pisoFoam -parallel > pisoFoam.out

