# To build a container use following:
#     > sudo docker build -t lulesh .
#
# On success, run lulesh demo as follows:
#     > sudo docker run -t lulesh /tutorial/lulesh2.0 -i 10 -p
#
# Various catalyst scripts can be run as follows
#     > sudo docker run -v /tmp/output:/tmp/output -t lulesh \ 
#                       /tutorial/lulesh2.0 -i 50 -p --script /tutorial/scripts/savedata.py
#
# To run with multiple mpi ranks
#     > sudo docker run -v /tmp/output:/tmp/output -t lulesh \
#                       /usr/bin/mpirun --allow-run-as-root -np 8 \
#                       /tutorial/lulesh2.0 -i 50 -p --script /tutorial/scripts/lineplot.py
FROM ubuntu:xenial
MAINTAINER Utkarsh Ayachit <utkarsh.ayachit@kitware.com>

# install prerequisites
RUN apt-get update && apt-get install -y \
  git \
  curl \
  build-essential \
  gcc \
  g++ \
  python \
  python-dev \
  python-numpy \
  openmpi-bin \
  libopenmpi-dev \
  wget \
  ninja-build \
  autoconf \
  pkg-config

#------------------------------------------------------------------
# Setup prerequisites
#------------------------------------------------------------------
WORKDIR /tutorial/tools

# Get suitable cmake
RUN wget https://cmake.org/files/v3.10/cmake-3.10.2-Linux-x86_64.tar.gz
RUN mkdir cmake
RUN tar zxf cmake-3.10.2-Linux-x86_64.tar.gz --strip-component 1 -C cmake

#------------------------------------------------------------------
# Setup ParaView/Catalyst
#------------------------------------------------------------------
WORKDIR /tutorial/sources

# Clone ParaView-superbuild source
RUN git clone https://gitlab.kitware.com/paraview/paraview-superbuild.git --recursive

# Checkout a tested revision
RUN cd paraview-superbuild && git checkout 34535277f3e3b15a2adb73f143930c49dd7e00a2 -f && git submodule update

# Build a version of ParaView for this tutorial
WORKDIR /tutorial/builds/paraview-superbuild
RUN /tutorial/tools/cmake/bin/cmake -G Ninja \
      -DENABLE_paraview=ON \
      -DENABLE_paraviewsdk=ON \
      -DENABLE_mpi=ON \
      -DENABLE_osmesa=ON \
      -DENABLE_python=ON \
      -DUSE_SYSTEM_mpi=ON \
      -DUSE_SYSTEM_python=ON \
      -Dparaview_SOURCE_SELECTION=git \
      -Dparaview_GIT_TAG=1e6bc029c762eeec40ae66609507d50ca51015e8 \
      /tutorial/sources/paraview-superbuild
RUN ninja

#------------------------------------------------------------------
# Setup LULESH with Catalyst support
#------------------------------------------------------------------
WORKDIR /tutorial/sources/
RUN git clone https://github.com/utkarshayachit/LULESH.git lulesh

WORKDIR /tutorial/builds/lulesh
RUN /tutorial/tools/cmake/bin/cmake -G Ninja \
    -Denable_mpi=ON \
    -Denable_catalyst=ON \
    -DParaView_DIR=/tutorial/builds/paraview-superbuild/install/lib/cmake/paraview-5.4/ \
    /tutorial/sources/lulesh
RUN ninja
RUN cp ./lulesh2.0 /tutorial/

WORKDIR /tutorial
RUN ln -s /tutorial/sources/lulesh/scripts scripts
RUN ./lulesh2.0 -i 1

CMD ["/bin/bash"]
