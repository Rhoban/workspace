<?php

class GitCommand extends Command
{
    public function getName()
    {
        return 'git';
    }

    public function getDescription()
    {
        return array('Run the build');
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
        $args = implode(' ', $arguments);
        foreach ($this->workspace->getPackages() as $package) {
            $repositories[$package->getRepository()] = true;
        }
        foreach ($repositories as $repository => $true) {
            $this->retryCmd("Applying git cmd '".$args."' on $repository", 'cd src/'.$repository.'; git '.$args);
        }
    }
}
