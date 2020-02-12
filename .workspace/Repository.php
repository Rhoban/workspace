<?php

class Repository
{
    protected $directory;
    protected $name;
    protected $host;

    public function __construct($directory = null)
    {
        $this->directory = $directory;

        if (is_dir($this->directory)) {
            $this->setRemote(`cd $this->directory; git config --get remote.origin.url`);
        }
    }

    public function getDirectory()
    {
        return $this->directory;
    }

    public function setRemote($address)
    {
        // No case
        $address = strtolower($address);
        $default = false;

        // Guessing the repository host and name
        if (preg_match('#^http(s?)://([^/]+)/(.+)$#Usi', $address, $match)) { // https
            $this->host = $match[2];
            $this->name = $match[3];
        } else if (preg_match('#^ssh://([^/]+)/(.+)$#Usi', $address, $match)) { // ssh
            $this->host = $match[1];
            $this->name = $match[2];
        } else if (preg_match('#^([a-z0-9]+)@(.+):(.+)$#Usi', $address, $match)) { // git
            $this->host = $match[2];
            $this->name = $match[3];
        } else { // Default
            $this->host = 'github.com';
            $this->name = $address;
            $default = true;
        }

        // Removing prefix @ in hosts
        $tmp = explode('@', $this->host);
        $this->host = $tmp[count($tmp)-1];

        // Removing traling .git in repository name
        if (substr($this->name, -4) == '.git') {
            $this->name = substr($this->name, 0, -4);
        }

        // Directory
        $this->directory = 'src/'.$this->getTarget();
    }

    public function getTarget()
    {
        return $this->name;
    }

    public function getRemotes()
    {
        $remotes = [];

        // Bitbucket
        if ($this->host == 'bitbucket.org') {
            $remotes['origin'] = 'ssh://hg@bitbucket.org/'.$this->name;
        } else {
            $remotes['origin'] = 'git@'.$this->host.':'.$this->name.'.git';
            // $remotes['https'] = 'https://'.$this->host.'/'.$this->name.'.git';
        }

        return $remotes;
    }

    public function getOrigin()
    {
        $remotes = $this->getRemotes();

        return $remotes['origin'];
    }

    public function getName()
    {
        return $this->name;
    }

    public function install($tag = 'master')
    {
        $fast = getenv('GIT_FAST');
        $args = '';
        if ($fast) {
            $args = '--depth=1';
        }
        $command = "cd src/; git clone ".$args." ".$this->getOrigin()." ".$this->getTarget();

        $r = OS::run($command);
        if ($r != 0) {
            Terminal::error('Unable to clone '.$this->getOrigin()."\n");
            die();
        }

        $has_tag = strcmp($tag,'master') != 0;
        if ($has_tag) {
            // Silently using checkout to branch/tag $tag
            $command = "cd src/".$this->getTarget()." && git checkout -q ".$tag;
            $r = OS::run($command);
            if ($r != 0) {
                Terminal::error("Unable to checkout tag/branch: '".$tag."'");
            }
        }

        if (!$fast) {
            OS::run("cd $this->directory; git remote set-branches origin '*'");
            OS::run("cd $this->directory; git fetch");
            $this->updateRemotes();
            if (!$has_tag) {
                $this->setUpstream('origin');
            }
        }
    }

    public function updateRemotes()
    {
        foreach ($this->getRemotes() as $name => $remote) {
            OS::run("cd $this->directory; git remote rm $name");
            OS::run("cd $this->directory; git remote add $name $remote");
        }
    }

    public function getBranch()
    {
        return trim(`cd $this->directory; git rev-parse --abbrev-ref HEAD`);
    }

    public function setUpstream($name)
    {
        $branch = $this->getBranch();
        OS::run("cd $this->directory; git fetch $name");
        OS::run("cd $this->directory; git branch -u $name/$branch");
    }

    public function unshallow()
    {
        OS::run("cd $this->directory; git fetch --unshallow");
    }
}
