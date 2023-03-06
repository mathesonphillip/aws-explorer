#!/usr/bin/env bash
# Simple bash script to run the make command every 30 seconds
# I have a makefile that will format, lint, test and type-check the project.

# Define the project root
PROJECT_ROOT=/home/phil/Projects/aws-explorer
cd $PROJECT_ROOT

VENV_PATH=/home/phil/Projects/aws-explorer/env/bin/activate

while true; do

    # Wait for a save event on the run.py file
    inotifywait --quiet --event close_write ./aws_explorer

    clear
    # Run the application
    source $VENV_PATH && pytest

    sleep 10

done
