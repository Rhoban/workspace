# catkin workspace with packages manager

## Usage

First, you'll need to install `catkin`, the most convenient method is the following

    sudo apt-get install python-pip python-empy
    sudo pip install -U catkin_tools


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

## Dependencies

In `packages.xml`, you can annotate the repositories:

```xml
    <build_depend>model</build_depend> <!-- rhobanproject/model -->
```

By default, this will use GitHub, you can also use complete repo names

```xml
    <build_depend>csa_mdp_experiments</build_depend> <!-- optional git@bitbucket.org:rhoban/csa_mdp_experiments.git -->
```

Here, a full repository name is used, and the dependency is tagged optional
