<?php

class BuildTestsCommand extends BuildCommand
{
    public function getName()
    {
        return 'build_tests';
    }

    public function getDescription()
    {
        return array('Build tests');
    }

    public function run(array $arguments)
    {
        array_unshift($arguments, '--catkin-make-args tests', '--');
        return parent::run($arguments);
    }
}
