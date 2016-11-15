<?php

class PullCommand extends Command
{
    public function getName()
    {
        return 'pull';
    }

    public function getDescription()
    {
        return array('Pull all the repositories');
    }

    public function run(array $arguments)
    {
        $repositories = array();
        foreach ($this->workspace->getPackages() as $package) {
            $repositories[$package->getRepository()] = true;
        }
        foreach ($repositories as $repository => $true) {
            Terminal::success("* Updating $repository...\n");
            OS::run('cd src/'.$repository.'; git pull');
        }
    }
}
