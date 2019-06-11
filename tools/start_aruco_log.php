#!/usr/bin/php

<?php

$host = '10.0.0.1';
if (count($argv) >= 2) {
  $host = $argv[1];
}

include "robot_tools.php";

msg('INIT', 'Press enter to run init');
readline();
cmd('init');

msg('INIT', 'Press enter to run walk');
readline();
cmd('walk');

// We want to make sure that the robot detects when it is handled to avoid
// logging image in this case
requestTare();

// Since we log robot in field, gyroTare might be useful
requestGyroTare();

$logDuration = askDouble("What is the required duration for log? [s]");

msg('AUTO', "Forcing the robot to scan for the ball");
cmd('/moves/head/forceScanBall=1');

msg('AUTO', "Slowing down scan speed");
cmd('/moves/head/maxSpeed=20');

msg('AUTO', "Configuring scan trajectory.");
cmd('/moves/head/minOverlap=40');
cmd('/moves/head/minTilt=-30');
cmd('/moves/head/maxTilt=80');
cmd('/moves/head/maxPan=150');

msg('AUTO', "Reducing framerate to 10 FPS");
cmd('/Vision/source/FrameRate/absValue=10');

msg('AUTO', "Increasing shutter to 10");
cmd('/Vision/source/Shutter/absValue=10');

msg('AUTO', "Reducing gain to 10");
cmd('/Vision/source/Gain/absValue=0');

msg('FINAL', 'Press enter to activate head and start logging');
readline();
cmd('/moves/head/disabled=false');

msg('LOG', "Starting manual Log for ".$logDuration." seconds");
cmd('/localisation/consistency/enabled=0');
cmd('customReset 0 0 0');
cmd('logLocal '.$logDuration);

?>
