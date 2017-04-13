<?php

class OS
{
    public static function run($command)
    {
        system($command, $ret);

        return $ret;
    }
}
