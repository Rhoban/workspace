<?php

/**
 * Simple autoloader that loads the class Class from
 * Class.php
 */
spl_autoload_register(function($cName) {
    $filename = __DIR__. '/' . $cName . '.php';
    if (file_exists($filename)) {
        require_once($filename);
    }
});
