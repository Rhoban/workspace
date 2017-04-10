<?php

class BuildCommand extends Command
{
    public function getName()
    {
        return 'build';
    }

    public function getDescription()
    {
        return array('Run the build');
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

        Terminal::success("* Running a build for profile $profile\n");
        passthru('catkin build --force-color --profile '.$profile.' '.$args);
    }
}
