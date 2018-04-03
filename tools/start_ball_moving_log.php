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

positionReset(true,false);

msg('FINAL', 'Press enter to activate head and start logging');
readline();
cmd('/moves/head/disabled=false');

msg("Forcing robot to track the ball");
cmd('/moves/head/forceTrackDist=20');

msg("Activation of autoLogMode");
cmd('/Vision/autologMovingBall=true');

msg("Log has started!\nRemember to set '/Vision/autoLogMovingBall' to false after.");
?>
