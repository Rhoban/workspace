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

requestGyroTare();

msg('SETUP', 'drastically reducing noise on localisation');
cmd('/localisation/field//RobotController/angleExploration=0.01');
cmd('/localisation/field//RobotController/posExploration=0.0001');

msg('SETUP', 'Forcing robot to track the ball');
cmd('/moves/head/forceTrackDist=20');
cmd('/moves/head/disabled=false');

positionReset(true,false);

$logDuration = askDouble("What is the required duration for log? [s]");

msg('FINAL', 'Press enter to start logging');
readline();

msg('INFO', "Starting manual Log for ".$logDuration." seconds");
cmd('logLocal '.$logDuration);

// Outdated
//msg("Activation of autoLogMode");
//cmd('/Vision/autologMovingBall=true');
//msg("Log has started!\nRemember to set '/Vision/autoLogMovingBall' to false after.");
?>
