<?php

class StatusCommand extends Command
{
    public function getName()
    {
        return 'status';
    }

    public function getDescription()
    {
        return array('Getting the status of each package');
    }

    public function gitBranch(string $dir)
    {
      return trim(`cd $dir; git rev-parse --abbrev-ref HEAD`);
    }

    public function gitStatus(string $name, string $dir)
    {
      $result = `cd $dir; LANG=en_US git status`;
      $errors = array();
      $warnings = array();
      $messages = array();
      if (strstr($result, 'Changes not staged for commit:') !== false) {
          $errors[] = 'Unstaged changes';
      }
      if (strstr($result, 'Changes to be committed:') !== false) {
          $errors[] = 'Changes to commit';
      }
      if (strstr($result, 'Your branch is ahead of') !== false) {
          $errors[] = 'Not pushed changes';
      }
      if (strstr($result, 'Your branch is behind') !== false) {
          $warnings[] = 'Branch is behind origin';
      }
      if (strstr($result, 'Untracked files:') !== false) {
          $warnings[] = 'Untracked files';
      }
      $messages = implode(', ', array_merge($errors, $warnings, $messages));
      if ($messages) $messages = '('.$messages.')';
      $branch = $this->gitBranch($dir);
      if (count($errors)) {
          Terminal::error("* [$branch] $name: ERROR $messages\n");
      } else if (count($warnings)) {
          Terminal::warning("* [$branch] $name: WARNING $messages\n");
      } else {
          Terminal::success("* [$branch] $name: OK $messages\n");
      }
    }

    public function printStatus(Repository $repository)
    {
        $dir = $repository->getDirectory();
        $name = $repository->getName();

        $this->gitStatus($name, $dir);
    }

    public function run(array $arguments)
    {
        Terminal::info("Repositories:\n");
        $this->gitStatus('workspace', '.');
        foreach ($this->workspace->getRepositories() as $repository) {
            $this->printStatus($repository);
        }
    }
}
