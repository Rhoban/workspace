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

    protected function retryCmd($title, $cmd)
    {
        $retry = false;
        do {
            Terminal::success("* $title\n");
            $return = OS::run($cmd);
            $retry = false;
            if ($return) {
                if (!Prompt::ask('It appear that the operation was not successful, continue anyway (n=retry) ?', false)) {
                    $retry = true;
                }
            }
        } while ($retry);
    }

    public function run(array $arguments)
    {
        $repositories = array();
        $this->retryCmd("Self updating", 'git pull');
        foreach ($this->workspace->getPackages() as $package) {
            $repositories[$package->getRepository()] = true;
        }
        foreach ($repositories as $repository => $true) {
            $this->retryCmd("Updating $repository", 'cd src/'.$repository.'; git pull');
        }
    }
}
