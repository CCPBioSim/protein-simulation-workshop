# CCPBioSim Protein Simulation Workshop

[![ci](https://github.com/ccpbiosim/protein-simulation-workshop/actions/workflows/build.yaml/badge.svg?branch=main)](https://github.com/ccpbiosim/protein-simulation-workshop/actions/workflows/build.yaml)
[![latest](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fccpbiosim.github.io%2Fworkshop.json&query=%24.containers.protein-simulation-workshop.latest&labelColor=grey&logo=github&logoColor=white&label=latest&color=purple)](https://github.com/ccpbiosim/protein-simulation-workshop/pkgs/container/protein-simulation-workshop)
[![issues](https://img.shields.io/github/issues/ccpbiosim/protein-simulation-workshop?logo=github&labelColor=grey)](https://github.com/CCPBioSim/protein-simulation-workshop/issues)
[![pr](https://img.shields.io/github/issues-pr/ccpbiosim/protein-simulation-workshop?logo=github&labelColor=grey)](https://github.com/CCPBioSim/protein-simulation-workshop/pulls)

This workshop source repository contains the build recipe for a docker container derived from the CCPBioSim JupyterHub image. This container adds the necessary software packages and notebook content to form a deployable course container.

Though Python is a very popular and powerful environment for Biomolecular Simulation, many important and well-established tools require working from the command line in a terminal window. So it's an advantage to be familiar and comfortable with both ways of working. 
 
This workshop demonstrates two approaches to running MD simulations on a simple protein system:

1. From the command line in a terminal window, using AMBER
2. In Python, via a Jupter Notebook, using OpenMM

The focus is on the preliminary simulations that are required to relax and equiliobrate an initially-built system, so that later "production" simulations have the best chance of being stable and reliable.


## How to Use

This training course is deployed on the [CCPBioSim](www.ccpbiosim.ac.uk) website via our cloud infrastructure, however you can deploy on your own machine with docker.

Pull the container from our repository::

    docker pull ghcr.io/ccpbiosim/protein-simulation-workshop:latest

In our containers we are using the JupyterHub default port 8888, so you should
forward this port when deploying locally::

    docker run -p 8888:8888 ghcr.io/ccpbiosim/protein-simulation-workshop:latest

## Authors

Workshop Content Authors:

- Charlie Laughton

## Contact

Please direct all questions and feedback to [Charlie Laughton](mailto:charles.laughton@nottingham.ac.uk)
