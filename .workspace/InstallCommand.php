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
            foreach ($this->workspace->getRepositories() as $repository) {
                $this->workspace->install($repository->getName());
            }
        }
    }
}
