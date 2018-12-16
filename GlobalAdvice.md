<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#orgheadline30">Problems</a></li>
<li><a href="#orgheadline55">Checkup of the robot (main things to check)</a></li>
<li><a href="#orgheadline112">General remarks and advice</a></li>
<li><a href="#orgheadline152">Workflow</a></li>
<li><a href="#orgheadline196"><span class="todo nilTODO">TODO</span> </a></li>
</ul>
</div>
</div>


# Problems<a id="orgheadline30"></a>

-   If the robot doesn't follow the gamecontroller

    -   The robot should not walk while you hold it off the ground

    -   Check if the robots are seen by the gamecontroller

        -   If not: check the wifi and the team id (maybe the robot id)
        -   try to `./startup` again

    -   Check if the gamecontroller referee clicks the right button

        -   Was the robot correctly put/removed from pickup?
        -   Always repeat the orders (eg. shout Pickup Red 2!)

-   If the robot "suicides" (give-up state)

    -   Check the camera

        -   Camera ethernet?
            -   Is the camera led is blinking red? (**it should be green**)
                -   Check camera network (`sudo ifconfig` => eno1 should be up with the good ip)
        -   Switch off/on the robot again

    -   Localization is very bad

        -   Check the vision
        -   Does the robot see the goal posts correctly? (see goalByDNN)
        -   Check the focus of the camera
        -   Did the robot was positioned at the good position? (a, b, c, d?)
        -   Try a `gyroTare` (will tare the IMU, robot should be in 'walk' mode, on the ground and **not moving**)

-   If the walk is unstable

    -   Check the pressure sensors

        -   Start the walk and push the robot on its side to put it on one foot
            -   the walk should stop, if not, check the pressure sensors

    -   Check the motors

    -   If pressure sensors and motors are ok

        -   Tune the walk parameters

-   Strange behavior observed on the Monitoring

    -   Robot is teleporting/oscillating? You may have several KidSize servers running on the network with the same robot id

        -   Be sure to kill all your simulations! (ie. run the `stop_fake_team.sh` script in env)
        -   Check if someone else has a KidSize server running
        -   In doubt, check that every computer wifi is shut down

    -   Everything seems ok but the robot is not moving on the monitoring

        -   Odometry may be broken, check the pressure sensors

-   The robot doesn't start when ./run

    -   try to see the log with ./out

        -   If the KidSize server crashed
            -   If you see some "json" problems
                -   Check the json
                -   Check if `"display":true` is activated in some json (it should not)

-   Problems with the motors

    -   Connect to the robot in rhio:

        -   command: `rhalCheck` (it will tell you if all the motors are currently detected)
        -   command: `rhalStatus` (it will give you a summary of all the motors, the number of errors and missing)
        -   If you see a high number of "missing" it means that the connection with this motor is lost
            -   Most probably the cable or the connector is bad and needs to be changed
        -   If you see a high number of "errors" it might be that the motor is damaged

-   Problems with the pressure sensors

    -   Connect to the robot in rhio:

        -   try the same as for motors `rhalCheck` and `rhalStatus`
        -   Try to `tare` again
        -   push a little each sensor by hand and try to tare again (the sensor should never touch anything while you use `tare`)
        -   plot the pressure values and push them by hand to see if they are all moving correctly
            -   One sensor is not moving
                -   Check the sensor connection (cable, connector)
                -   Check that the screw of the sensor are not too tight
                -   Change the sensor
            -   No sensor is moving
                -   Check the pressure electronics board connection
                    -   Try to unplug/plug again

-   If the robot freeze

    -   If you lost the connection wifi

        -   Most probably the NUC PC shut down
        -   Or the Kidsize server crashed (you should start again)

-   Vision

    -   Check the camera focus (the lens should not move easily)

    -   Check the camera parameters (gain, shutter, exposure, framerate)

    -   Check/adjust the green

    -   Check the clipping

    -   Check the configuration files (json)

        -   You may have deployed wrong parameters or wrong neural networks
        -   If the regions of interest are good (there are rectangles around the ball and the goals)
            -   You may need to adjust the neural network threshold
        -   If the regions of interest are not good (no rectangle around the ball and the goals)
            -   You may need to tune the green/white

    -   Check the horizon (see TaggedImage, the horizon line should be good and correctly move with the robot)

        -   If not: check that the IMU is working correctly
            -   plot the IMU acc and gyr values in rhio
        -   check that there is no problem with the neck motors (all screws tight, nothing bent)
            -   Put the robot in the init position, everything should be straight (the camera should be perfectly level)
                -   You may need to adjust the zero of the motor (lowlevel/head<sub>pitch</sub>/parameters/zero, then init again)
        -   check that the IMU doesn't move (open the robot and try to move the IMU pcb, **it should not move**)
            -   Notice that the IMU precise position was calibrated by us (long and difficult process) and it **should never be moved!**

# Checkup of the robot (main things to check)<a id="orgheadline55"></a>

-   Mechanical

    -   Check that all the screws are tight (in particular the Yaw axis)

    -   Check the motors

        -   Do you feel more backlash or hard position? You may need to change it.

    -   Check that the camera lens is tight (you can also check that the focus is still ok)

    -   Check the piano wire (both front and back protection)

        -   Be sure they are properly oriented

        -   They are **very important** but sacrificial part that you may need to change regularly

        -   If you need to change them, buy at least 2.5mm piano wire (or spring steel wire)

-   Electronics

    -   Check all the cables

        -   No cut cable? In case of doubt change it!

        -   No loose connector? In case of doubt change it!

        -   Go in rhio and try `rhalScan` and `rep rhalStatus`, move the cables and the motors. There should be no errors or missing appearing

    -   Check that all the pressure sensors are ok

        -   If some sensor is not reliable, change it

    -   Check that the IMU is ok and not moving

-   Parameters

    -   Walk

        -   If the robot is not very stable (you see some bad oscillations, it falls very often)

            -   cf. [Walk is unstable](#orgheadline11)

            -   You may tune the walk parameters again

    -   Kick

        -   If the robots falls when kicking you may need to adjust the kick motion again

# General remarks and advice<a id="orgheadline112"></a>

-   Always use good quality materials (tools, cables&#x2026;)

-   At the robocup don't use any personal wifi

    -   All wifi should be **shut down** (computer, phone&#x2026;)

    -   Only the fields wifi is allowed

    -   Never connect to the robot in wifi

        -   In match
            -   Never ssh a robot in wifi (**FORBIDDEN!**)
            -   Never never connect rhio to a robot in wifi (**FORBIDDEN!**)
            -   Always Monitor. Monitoring is ok (only listening)

-   Always change the battery at half game

-   Always make a startup at half game

-   Always have someone running the Monitoring software

    -   You should monitor each half in different folder

    -   He has to check that the video is always pointing towards the ball

    -   He should be careful not having someone in front of the camera but he **can not** ask to the referee to move

-   Always have someone behind the gamecontroller to check everything

-   Unless for initial placing (game startup) always place the robot on the line, in front of the penalty mark

-   Always be sure all the robots have been "deploy" with the same version of the code/env (the last working one)

    -   The "master" branch should always be good (it should compile and work)

-   Always be sure to plug a LiPo beeper to the battery

-   If no robot is ready to play

    -   Ask for a timeout!

-   If one robot is not ready to play

    -   Always ask for a pickup

-   Regularly check the robots

-   Robocup setup days

    -   These are usually very hectic days, you may have a lot of problems to solve!

    -   Check that the robots are in good working condition (the travel may damage the robots)

        -   All the cables and connections, all the screws, all the parts (nothing broken or bent)

    -   Organise your table for efficient robot maintenance (mechanics, electronics, battery charging&#x2026;.)

        -   Don't forget to bring all the tools and spare parts including motors, cables, screws&#x2026;

    -   As soon as possible go to the robot qualification

        -   The Sigmaban+ robots are ok for the 2019 rules but will need modifications for 2020 (you only need to change the color markers)
        -   Be aware that you may need to modify the robot to comply to the rules

    -   Check the fields

        -   Measure the fields (cf. Robocup rules) and adapt the configuration (file: env/common/field<sub>dimensions</sub>)
        -   Check the grass and the lines, you may need to adapt (walk, foot studs, vision&#x2026;)
        -   Check and configure the wifi for each field

    -   As soon as possible book a field to take a lot of logs

        -   Adapt the camera parameters (In Vision/source, the gain, shutter, exposure, framerate&#x2026;)
        -   You will probably need to train some new neural network (goal posts&#x2026;)

    -   As soon as you can (when you are ready) book a field to make a test match

        -   Don't forget to activate the logs and the Monitoring to be able to replay and debug on your computer

    -   Do as much work as possible during the setup days (during the competition you will have less time)

-   Procedure to start a match

    -   **Everything** should be ready 5 minutes before the start!

    -   At least one hour before the match

        -   Go meet the opponent team and referees to agree on color markers and field choice

        -   change the color markers if needed

    -   At your table:

        -   Be sure that the "Master" branch is **clean and up to date** for everyone

        -   You should start synchronizing the code and the env **at least 30 minutes** before

        -   **compile**

        -   **deploy** (test the robot?)

    -   20 minutes before the match

        -   Go install the team to the field with all the materials you need (batteries, tools, computers, robots&#x2026;)

        -   Check that the GameController is correctly configured

        -   Check that the robot can connect to the wifi (you may run the wifi script, run and see the GameController)

    -   5 minutes before the match

        -   Start the robots (run, startup)

        -   Quickly check again that everything is ok

        -   Position the robots on their designated positions

        -   Start the Monitoring

        -   Enjoy the match&#x2026;

    -   At the half time:

        -   Change the batteries

        -   Check if everything is ok

        -   Startup again

        -   Don't forget to change the side!

        -   Save the monitoring data to a folder (jpegs and monitoring.log) and run the Monitoring for the second half

# Workflow<a id="orgheadline152"></a>

-   Working with the robots

    -   Configure your network to be able to connect to the robot (you only need to do that once per robot)

        -   You need to configure an ethernet network on your computer to connect to the robot (static address, usually 10.0.0.2)

        -   copy your ssh key to the robot (you should do that for every robot)

            -   `ssh-copy-id rhoban@10.0.0.1` (for now the robot's login is 'rhoban' but you may change it)

    -   You always need to be 2 persons to work on a robot (always someone to hold it in case of failure)

        -   Try to avoid to make the robot fall (it can damage it prematurely)

-   Working with git

    -   Some tutorials

        -   <https://rogerdudler.github.io/git-guide/>
        -   <https://marklodato.github.io/visual-git-guide/index-en.html>
        -   <https://services.github.com/on-demand/downloads/github-git-cheat-sheet.pdf>
        -   <http://ndpsoftware.com/git-cheatsheet.html>
        -   <https://git-scm.com/doc/ext>
        -   You may want to try a graphical interface: <https://git-scm.com/download/gui/linux>

    -   **"Master" should always be GOOD!**

        -   It should always compile and working good
        -   It will be the version you deploy to the robot

    -   Every time you test/develop a new thing

        -   make a new branch (for example call it MyTestbranch) and directly move to it (`git checkout -b MyTestBranch`)

        -   be sure you are working in your branch (`git branch` to show the current branch)

            -   to move to the branch MyTestBranch: `git checkout MyTestBranch`

            -   to move back to the Master branch: `git checkout master`

        -   if you need to add some new file to the repository: `git add MyNewFile`

        -   don't forget to commit your work:

            -   you can also chose the file you commit with: `git add YourFile`

            -   then `git commit -m"A comment about the commit"`

        -   to pull data from the master branch on the server (to synchronize with other):

            -   `git checkout master` (to go into the master branch)

            -   `git pull origin master`

        -   to push data from your branch MyTestBranch to the server (to save your work on the server): `git push origin MyTestBranch`

        -   when you are happy with your new branch and want to merge it into master

            -   first merge Master into your branch: be sure to be in your branch and `git merge master`

            -   check that everything compiles and work as intended

            -   then if everything is ok, merge you branch MyTestbranch to the Master branch:

            -   go back to the Master branch: `git checkout master`

            -   then merge your branch MyTestbranch: `git merge MyTestbranch`

            -   you can now push into master to share your work with everyone: `git push origin master`

    -   If you have a merge conflict

        -   don't panic!

        -   take your time to understand what is happening. It may be only a small problem

        -   try `git status` to see which files are in conflict

        -   try to find/ask who modified these files to understand

        -   try to see the diff with `git diff TheFileInConflict` to see if there is only a small conflict

        -   try to edit and solve the conflict by hand

        -   if there is too much conflict you can try to resolve them with a merge tool (like kdiff3): `git mergetool`

        -   when the conflict is solved you can commit and push

# TODO <a id="orgheadline196"></a>

-   It would be a good thing to replace all the "Rhoban" specific stuffs

    -   Fork all the Rhoban repositories and change your workspace configuration to use them instead of the Rhoban's ones

    -   Use your fork of the workspace repository

        -   Change the robot names everywhere (replace Tom, Nova&#x2026;)

        -   Be sure to change the team ID everywhere

    -   Change the login of the robots. Currently it is 'rhoban' (with the password 'rhoban')

    -   Change the login of the robots on the scripts (deploy etc&#x2026;)

    -   Change the logo on the Monitoring

-   If you make a new robot

    -   If the size/shape is different, don't forget to update the urdf model! (`sigmaban.urdf` in env)

    -   You need to install a new computer (for now we use a Intel NUC)

        -   Configure the BIOS to auto boot on AC power plug

        -   The simple solution would be to clone the SSD hard drive of on existing computer (use a M.2 SSD to USB converter)

            -   Copy the hard drive of one of the existing robot to a file (see: <https://wiki.archlinux.org/index.php/Dd#Disk_cloning_and_restore>)

                -   dd if=/dev/sdX of=RobotSystem.img bs=128K conv=noerror,sync status=progress (**replace sdX by the device you want to clone**)

            -   Then can use the file RobotSystem.img for all your new robots

                -   dd if=RobotSystem.img of=/dev/sdX.img bs=128K conv=noerror,sync status=progress (**replace sdX by the device you want to create**)

            -   Change the hostname (in `/etc/hostname`) to put the name of your robot and also in `/etc/hosts/` (127.0.1.1 YourHostName)

            -   Eventually change the udev rules in `/etc/udev/rules.d/45-maple.rules`

                -   Plug your DXLBoard and `dmesg` you should see the Rhoban device. Use the VendorId and ProductId to create a new rule if it doesn't exist (with symlink maple)

        -   If you want to install from scratch:

            -   Install a debian 9 server

            -   Create a "rhoban" user (you may want to change that)

            -   change the hostname

            -   Add the udev rule

            -   Configure grub to autoboo

            -   configure the network (the simple way is to copy the file `/etc/network/interfaces` from another robot)

        -   Create a directory for your robot in env (you can copy one of the existing robot)

        -   You should be sure the low level configuration file `rhal.json` is correct for your robot (motors ID)

        -   You should configure your new camera (check the documentation in `Vision/Readme`)

    -   You should calibrate your IMU precisely!

        -   The IMU should be perfectly level and correctly oriented with upper torso plate of the robot

            -   You should put the torso on a perfectly level position and adjust the IMU position until everything is correct (plot the IMU sensor to help)

            -   If you cannot adjust the IMU position you can modify the file `VCM.json` to correct the IMU offset in software

                -   Draw a visible line (ie. on a goal post) at the height of the robot's camera

                -   Be sure that the mechanics is perfectly ok (in the 'init' position the robot should be vertical

                -   camera offsets should be 0 unless you can optimize the calibration parameters for different robot positions

                -   the IMU offset (roll and pitch) should be adjusted in order to get a perfectly horizontal line

                    -   First adjust the roll (make sure the robot is in 'init' position with the head perfectly level)

                        -   adjust the parameter until the horizon line is level (you need to re run the server to take it into account)

                    -   then adjust the pitch to align the horizon line to the mark

    -   If you change the camera/lens you may need to calibrate it (file `camera_calib.yml` using opencv calibration)

        -   You may also need to adjust the camera angular field of view parameters in `VCM.json` (camera<sub>pan</sub>, camera<sub>tilt</sub>)
