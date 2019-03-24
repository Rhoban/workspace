#!/bin/sh

files=$( find src/rhoban -name "*.cpp" -or -name "*.h" -or -name "*.hpp" -or -name "*.cc" -or -name "*.hh" )

clang-format -i -style=file --verbose ${files}
