cmake_minimum_required(VERSION 3.3)
project(lulesh)

option(enable_mpi "Enable MPI" ON)
option(enable_catalyst "Enable Catalyst" ON)

set(sources
	lulesh.h
	lulesh.cc
	lulesh-comm.cc
	lulesh-viz.cc
	lulesh-util.cc
	lulesh-init.cc
	)
if (enable_catalyst)
	list(APPEND sources
		lulesh-catalyst.cc)
endif()

add_executable(lulesh2.0 ${sources})

if (enable_mpi)
	find_package(MPI REQUIRED)
	target_link_libraries(lulesh2.0 PRIVATE ${MPI_C_LIBRARIES} ${MPI_CXX_LIBRARIES})
	target_include_directories(lulesh2.0 PRIVATE ${MPI_C_INCLUDE_PATH} ${MPI_CXX_INCLUDE_PATH})
	target_compile_definitions(lulesh2.0 PRIVATE USE_MPI=1)
else()
	target_compile_definitions(lulesh2.0 PRIVATE USE_MPI=0)
endif()

if (enable_catalyst)
	find_package(ParaView 5.4
		COMPONENTS vtkPVCatalyst  vtkPVPythonCatalyst
		REQUIRED)
	target_link_libraries(lulesh2.0 PRIVATE vtkPVCatalyst vtkPVPythonCatalyst)
	target_compile_definitions(lulesh2.0 PRIVATE VIZ_CATALYST)
	target_include_directories(lulesh2.0 PRIVATE ${PARAVIEW_INCLUDE_DIRS})
endif()
