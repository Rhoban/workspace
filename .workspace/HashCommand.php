<?php

class HashCommand extends Command
{
    public function getName()
    {
        return 'hash';
    }

    public function getDescription()
    {
        return array('Display the hash of last commit of given repos');
    }

    public function run(array $arguments)
    {
        foreach ($arguments as $repository) {
            echo $repository.': ';
            OS::run('cd src/'.$repository.'; git rev-parse HEAD');
        }
    }
}
