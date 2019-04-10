# Vive process

## 1) Prepare the setup

### 1.1) Synchronize using ntp

The computer hosting the vive server can run an NTP server using the `ntp.conf`
file in this folder.

Then, use `ntpdate` with the `-b` argument (force immediate update) on the robot
with your IP, like:

  sudo ntpdate -bd 10.0.0.2

### 1.2) Calibrate the field using vive controller

After starting SteamVR, and having at least a controller plugged.

Run:

  ./vive_field_calibration.py

And click the calibration points to calibrate the vive

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

Download the logs on your computer:

  ./tools/downloadViveLog.sh

This will be made in `vive_logs` directory.