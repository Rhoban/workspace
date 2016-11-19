# catkin workspace with packages manager

## Usage

First, you'll need to install `catkin`

Then, clone this repository and enter it:

    https://github.com/Rhoban/workspace.git
    cd workspace

Run the setup:

    ./workspace setup

You can now install a repository:

    ./workspace install rhoban/rhio

## Commands

To pull all the repositories:

    ./workspace pull

To build:

    ./workspace build

To build (debug):

    ./workspace build

Listing packages:

    ./workspace packages

To build just a specific package:

    ./workspace build RhIOShell
