# Vive process

## 1) Prepare the setup

### 1.1) Synchronize using ntp

The computer hosting the vive server can run an NTP server using the `ntp.conf`
file in this folder.

The NTP sync will be done at the begining of each log using `start_vive_log` (see below).

### 1.2) Calibrate the field using vive controller

After starting SteamVR, and having at least a controller plugged.

Run:

  ./vive_field_calibration.py

And click the calibration points to calibrate the vive. If the controller vibrates,
it indicates that there was an error and you should start over.

You can check that everything is OK by running:

  ./vive_buller.py

And visualize

## 2) Take logs

After the steps in 1) are achieved, you can repeat the following steps
multiple times:

### 2.1) Tag the ball positions

Run:

  ./vive_tag_positions.py

And click all the ball positions

### 2.2) Run the vive server and log the vive messages

Run the server:

  ./vive_server.py

And the log on the robot:

  ./tools/start_vive_log.php

And do the log

### 2.3) Download the logs

Stop the vive server and download the logs on your computer:

  ./tools/downloadViveLog.sh

This will be made in `vive_logs` directory.