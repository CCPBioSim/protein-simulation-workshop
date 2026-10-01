# Start with BioSim base image.
ARG BASE_IMAGE=latest
FROM ghcr.io/ccpbiosim/jupyterhub-base:$BASE_IMAGE

LABEL maintainer="James Gebbie-Rayet <james.gebbie@stfc.ac.uk>"

ARG TARGETPLATFORM
ARG AMBERTOOLS_DL=null
ARG AMBERTOOLS_VER=26

# Switch to jovyan user.
USER $NB_USER
WORKDIR $HOME

ENV AMBERHOME=/opt/conda
# Ensure Fortran compilers force legacy argument matching across all sub-tools
ENV FFLAGS="-fallow-argument-mismatch -fallow-invalid-boz -w"
ENV FCFLAGS="-fallow-argument-mismatch -fallow-invalid-boz -w"

# Install workshop deps 
RUN conda install -y -c conda-forge -c bioconda \
    #bioconda::bio=1.8.4 \
    conda-forge::ipywidgets=8.1.9 \
    #conda-forge::freesasa=2.2.1 \
    #conda-forge::gemmi=0.7.5 \
    conda-forge::matplotlib=3.11.2 \
    conda-forge::mdtraj=1.11.1 \
    conda-forge::netcdf4=1.7.4 \
    #conda-forge::networkx=3.7 \
    #conda-forge::numba=0.67.0 \
    conda-forge::nglview=4.0.1 \
    conda-forge::openmm=8.6.1 \
    conda-forge::openmpi=5.0.10 \
    conda-forge::mpi4py \
    conda-forge::pandas \
    conda-forge::parmed=4.3.1
    #conda-forge::rich=15.0.0 \
    #conda-forge::scikit-learn=1.9.1 \
    #conda-forge::sympy=1.14.0

WORKDIR /tmp

RUN wget --no-verbose $AMBERTOOLS_DL/ambertools$AMBERTOOLS_VER.tar.bz2 && \
    tar xjf ambertools$AMBERTOOLS_VER.tar.bz2 && \
    rm ambertools$AMBERTOOLS_VER.tar.bz2 && \
    mv ambertools${AMBERTOOLS_VER}_src ambertools_src

WORKDIR /tmp/ambertools_src
RUN ./update_amber --update
RUN sed -i 's/add_library(kmmd ${KMMD_SOURCE})/if(NOT TARGET kmmd)\n  add_library(kmmd ${KMMD_SOURCE})\nendif()/' AmberTools/src/kmmd/CMakeLists.txt

# 1. Serial / OpenMP Build
RUN mkdir /tmp/build_serial
WORKDIR /tmp/build_serial

RUN cmake /tmp/ambertools_src \
    -DCMAKE_INSTALL_PREFIX=/opt/conda \
    -DPYTHON_EXECUTABLE=/opt/conda/bin/python \
    -DUSE_CONDA_LIBS=TRUE \
    -DBUILD_PYTHON=FALSE \
    -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=TRUE \
    -DDOWNLOAD_MINICONDA=FALSE \
    -DCOMPILER=GNU \
    -DBUILD_GUI=FALSE \
    -DOPENMP=TRUE \
    -DCUDA=FALSE \
    -DMPI=FALSE \
    -DUSE_FFT=True \
    -DBUILD_DEPRECATED=False \
    -DBUILD_INDEV=False \
    -DBUILD_PERL=True \
    -DOPTIMIZE=True \
    -DCMAKE_Fortran_FLAGS="-fallow-argument-mismatch -fallow-invalid-boz -w"

RUN make -j8 && make install && rm -rf /tmp/build_serial

# 2. Parallel (MPI) Build
RUN mkdir /tmp/build_mpi
WORKDIR /tmp/build_mpi

RUN cmake /tmp/ambertools_src \
    -DCMAKE_INSTALL_PREFIX=/opt/conda \
    -DPYTHON_EXECUTABLE=/opt/conda/bin/python \
    -DUSE_CONDA_LIBS=TRUE \
    -DBUILD_PYTHON=FALSE \
    -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=TRUE \
    -DDOWNLOAD_MINICONDA=FALSE \
    -DCOMPILER=GNU \
    -DBUILD_GUI=FALSE \
    -DOPENMP=TRUE \
    -DCUDA=FALSE \
    -DMPI=TRUE \
    -DBUILD_QUICK=FALSE \
    -DUSE_FFT=True \
    -DBUILD_DEPRECATED=False \
    -DBUILD_INDEV=False \
    -DBUILD_PERL=True \
    -DOPTIMIZE=True \
    -DCMAKE_Fortran_FLAGS="-fallow-argument-mismatch -fallow-invalid-boz -w" \
    -DMPI_Fortran_COMPILE_FLAGS="-fallow-argument-mismatch -fallow-invalid-boz -w"

RUN make -j8 && make install && rm -rf /tmp/build_mpi /tmp/ambertools_src

WORKDIR $HOME

COPY docker/fix-nglview.sh /tmp/fix-nglview.sh
RUN bash /tmp/fix-nglview.sh

# Get workshop files and move them to jovyan directory.
COPY --chown=1000:100 . .
RUN rm -rf INSTALL.txt LICENSE README.md docker .git .github .gitignore environment.yaml run_notebook.sh

# Always finish with non-root user as a precaution.
USER $NB_USER
