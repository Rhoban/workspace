#!/usr/bin/php

<?php

$host = '10.0.0.1';
if (count($argv) >= 2) {
  $host = $argv[1];
}

include "robot_tools.php";

requestTare();
requestGyroTare();

// Config for static calib with slow head motion
cmd('/moves/arucoCalibration/hipPitchAmplitude=0');
cmd('/moves/arucoCalibration/losangeAmplitude=0');
cmd('/moves/arucoCalibration/logDuration=40');
cmd('/moves/arucoCalibration/headSpeed=5');
cmd('/moves/head/minOverlap=30');
cmd('/moves/head/maxPan=120');
cmd('/Vision/source/FrameRate/absValue=5');// Reducing frameRate because speed is slow
cmd('/Vision/source/FrameRate/absValue=5');// Reducing frameRate because speed is slow

?>