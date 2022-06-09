# Rhoban's workspace for Kid Size league

## Setup of the system

### Recommended Operating System

The recommended operating system to run this version of the software is `Ubuntu
18.04 Bionic Beaver` using other OS might result on issues with some of the
packages required.

### Installing APT dependencies

First of all, you will need to install required packages:

    sudo apt-get install gcc cmake git libtinyxml-dev libncurses5-dev \
        php php-cli php-xml libv4l-dev gnuplot-qt \
        python3-pip python3-empy python3-setuptools python3-nose chrpath ffmpeg libudev-dev \
        libsfml-dev libconsole-bridge-dev freeglut3-dev libx11-dev libxrandr-dev libfreetype6-dev \
		    libjsoncpp-dev libprotobuf-dev protobuf-compiler libgtest-dev libtclap-dev \
        qt5-default qtmultimedia5-dev libqt5webkit5 \
        libopencv-dev liburdfdom-dev
    
### Installing FlyCapture dependency

To use *BlackFly* cameras from *FLIR*, you have to install their software. First
clone this repository outside of the workspace folder:

    git clone https://github.com/RhobanDeps/flycapture.git

And run the install script:

    cd flycapture
    sudo ./install_flycapture.sh
    
Maybe there will be issues with apt packages, in this case, run:

    sudo apt --fix-broken install

And try again (you might need to repeat the last step 2 or 3 times)

### Installing OpenVINO

Install OpenVINO for Ubuntu:
https://docs.openvino.ai/latest/openvino_docs_install_guides_installing_openvino_linux.html#doxid-openvino-docs-install-guides-installing-openvino-linux

Don't forget to install dependencies, drivers, and add setupvars.sh to your bashrc.


### Setting up your Github account with your public key

Since the `wks` manager handle dozens of repositories at once, it is much
more convenient to use SSH keys.  If you don't have a one, generate one using:

    ssh-keygen -t rsa
    
Sign in on your GitHub account and go to Settings, and then "SSH and GPG
keys". Click "New SSH key" and copy the content of `.ssh/id_rsa.pub` in the key
field, choose any name you want and validate the new key.

### Setting up the workspace (rhoban developer)

First, install `wks`:

    pip install wks

And then run:

    wks install rhoban/kid_size

This will install the upstream repositories. You can now build using:

    wks build


### Adding Rhoban binaries to your path

Binaries are built in `build/bin`.

Run this command to add all rhoban binaries to your `$PATH`:

    echo export "PATH=\"\$PATH:$PWD/build/bin\"" >> ~/.bashrc
    
Don't forget to re-run the shell to have the change applied. Once you build the
rhoban tools, you should be able to use them without specifying the full path.

## Workspace commands

To pull all the repositories:

    wks pull

To build:

    wks build

To build (debug), manually create a `build_debug` directory and simply run `cmake ../src`,
then edit the proper CMakeCache variables using `ccmake .` to set the build type to `DEBUG`.

To build just a specific package:

    wks build [package]

### Workspace dependencies

Have a look at [wks documentation](https://github.com/rhoban/wks#wks-simple-cmake-workspace-manager) for
more details about how dependencies are handled.

## Rhoban basic commands

### Compiling the robot program (KidSize)

Run the following to build the program:

    wks build KidSize

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
