<?php

class UnshallowCommand extends Command
{
    public function getName()
    {
        return 'unshallow';
    }

    public function getDescription()
    {
        return array('Unshallows a repository (will fetch the history,',
                    'getting it as it was not cloned using depth=1)');
    }

    public function getUsage()
    {
        return $this->getName().' [repository]';
    }

    public function run(array $args)
    {
        if (!$args) {

        } else {
            foreach ($args as $arg) {
                Terminal::info("* Unshallowing $arg\n");
                $repository = new Repository();
                $repository->setRemote($arg);
                $repository->unshallow();
            }
        }
    }
}
