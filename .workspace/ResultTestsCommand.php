<?php

class ResultTestsCommand extends Command
{
    public function getName()
    {
        return 'result_tests';
    }

    public function getDescription()
    {
        return array('Get tests result(s)');
    }

    public function run(array $arguments)
    {
        if (!is_executable('src/catkin/bin/catkin_test_results')) {
            Terminal::error("`src/catkin/bin/catkin_test_results` does not exist or is not executable. Did you run `workspace setup` ?");
            return;
        }

        $args = implode(' ', $arguments);
        return OS::run('./src/catkin/bin/catkin_test_results ' . $args);
    }
}