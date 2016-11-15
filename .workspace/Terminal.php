<?php

class Terminal
{
    protected static function hasColor()
    {
        return true;
    }

    public static function info($message)
    {
        if (self::hasColor()) echo "\033[1;34m";
        echo $message;
        if (self::hasColor()) echo "\033[m";
    }
    
    public static function warning($message)
    {
        if (self::hasColor()) echo "\033[1;33m";
        echo $message;
        if (self::hasColor()) echo "\033[m";
    }

    public static function success($message)
    {
        if (self::hasColor()) echo "\033[1;32m";
        echo $message;
        if (self::hasColor()) echo "\033[m";
    }
    
    public static function error($message)
    {
        if (self::hasColor()) echo "\033[1;31m";
        echo $message;
        if (self::hasColor()) echo "\033[m";
    }
    
    public static function bold($message)
    {
        if (self::hasColor()) echo "\033[1m";
        echo $message;
        if (self::hasColor()) echo "\033[m";
    }

    public static function write($message)
    {
        echo $message;
    }
}
