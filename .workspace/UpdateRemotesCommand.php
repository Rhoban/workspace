<?php

class UpdateRemotesCommand extends Command
{
    public function getName()
    {
        return 'update-remotes';
    }

    public function getDescription()
    {
        return array('Update the remotes of each dependency');
    }

    public function run(array $arguments)
    {
        foreach ($this->workspace->getRepositories() as $repository) {
            Terminal::info("Updating remotes for ".$repository->getName()."...\n");
            $repository->updateRemotes();
        }
    }
}
