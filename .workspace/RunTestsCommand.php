<?php

class RunTestsCommand extends BuildCommand
{
    public function getName()
    {
        return 'run_tests';
    }

    public function getDescription()
    {
        return array('Run tests');
    }

    public function run(array $arguments)
    {
        array_unshift($arguments, '--interleave', '--catkin-make-args run_tests', '--');
        return parent::run($arguments);
    }
}