default:	foam/constant/polyMesh/boundary foam/system/decomposeParDict foam/system/controlDict foam/processor0/constant/polyMesh/boundary 

NP=$(shell cat params/mpi_size)

pisoFoam/pisoFoam:	pisoFoam/*.H pisoFoam/*.C
	cd pisoFoam; wmake

mesh/wavy.geo:	mesh/wavy.geo.template mesh/geo.py params/grid params/geom
	cd mesh; python geo.py ../params

mesh/wavy.msh:	mesh/wavy.geo
	cd mesh; gmsh -3 wavy.geo > gmsh.out

foam/constant/polyMesh/boundary:	mesh/wavy.msh foam/setup.py foam/system/controlDict
	cd foam; gmshToFoam ../mesh/wavy.msh > gmshToFoam.out; python setup.py

foam/system/decomposeParDict:	foam/setup.py params/mpi_size
	cd foam; python setup.py

foam/system/controlDict:	foam/setup.py params/endTime params/physics
	cd foam; python setup.py

foam/processor0/constant/polyMesh/boundary:	foam/constant/polyMesh/boundary foam/system/decomposeParDict
	cd foam; rm -rf processor*; decomposePar > decomposePar.out

run:	foam/constant/polyMesh/boundary foam/processor0/constant/polyMesh/boundary foam/system/decomposeParDict foam/system/controlDict pisoFoam/pisoFoam
	cd foam; rm -rf 0.* 1* 2* 3* 4* 5* 6* 7* 8* 9*; mpiexec -np $(NP) ../pisoFoam/pisoFoam -parallel > pisoFoam.out

