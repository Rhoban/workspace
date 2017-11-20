<?php

class GraphCommand extends Command
{
    public function getName()
    {
        return 'graph';
    }

    public function getDescription()
    {
        return array('Graph of packages');
    }

    public function run(array $arguments)
    {
        $count = 0;
        $graph = "digraph {\n";
        foreach ($this->workspace->getPackages() as $package) {
            $name = strtolower(basename($package->getName()));
            $graph .= "\"$name\"";
            if (strstr(strtolower($package->getRepository()), 'rhoban') !== false
            && strstr(strtolower($package->getRepository()), 'deps') === false) {
                $graph .= " [color=deepskyblue4,fontcolor=white,fillcolor=deepskyblue4,style=filled,fontsize=30]";
            } else {
                $graph .= " [color=black,fontcolor=white,fillcolor=black,style=filled,fontsize=30]";
            }
            $graph .="\n";
        }
        foreach ($this->workspace->getPackages() as $package) {
            $count++;
            $name = strtolower(basename($package->getName()));
            foreach ($package->getDependencies() as $k => $dep) {
                $rep = new Repository;
                $rep->setRemote($dep);
                foreach ($this->workspace->getPackages() as $otherPackage) {
                    if ($otherPackage->getRepository() == $rep->getName()) {
                        $graph .= "\"$name\" -> \"".strtolower(basename($otherPackage->getName()))."\"\n";
                    }
                }
            }
        }
        $graph .= "}\n";
        file_put_contents('/tmp/out.dot', $graph);
        `dot -Tpng /tmp/out.dot > /tmp/out.png`;
        `eog /tmp/out.png`;
    }
}
