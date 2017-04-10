#!/bin/bash

if [[ $# -lt 1 ]]
then
    echo "Usage: $0 <cmd>"
    exit 1
fi

folders=$(find . -wholename "*src*.git"  | sed 's|/.git||g')

curr_dir=$(pwd)

for folder in ${folders[@]}
do
    cd ${folder}
    echo "[$folder]: $*"
    $*
    cd ${curr_dir}
done
