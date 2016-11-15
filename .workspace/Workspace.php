<?php

class Workspace
{
    protected $directory;
    protected $commands = array();
    protected $packages = array();

    public function __construct($directory)
    {
        $this->directory = $directory;

        $this->addCommand(new SetupCommand);
        $this->addCommand(new InstallCommand);
        $this->addCommand(new BuildCommand);
        $this->addCommand(new PackagesCommand);

        $this->updatePackages();
    }

    protected function addCommand(Command $command)
    {
        $command->setWorkspace($this);
        $this->commands[$command->getName()] = $command;
    }

    public function help()
    {
        Terminal::info("workspace manager for catkin v0.1\n");
        Terminal::info("\n");
        foreach ($this->commands as $command) {
            Terminal::bold($command->getName());
            Terminal::info(": usage: ./workspace ".$command->getUsage()."\n");
            Terminal::write('    '.implode("\n    ", $command->getDescription())."\n\n");
        }
    }

    public function run(array $args)
    {
        if (count($args)) {
            $parts = explode(':' , array_shift($args));
            $command = array_shift($parts);
            if (isset($this->commands[$command])) {
                $this->commands[$command]->setFlags($parts);
                try {
                    if ($this->commands[$command]->run($args)) {
                        exit(10);
                    }
                } catch (\Exception $error) {
                    Terminal::error("Error: ".$error->getMessage()."\n");
                }
                return;
            } else {
                Terminal::error("Error: Unknown command $command\n");
                return;
            }
        }

        $this->help();
    }

    protected $installed = array();

    public function install($repository)
    {
        // Retrieving the directory name
        $parts = explode('/', $repository);
        $directory = $parts[count($parts)-1];

        if (isset($this->installed[$directory])) {
            return;
        }
        $this->installed[$directory] = false;

        if (substr($directory, -4) == '.git') {
            $directory = substr($directory, 0, -4);
        }

        if (!is_dir('src/'.$directory)) {
            Terminal::success("* Installing $repository in $directory\n");
            OS::run('cd src/; git clone '.$repository.' '.$directory.'; cd '.$directory.';
            git checkout -b catkin origin/catkin');
            $this->updatePackages();
        } else {
            Terminal::info("* Repository $directory already installed\n");
        }

        Terminal::info("* Scanning dependencies for $directory...\n");
        $toInstall = array();
        foreach ($this->packages as $package) {
            if ($package->getRepository() == $directory) {
                foreach ($package->getDependencies() as $dependency) {
                    $toInstall[] = $dependency;
                }
            }
        }
        foreach ($toInstall as $install) {
            $this->install($install);
        }
    }

    protected function scanPackages($dir, $repository = null)
    {
        if (file_exists($dir . '/package.xml')) {
            $this->packages[] = new Package($repository, $dir);
        } else {
            foreach (scandir($dir) as $subdir) {
                if ($subdir != '.' && $subdir != '..' && $subdir != 'catkin') {
                    $rep = $subdir;
                    $subdir = $dir . '/' . $subdir;
                    if (is_dir($subdir)) {
                        $this->scanPackages($subdir, $repository ?: $rep);
                    }
                }
            }
        }
    }

    public function updatePackages()
    {
        $this->packages = array();
        $this->scanPackages('src');
    }

    public function getPackages()
    {
        return $this->packages;
    }
}
