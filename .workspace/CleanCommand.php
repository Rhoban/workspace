<?php

class CleanCommand extends Command
{
    public function getName()
    {
        return 'clean';
    }

    public function getDescription()
    {
        return array('Cleans the build');
    }

    public function run(array $arguments)
    {
        $profile = 'release';

        if ($this->flags) {
            if (count($this->flags) > 1) {
                Terminal::error("This only support one flag\n");
                return;
            }
            $profile = $this->flags[0];
        }

        OS::run('catkin clean --yes --profile '.$profile);
    }
}
