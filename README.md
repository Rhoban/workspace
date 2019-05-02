# catkin workspace with packages manager

## Setup of the system

### TODO: Update of the README

- Choose the recommended distribution for next year (18.04?)
- Update dependencies (moving to OpenCV3)
  - Currently nonfree of OpenCV3 is not supported in 18.04
- Change install commands for rhoban developers (use private repositories)
- Is 'workspace' only for 'kid_size' or not?
  - To be discussed

### Recommended Operating System

The recommended operating system to run this version of the software is `Ubuntu
16.04 Xenial Xerus` using other OS might result on issues with some of the
packages required.

### Installing APT dependencies

First of all, you will need to install required packages:

    sudo apt-get install gcc cmake git libtinyxml-dev libncurses5-dev\
        php php-cli php-xml libopencv-dev libv4l-dev gnuplot5-qt \
        python-pip python-empy python-setuptools python-nose chrpath ffmpeg libudev-dev \
        libsfml-dev libconsole-bridge-dev freeglut3-dev libx11-dev libxrandr-dev libfreetype6-dev \
		    libjsoncpp-dev libprotobuf-dev protobuf-compiler libgtest-dev libtclap-dev \
        qt5-default qtmultimedia5-dev libqt5webkit5
        
### Installing catkin

    sudo pip install -U catkin_tools mock
    
### Setting up your Github account with your public key

Since the `workspace` manager handle dozens of repositories at once, it is much
more convenient to use SSH keys.  If you don't have a one, generate one using:

    ssh-keygen -t rsa
    
Sign in on your GitHub account and go to Settings, and then "SSH and GPG
keys". Click "New SSH key" and copy the content of `.ssh/id_rsa.pub` in the key
field, choose any name you want and validate the new key.

### Setting up the workspace

Clone the latest stable release of `workspace` repository and move to it:

    git clone -b final_2018 https://github.com/rhoban/workspace.git
    cd workspace

Then, run the setup:

    ./workspace setup

You can then install the latest stable release of all the rhoban source code:
Note: You should make a fork of rhoban/environments_public in order to have
the configuration for your own robots.

    ./workspace install rhoban/hl_kid_public.git
    ./workspace install rhoban/environments_public.git
    ./workspace install rhoban/monitoring_robocup.git
    ./workspace git checkout final_2018
    ln -sf src/rhoban/environments_public env

Some symbolic links should be modified in env/fake.
"default_robot" should be change with one of the robot folder name:

    ln -sf ../default_robot/kick_classic.json env/fake
    ln -sf ../default_robot/kick_small.json env/fake
    ln -sf ../default_robot/kick_lateral.json env/fake
    ln -sf ../default_robot/KickModelCollection.json env/fake
    ln -sf ../default_robot/VCM.json env/fake
    ln -sf ../default_robot/sigmaban.urdf env/fake
    ln -sf ../../../rhoban/model/Data/font.ttf env/fake

    
### Installing FlyCapture dependency

To use *BlackFly* cameras from *FLIR*, you have to install their software. First
clone this repository:

    git clone https://github.com/RhobanDeps/flycapture.git
    
And run the install script:

    cd flycapture
    sudo ./install_flycapture.sh
    
Maybe there will be issues with apt packages, in this case, run:

    sudo apt --fix-broken install
    
And try again (you might need to repeat the last step 2 or 3 times)

### Installing RhIO Shell

You can now compile the RhIO Shell:

    ./workspace build RhIOShell
    
Run this command to add `rhio` to your `$PATH`:

    echo export "PATH=\"\$PATH:$PWD/devel_release/lib/RhIOShell/\"" >> ~/.bashrc
    
Don't forget to re-run the shell to have the change, you should then be able to
run the `rhio` command.

### Installing RoboCup monitoring software

You can now compile the RoboCup monitoring software:

    ./workspace build monitoring_robocup
    
Run this command to add `MonitoringRobocup` to your `$PATH`:

    echo alias "MonitoringRoboCup=\"\$PWD/devel_release/lib/monitoring_robocup/MonitoringRoboCup\"" >> ~/.bashrc
    
Don't forget to re-run the shell to have the change, you should then be able to
run the `MonitoringRoboCup` command.

## Basic commands

    
### Compiling the robot program (KidSize)

Run the following to build the program:

    ./workspace build kid_size
    
### Communicating with the robot

Our robots communicate with the `10.0.0.1` ip address, so you need to configure your computer to a compatible static address like `10.0.0.2`

It is strongly recommended that you add your private key to the robot. By copying the content of `.ssh/id_rsa.pub` in the `.ssh/authorized_keys` inside the robot.
    
### Deploying the program to the robot

This will deploy the program on the robot:
    
    ./deploy
    
### Running the program on the robot

This will remotely run the program on the robot

    ./run
    
### Connecting to the robot with rhio

    rhio 10.0.0.1
    
### Saving logs with MonitoringRoboCup

Simply place a terminal with the location in which you want to save the log and run:

    MonitoringRoboCup

This will save all the content in a file named `monitoring.log` and if a webcam
is connected, it will also save images in the folder.

Note: If a file named `monitoring.log` exists in the folder, `MonitoringRoboCup`
will crash rather than overwritting current log. If you want to ecrase current
log, just remove the file `monitoring.log` to allow the program to start.

### Replaying logs with MonitoringRoboCup

Move to the folder containing the `monitoring.log` file and run:

    MonitoringRoboCup monitoring.log

## Workspace commands

To pull all the repositories:

    ./workspace pull

To build:

    ./workspace build

To build (debug):

    ./workspace build:debug

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
