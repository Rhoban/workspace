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
        system('which dot > /dev/null', $ret);
        if ($ret != 0) {
            Terminal::error("Can't find dot, try: apt-get install graphviz\n");
            die();
        }

        $count = 0;
        $graph = "digraph {\n";
        $graph .= "graph [bgcolor=transparent]\n";
        foreach ($this->workspace->getPackages() as $package) {
            $name = basename($package->getName());
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
            $name = basename($package->getName());
            foreach ($package->getBuildDependencies() as $dep) {
                $graph .= "\"$name\" -> \"".$dep."\"\n";
            }
        }
        $graph .= "}\n";
        file_put_contents('/tmp/out.dot', $graph);
        `dot -Tpdf /tmp/out.dot > /tmp/out.pdf`;
        `evince /tmp/out.pdf`;
    }
}
