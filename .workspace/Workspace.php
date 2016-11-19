<?php

class Workspace
{
    protected $directory;
    protected $commands = array();
    protected $packages = array();
    protected $repositories = array();

    public function __construct($directory)
    {
        if (!is_dir('src')) {
            mkdir('src');
        }

        $this->directory = $directory;

        $this->addCommand(new SetupCommand);
        $this->addCommand(new InstallCommand);
        $this->addCommand(new BuildCommand);
        $this->addCommand(new PackagesCommand);
        $this->addCommand(new StatusCommand);
        $this->addCommand(new PullCommand);
        $this->addCommand(new UpdateRemotesCommand);
        $this->addCommand(new UpstreamCommand);
        $this->addCommand(new CleanCommand);
        $this->addCommand(new UnshallowCommand);

        $this->updatePackages();
        $this->repositories = array();
        $this->updateRepositories();
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

    public function install($address)
    {
        $parts = explode(' ', $address);
        $prefix = null;
        if (count($parts) > 1) {
            $address = $parts[count($parts)-1];
            $prefix = $parts[0];
        }

        // Getting repository data
        $repository = new Repository();
        $repository->setRemote($address);
        $name = $repository->getName();
        $directory = $repository->getDirectory();

        if (isset($this->installed[$name])) {
            return;
        }
        $this->installed[$name] = false;

        // Asking for install
        $install = true;
        $ask = "Do you want to install the optional $name package ?";
        if ($prefix == 'optional') {
            $install = Prompt::ask($ask, false);
        }
        if ($prefix == 'recommend') {
            $install = Prompt::ask($ask, true);
        }

        if (!$install) {
            Terminal::error("* Not installing $name\n");
            return;
        }

        if (!is_dir($repository->getDirectory())) {
            Terminal::success("* Installing $name in $directory\n");
            $repository->install();
            $this->updatePackages();
        } else {
            Terminal::info("* Repository $name already installed\n");
        }

        Terminal::info("* Scanning dependencies for $name...\n");
        $toInstall = array();
        foreach ($this->packages as $package) {
            if ($package->getRepository() == substr($directory, 4)) {
                foreach ($package->getDependencies() as $dependency) {
                    $toInstall[] = $dependency;
                }
            }
        }
        foreach ($toInstall as $install) {
            $this->install($install);
        }
    }

    protected function scanPackages($dir, $repository = null, $over = false)
    {
        if (file_exists($dir . '/package.xml')) {
            $this->packages[] = new Package($repository, $dir);
        } else {
            if (is_dir("$dir/.git")) {
                $over = true;
            }
            foreach (scandir($dir) as $subdir) {
                if ($subdir != '.' && $subdir != '..' && $subdir != 'catkin') {
                    $rep = $subdir;
                    $subdir = $dir . '/' . $subdir;
                    if (is_dir($subdir)) {
                        $tmp = $repository;
                        if (!$over) {
                            if (!$tmp) $tmp = $rep;
                            else $tmp .= "/$rep";
                        }
                        $this->scanPackages($subdir, $tmp, $over);
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

    public function updateRepositories($sdir = 'src')
    {
        foreach (scandir($sdir) as $dir) {
            if ($dir != '.' && $dir != '..' && $dir != 'catkin') {
                $tmp = "$sdir/$dir";
                if (is_dir("$tmp")) {
                    if (is_dir("$tmp/.git")) {
                        $this->repositories[] = new Repository($tmp);
                    } else {
                        $this->updateRepositories("$tmp");
                    }
                }
            }
        }
    }

    public function getRepositories()
    {
        return $this->repositories;
    }
}
