<?php

class SetupCommand extends Command
{
    public function getName()
    {
        return 'setup';
    }

    public function getDescription()
    {
        return array('Setup the catkin workspace');
    }

    public function run(array $arguments)
    {
        Terminal::info("* Runing setup of the workspace\n");
        if (!is_dir('src')) {
            mkdir('src');
        }
        if (!is_dir('src/catkin')) {
            Terminal::info("* Cloning catkin\n");
            OS::run('cd src; git clone --depth=1 https://github.com/ros/catkin.git');
        }
        Terminal::info("* Runnin catkin init\n");
        OS::run('catkin init --workspace .');
        Terminal::info("* Setup of profile debug and release");
        OS::run('catkin config --profile debug -x _debug --cmake-args -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="-msse2"');
        OS::run('catkin config --profile release -x _release --cmake-args -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="-msse2"');
        OS::run('catkin config --profile release_linter -x _release_linter --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="-msse2"');
        OS::run('catkin config --profile novision -x _nv_release --cmake-args -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="-msse2" -DBUILD_KID_SIZE_VISION=OFF');
        OS::run('catkin config --profile novision_debug -x _nv_debug --cmake-args -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="-msse2" -DBUILD_KID_SIZE_VISION=OFF');
    }
}
