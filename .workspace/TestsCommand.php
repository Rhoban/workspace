<?php

class TestsCommand extends Command
{
    public function getName()
    {
        return 'tests';
    }

    public function getDescription()
    {
        return array('Build the tests');
    }

    public function run(array $arguments)
    {
        $args = implode(' ', $arguments);
        $profile = 'release';

        if ($this->flags) {
            if (count($this->flags) > 1) {
                Terminal::error("This only support one flag\n");
                return;
            }
            $profile = $this->flags[0];
        }

        Terminal::success("* Building tests for profile $profile\n");
        passthru('catkin build --make-args tests -- --force-color --profile '.$profile.' '.$args);
    }
}
