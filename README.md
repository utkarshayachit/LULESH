ParaView Catalyst enabled LULESH
================================

This is fork of [LULESH 2.0](README) that adds support for
in situ processing using Catalyst.

The code base has following changes to add support for ParaView Catalyst:

1. We needed to tweak LULESH API (commit e61b8447) to expose internal array pointers
   to pass data to Catalyst with zero-copy, whenever possible.

2. Next, we added the Catalyst adaptor ([.h](lulesh-catalyst.h)  [.cc](lulesh-catalyst.cc)).
   This adaptor is Python-enabled i.e. we will use Catalyst Python scripts to do in situ
   viz. Non-python pipelines are also possible, but left out in this tutorial.

3. We also adde a CMakeLists.txt file to *cmake-ify* the project to simply linking against
   Catalyst libraries. There are ways around this too, so feel free to ping if you
   need to avoid this step.

4. Minimally tweaked scripts exports from **ParaView Catalyst Script Export** to improve
   reability and add configuration options to change output directory, for example,
   are available under [scripts](scripts) directory.


Build instructions
-------------------

```
> mkdir lulesh
> cd lulesh
> git clone https://github.com/utkarshayachit/LULESH.git -b catalyst_adaptor src
> mkdir build
> cd build
> cmake -Denable_mpi=ON -Denable_catalyst=ON -DParaView_DIR=<> ..\src
> make
```
Where `ParaView_DIR` should be set to the directory containing `ParaViewConfig.cmake` file in your ParaView or Catalyst build (or SDK install).

Run instructions
-----------------

To run LULESH with default setup, you can simply use

```
> lulesh2.0
```

To run using MPI, if MPI was enabled

```
> mpirun -np <ranks> lulesh2.0
```

To run with a catalyst pipeline for saving out full datasets

```
> lulesh2.0 --script <src>/scripts/savedata.py
```

You can pass multiple scripts, to execute mutliple pipelines
during the same run

```
> lulesh2.0 --script <src>/scripts/savedata.py \
            --script <src>/scripts/surfacecolor.py
```

**NOTE:** Please edit the scripts to update directory where to generate
output files and write frequency.

Scripts
-------

1. [**savedata.py**](scripts/savedata.py): This script saves out the data in pvtu files.

2. [**surfacecolor.py**](scripts/surfacecolor.py):
   This script generates surface plots with the surface colored using velocity magnitude.
   This was exported using ParaView UI. The visualization pipeline was set up using the representative dataset
   generated using **savedata.py**. The script has been slighly modified to make it more readable and expose
   options to change output directory and write frequency at the top of the script.

3. [**lineplot.py**](scripts/lineplot.py):
   This script generates a line plot for velocity magnitude.
   This was exported using ParaView UI. The visualization pipeline was set up using the representative dataset
   generated using **savedata.py**. The script has been slighly modified to make it more readable and expose
   options to change output directory and write frequency at the top of the script.
