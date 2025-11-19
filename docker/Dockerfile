# Start with BioSim base image.
ARG BASE_IMAGE=latest
FROM ghcr.io/ccpbiosim/jupyterhub-base:$BASE_IMAGE

LABEL maintainer="James Gebbie-Rayet <james.gebbie@stfc.ac.uk>"

ARG AMBERTOOLS_DL=null
ARG AMBERTOOLS_VER=25
ARG AMBER_DL=null
ARG AMBER_VER=24

# Switch to jovyan user.
USER $NB_USER
WORKDIR $HOME

# Install workshop deps
RUN mamba install -c conda-forge openmm matplotlib scipy cython
RUN pip install git+https://github.com/CompBioAsia/CBAtools.git
WORKDIR /tmp

RUN wget --no-verbose $AMBERTOOLS_DL/ambertools$AMBERTOOLS_VER.tar.bz2 && \
    tar xjf ambertools$AMBERTOOLS_VER.tar.bz2 && \
    rm ambertools$AMBERTOOLS_VER.tar.bz2 && \
    mv ambertools${AMBERTOOLS_VER}_src ambertools_src

RUN wget --no-verbose $AMBER_DL/pmemd$AMBER_VER.tar.bz2 && \
    tar xjf pmemd$AMBER_VER.tar.bz2 && \
    rm pmemd$AMBER_VER.tar.bz2 && \
    mv pmemd${AMBER_VER}_src pmemd_src

WORKDIR /tmp/ambertools_src
RUN ./update_amber --update
WORKDIR /tmp/pmemd_src
RUN ./update_pmemd --update

RUN mkdir /tmp/build_ambertools && \
    mkdir /tmp/build_pmemd
WORKDIR /tmp/build_ambertools

RUN cmake /tmp/ambertools_src -DCMAKE_INSTALL_PREFIX=/opt/conda -DPYTHON_EXECUTABLE=/opt/conda/bin/python -DUSE_CONDA_LIBS=TRUE -DBUILD_PYTHON=TRUE -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=TRUE -DDOWNLOAD_MINICONDA=FALSE -DCOMPILER=MANUAL -DBUILD_GUI=FALSE -DCOMPILER=GNU -DOPENMP=TRUE -DCUDA=FALSE -DMPI=FALSE -DUSE_FFT=True -DBUILD_DEPRECATED=FALSE -DBUILD_INDEV=FALSE -DBUILD_PERL=FALSE -DOPTIMIZE=TRUE
RUN make -j8
RUN make install

WORKDIR /tmp/build_pmemd

RUN cmake /tmp/pmemd_src -DCMAKE_INSTALL_PREFIX=/opt/conda -DPYTHON_EXECUTABLE=/opt/conda/bin/python -DBUILD_PYTHON=FALSE -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=TRUE -DDOWNLOAD_MINICONDA=FALSE -DCOMPILER=MANUAL -DBUILD_GUI=FALSE -DCOMPILER=GNU -DOPENMP=TRUE -DCUDA=FALSE -DMPI=FALSE -DPMEMD_ONLY=TRUE -DBUILD_DEPRECATED=FALSE -DBUILD_INDEV=FALSE -DBUILD_PERL=FALSE -DOPTIMIZE=TRUE
RUN make -j8
RUN make install

# Cleanup.
RUN rm -r /tmp/ambertools_src /tmp/pmemd_src /tmp/build_ambertools /tmp/build_pmemd

# Add the exec to the path.
ENV AMBERHOME=/opt/conda

# Get workshop files and move them to jovyan directory.
COPY --chown=1000:100 . .
RUN rm -rf INSTALL.txt LICENSE README.md docker .git .github .gitignore

# Copy updated lab workspace
#COPY --chown=1000:100 docker/default-37a8.jupyterlab-workspace /home/jovyan/.jupyter/lab/workspaces/default-37a8.jupyterlab-workspace

# Always finish with non-root user as a precaution.
USER $NB_USER
