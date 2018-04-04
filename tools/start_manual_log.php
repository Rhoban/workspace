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

$logDuration = askDouble("What is the required duration for log? [s]");

msg('AUTO', "Forbiding robot to track the ball");
cmd('/moves/head/trackingPeriod=-1');

msg('AUTO', "Reducing framerate to 10 FPS");
cmd('/Vision/source/FrameRate/absValue=10');


msg('FINAL', 'Press enter to activate head and start logging');
readline();
cmd('/moves/head/disabled=false');

msg("Starting manual Log for ".$logDuration." seconds");
cmd('logLocal '.$logDuration);

?>
