<?php

class UpstreamCommand extends Command
{
    public function getName()
    {
        return 'upstream';
    }

    public function getDescription()
    {
        return array('Change the used upstream for each repository');
    }

    public function run(array $arguments)
    {
        if (count($arguments) != 1) {
            Terminal::error("Usage: upstream [name]\n");
        } else {
            $upstream = $arguments[0];
            foreach ($this->workspace->getRepositories() as $repository) {
                Terminal::info("Setting upstream to $upstream for ".$repository->getName()."\n");
                $repository->setUpstream($upstream);
            }
        }
    }
}
