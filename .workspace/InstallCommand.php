<?php

class InstallCommand extends Command
{
    public function getName()
    {
        return 'install';
    }

    public function getDescription()
    {
        return array('Install a package');
    }

    public function getUsage()
    {
        return $this->getName().' [package]';
    }

    public function run(array $args)
    {
        if ($args) {
            foreach ($args as $arg) {
                $this->workspace->install($arg);
            }
        } else {
            Terminal::error('Bad usage, you should do: '.$this->getUsage()."\n");
        }
    }
}
