# catkin workspace with packages manager

## Usage

First of all, you will need `php`, `catkin` and a few required packages:

    sudo apt-get install php php-xml python-pip python-empy python-setuptools python-nose
    sudo pip install -U catkin_tools mock


Then, clone this repository and enter it:

    https://github.com/Rhoban/workspace.git
    cd workspace

Run the setup:

    ./workspace setup

## For rhoban developers

You can install the latest unstable version using:

    ./workspace install rhoban/kid_size.git
    ./workspace install rhoban/environments.git
    
## For non-rhoban developers

You can install the latest public release using:

    git checkout final_2018
    ./workspace install rhoban/hl_kid_public.git
    ./workspace install rhoban/environments_public.git
    ./global_cmd.sh git checkout final_2018
    ln -sf src/rhoban/environments_public env

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

