#!/usr/bin/php

<?php

$host = '10.0.0.1';
if (count($argv) >= 2) {
  $host = $argv[1];
}

include "robot_tools.php"

msg('INIT', 'Press enter to run init');
readline();
cmd('init');

msg('Overwriting head parameters for visual compass');
cmd('/moves/head/forceCompass=true');
cmd('/moves/head/compassMaxPan=210');
cmd('/moves/head/vcMaxSpeed=20');

msg('Reducing framerate to 5 FPS');
cmd('/Vision/source/FrameRate/absValue=5');

msg('Starting manual Log for 10 seconds');
cmd('logLocal 15');
