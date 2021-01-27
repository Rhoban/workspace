# catkin workspace with packages manager

## Setup of the system

### Recommended Operating System

The recommended operating system to run this version of the software is `Ubuntu
20.04 Focal Fossa` using other OS might result on issues with some of the
packages required.

### Installing APT dependencies

First of all, you will need to install required packages:

    sudo apt-get install gcc cmake git libtinyxml-dev libncurses5-dev\
        php php-cli php-xml libv4l-dev gnuplot-qt \
        python3-pip python3-empy python3-setuptools python3-nose chrpath ffmpeg libudev-dev \
        libsfml-dev libconsole-bridge-dev freeglut3-dev libx11-dev libxrandr-dev libfreetype6-dev \
		libjsoncpp-dev libprotobuf-dev protobuf-compiler libgtest-dev libtclap-dev \
        qt5-default qtmultimedia5-dev libqt5webkit5-dev libopencv-dev libeigen-dev
        
### Installing catkin

    sudo pip3 install -U mock
    sudo pip3 install git+https://github.com/catkin/catkin_tools.git

### Installing OpenCV with DNN support

Ubuntu 20.04 has native package of OpenCV 4.2.0 which supports DNN.

### Installing FlyCapture dependency (DEPRECATED)

**NOTE: Flycapture is going to be discontinued and is not maintained for Ubuntu
20.04, building support for FLIR camera will require to move to Spinnaker SDK.**

### Setting up your Github account with your public key

Since the `workspace` manager handle dozens of repositories at once, it is much
more convenient to use SSH keys.  If you don't have a one, generate one using:

    ssh-keygen -t rsa
    
Sign in on your GitHub account and go to Settings, and then "SSH and GPG
keys". Click "New SSH key" and copy the content of `.ssh/id_rsa.pub` in the key
field, choose any name you want and validate the new key.

### Setting up the workspace (user)

**This part is not for Rhoban Developers**

The latest public release of _Rhoban_ source code is tagged under different
repositories under the tag `public_2019` this tag is based on the code we
used during the final of the RoboCup 2019 with the following modifications:

- Showing who is the captain in Monitoring Software
- Solving several issues regarding DNN training and use
- Publishing improved DNN

Clone the latest public release of `workspace` repository and move to it:

    git clone -b public_2019 https://github.com/rhoban/workspace.git
    cd workspace

Then, run the setup:

    ./workspace setup

You can then install the latest public release of all the rhoban source code:

    ./workspace install:public_2019 rhoban/kid_size_public.git
    ./workspace install:public_2019 rhoban/env_public.git

In order to use the latest public release for all repositories, each time a
`./workspace install` command is specified, rather use:
`./workspace install:public_2019`

Notes:

- You should make a fork of `rhoban/env_public` in order to have the configuration
for your own robots.
- While installing, optional packages will be proposed, you can use the default
option for all of them

### Setting up the workspace (rhoban developer)

Clone the latest release of `workspace` repository and move to it:

    git clone https://github.com/rhoban/workspace.git
    cd workspace

Then, run the setup:

    ./workspace setup

You can then install the latest public release of all the rhoban source code:

    ./workspace install rhoban/kid_size.git
    ./workspace install rhoban/environments.git

### Adding Rhoban binaries to your path

Run this command to add all rhoban binaries to your `$PATH`:

    echo export "PATH=\"\$PATH:$PWD/bin\"" >> ~/.bashrc
    
Don't forget to re-run the shell to have the change applied. Once you build the
rhoban tools, you should be able to use them without specifying the full path.

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

### Workspace dependencies

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

## Rhoban basic commands

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

### Working on robot logs

All of this commands have to be issued while located in the `env/fake` folder.

#### Preparing a log environment

In order to work with a specific log, use:

    ./prepare.py <path_to_log>

This command also set the serial_number of the tracker of the robot if available
in the `metadata.json` file.

#### Extracting ground truth from Vive

It is possible to extract ground truth based on multiple logs with HTC Vive tracker

   ln -sf ../common/vive_roi_extractor.json vision_config.json
   ./extract_vive_patches.py <log1> <log2> ...

In this case, all the data will be placed in the folder `vive_data`. It is
important not to rewind the video (using key 'p') or update it stationary (using
key 'u') while you extracting log data, because it has a risk of duplicating data.
If you want to investigate on vive issues

#### Compressing vive data

It is possible to collect them in compressed `tar.gz` files to send them on
distant servers faster:

  ./compress_vive_data.sh

This command will use the data in the folder `vive_data`. The patches used for
classification will be stored in file `classification_data.tar.gz` and the
images with the position of the objects will be stored in
`attention_data.tar.gz`.

#### Labelling videos

This procedure is still evolving yet and will be made public along with data
soon.

### Using PyBullet viewer

The code allowing to display the robot with `pybullet` can be cloned outside of workspace:

    git clone git@github.com:rhoban/sigmaban_pybullet.git

It requires some dependencies

    sudo apt install python3-pip
    sudo pip3 install -U zmq pybullet numpy protobuf

In order to use it, you have to enable publishing of the model using RhIO: set `model/publish=true`

Then you can launch the viewer from the sigmaban_pybullet folder

    python3 client.py

### Using rhoban_monitoring tool

The rhoban monitoring tool can be installed as following:

    ./workspace install rhoban/qt_monitoring

In order to view a game in progress, move to the folder where you want to write
the log and use the following command:

    rhoban_monitoring -l

A folder with a name based on current date will be created. You can replay it by
moving in the folder and running:

    rhoban_monitoring -r

For custom execution and extended options (name of the robots, cameras, etc...),
you can edit a json configuration file (examples available in the
`qt_monitoring` repository) and launch the element as follows:

    rhoban_monitoring -m manager.json

### Synchronising robot clocks

Documentation: [doc/synchronisation.md](doc/synchronisation.md).

### Training new DNN

The code used to train multi-class DNN classifiers is independent from workspace
and can be found on:

- [https://www.github.com/rhoban/tf_deep_vision_public](rhoban/tf_deep_vision_public) for use
- [https://www.github.com/rhoban/tf_deep_vision](rhoban/tf_deep_vision) for rhoban developers
