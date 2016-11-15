<?php

class PackagesCommand extends Command
{
    public function getName()
    {
        return 'packages';
    }

    public function getDescription()
    {
        return array('Lists the packages');
    }

    public function run(array $arguments)
    {
        $count = 0;
        foreach ($this->workspace->getPackages() as $package) {
            $count++;
            Terminal::info("* ".$package->getName());
            Terminal::write(" (".$package->getDirectory().")\n");
        }
        Terminal::info("Found $count packages.\n");
    }
}
