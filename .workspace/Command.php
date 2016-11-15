<?php

abstract class Command
{
    protected $workspace;
    protected $flags = array();

    public function setWorkspace(Workspace $workspace)
    {
        $this->workspace = $workspace;
    }

    abstract public function getName();
    abstract public function getDescription();
    abstract public function run(array $arguments);
    
    public function getUsage()
    {
        return $this->getName();
    }

    public function setFlags(array $flags)
    {
        $this->flags = $flags;
    }
}
