#!/usr/bin/env bash
# Script to watch for changes in the source code and run the tests

proj_dir=~/Projects/aws-explorer
watch_1="$proj_dir/aws_explorer"
watch_2="$proj_dir/tests"

echo -e "Watching for changes in $WATCH_PATH"

while inotifywait --event close_write $watch_1 $watch_2; do
    echo -e "Change detected, running tests \n\n\n"

    pytest --verbosity 20 $proj_dir/tests --showlocals

done
