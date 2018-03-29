<?php

function msg($phase, $msg) {
    echo "\n\e[1m$phase: $msg\e[m\n";
}
function prompt($phase, $msg, array $possibilities) {
    $pos = implode(', ', $possibilities);
    while (true) {
        echo "\n\e[1m$phase: $msg\e[m (".$pos.")\n";
        echo "> ";
        flush();
        $m = strtolower(trim(readline()));
        if (in_array($m, $possibilities)) {
            return $m;
        }
        echo "\e[1;31mYou should answer one of the following: ".$pos."\e[m\n";
    }
}
function question($phrase, $msg) {
    return prompt($phrase, $msg, ['y', 'n']) == 'y';
}
function cmd($cmd, $display = true) {
    global $host;
    $result = trim(`rhio $host $cmd`);
    if ($display) echo "$result\n";
    return $result;
}
function isHandled() {
    $r = cmd('/decision/handled');

    return $r == '/decision/handled=true';
}

function requestTare() {
    msg('TARE', 'Hold me in the air and press enter');
    readline();
    cmd('tare');
    cmd('rhalSaveConf rhal.json');
}

function requestGyroTare() {
  while (true) {
    msg('GYROTARE', 'Put me on the floor now and press enter');
    readline();
    cmd('rhalGyroTare');
    cmd('rhalSaveConf rhal.json');

    msg('CHECK', 'Checking the pressure');
    if (isHandled()) {
      if (question("\e[31mERROR", 'Decision said I am handled when I should be on the floor, continue anyway?')) {
        break;
      }
    } else {
      break;
    }
  }
}

// TODO implement some kind of check here
function askDouble($message) {
  echo "\n".$message."\n";
  return floatval(readline());
}

function positionReset($customizePosition = true,$customizeDev=false) {
  msg("POS_RESET", "Customizing the position reset");
  $x = 0; $y = 0; $dir = 0; $posDev = 5; $dirDev = 2;
  if ($customizePosition) {
    $x = askDouble("Enter value for: playerX [m]");
    $y = askDouble("Enter value for: playerY [m]");
    $dir = askDouble("Enter value for: playerDir [deg]");
  }
  if ($customizeDev) {
    $posDev = askDouble("Enter value for: posStddev [m]");
    $dirDev = askDouble("Enter value for: dirStddev [deg]");
  }
  cmd("customReset ".$x." ".$y." ".$dir." ".$posDev." ".$dirDev);
}

?>