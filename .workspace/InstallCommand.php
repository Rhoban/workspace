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
        $tag = "master";
        if ($this->flags) {
            if (count($this->flags) > 1) {
                Terminal::error("This only support one flag");
                return 1;
            }
            $tag = $this->flags[0];
        }
        if ($args) {
            foreach ($args as $arg) {
                $this->workspace->install($arg, $tag);
            }
        } else {
            foreach ($this->workspace->getRepositories() as $repository) {
                $this->workspace->install($repository->getName(), $tag);
            }
        }
    }
}
