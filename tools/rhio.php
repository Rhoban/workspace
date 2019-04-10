<?php

class RhIO
{
    protected $directory;

    public function __construct($directory)
    {
        $this->directory = $directory;
    }

    public function readValue($node)
    {
        $file = $this->directory.'/'.dirname($node).'/values.conf';
        $param = basename($node);

        if (file_exists($file) && $data = file_get_contents($file)) {
            if (preg_match_all('# '.$param.'\.value = (.+)\n#mUsi', $data, $matches)) {
                return $matches[1][0];
            }
        }

        return null;
    }

    public function setValue($node, $value)
    {

        $file = $this->directory.'/'.dirname($node).'/values.conf';
        $param = basename($node);
        if ($data = file_get_contents($file)) {
            $data = preg_replace_callback('# '.$param.'\.value = (.+)\n#mUsi',
                function($match) use ($param, $value) {
                return ' '.$param.'.value = '.$value."\n";
            }, $data);

            file_put_contents($file, $data);
        }
    }
}
