<?php

class Package
{
    protected $repository;
    protected $directory;
    protected $name;
    protected $description;
    protected $dependencies = array();

    public function __construct($repository, $directory)
    {
        $this->repository = $repository;
        $this->directory = $directory;

        $package = file_get_contents($this->directory . '/package.xml');
        $xml = simplexml_load_string($package);
        if (!$xml) {
            Terminal::error('Malformed XML: '.$this->directory.'/package.xml'."\n");
            die();
        }
        $data = json_decode(json_encode($xml), true);
        $this->name = isset($data['name']) ? $data['name'] : 'Unknown';
        $this->description = isset($data['description']) ? $data['description'] : 'Unknown';

        preg_match_all('/\n(.+)depend([^\n]+)<\!\-\-(.+)\-\->/mUsi', $package, $matches);
        foreach ($matches[3] as $repository) {
            $this->dependencies[] = trim($repository);
        }
    }

    public function getRepository()
    {
        return $this->repository;
    }

    public function getDependencies()
    {
        return $this->dependencies;
    }

    public function getDirectory()
    {
        return $this->directory;
    }

    public function getName()
    {
        return $this->name;
    }

    public function getDescription()
    {
        return $this->description;
    }
}
