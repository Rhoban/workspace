<?php

class TestCommand extends Command
{
    public function getName()
    {
        return 'test';
    }

    public function getDescription()
    {
        return array('Run the tests');
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

        Terminal::success("* Running tests for profile $profile\n");
        passthru('catkin build --make-args test -- --force-color --profile '.$profile.' '.$args);
    }
}
