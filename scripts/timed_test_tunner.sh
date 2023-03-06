#!/usr/bin/env bash
# Simple bash script to run the make command every 30 seconds
# I have a makefile that will format, lint, test and type-check the project.

# Define the project root
PROJECT_ROOT=/home/phil/Projects/aws-explorer

cd $PROJECT_ROOT

printf "Running make every 30 seconds....\n"

while true; do
    clear
    make lint
    make typecheck
    make test
    sleep 30
done
