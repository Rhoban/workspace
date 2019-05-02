#!/usr/bin/php

<?php

$host = '10.0.0.1';
if (count($argv) >= 2) {
  $host = $argv[1];
}

$viveServer=`ps aux|grep vive_server.py|grep -v grep|awk '{print $2}'`;
if (!$viveServer) {
  die("WARNING: Vive server is not running!\n");
}

include "robot_tools.php";

// We want to make sure that the robot detects when it is handled to avoid
// logging image in this case
// requestTare();

$logDuration = askDouble("What is the required duration for log? [s]");

msg('AUTO', "Running NTP sync");
echo `ssh rhoban@$host sudo ifconfig wlan0 down`;
echo `ssh rhoban@$host sudo ntpdate -b 10.0.0.2`;

msg('AUTO', "Forbiding robot to track the ball");
cmd('/moves/head/trackingPeriod=-1');

msg('AUTO', "Reducing head max speed");
cmd('/moves/head/maxSpeed=100');

msg('AUTO', "Reducing framerate to 25 FPS");
cmd('/Vision/source/FrameRate/absValue=25');

msg('AUTO', "Reducing handledDelay");
cmd('decision/handledDelay=0.01');

msg('FINAL', 'Press enter to activate head and start logging');
readline();
cmd('/moves/head/disabled=false');

msg('LOG', "Starting manual Log for ".$logDuration." seconds");
cmd('/localisation/consistency/enabled=0');
cmd('customReset 0 0 0');
cmd('logLocal '.$logDuration);
cmd('head');