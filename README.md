p	# catkin workspace with packages manager

## Usage

First of all, you will need 'php' and some libraries: make sure to install
necessary packages:

    sudo apt-get install php php-xml

First, you'll need to install `catkin`, the most convenient method is the following

    sudo apt-get install python-pip python-empy python-setuptools
    sudo pip install -U catkin_tools


Then, clone this repository and enter it:

    https://github.com/Rhoban/workspace.git
    cd workspace

Run the setup:

    ./workspace setup

If you are a power rhoban team developper, use following command to perform a full install:
    ./workspace install rhoban/kid_size.git

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

Here, a full repository name is used, and the dependency is tagged `optional`. This means that
the user will be asked if he wants to install the dependency. You can also use `recommend`, that
would do the same, except that the default choice will be yes instead of no.

## Note when installing Rhoban's infamous Code repository
Try installing random stuff until it works, under ubuntu 16.04 the following were needed:

    sudo apt-get install liburdfdom-dev libboost-thread1.58-dev lib64ncurses5-dev g++ libopencv-dev libv4l-dev php7.0-xml


