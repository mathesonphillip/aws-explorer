#!/usr/bin/env bash
# Monitor a directory for changes
# Based on filepath run a specifc command

# Uses inotifywait to monitor a directory for changes
# Will execute a command based on conditions defined within the while loop

# Change to the directory of the script where this script is located
# cd "$(dirname "$(readlink -f "$0")")"

# exit when any command fails
# set -e

# Define the project root
WATCH_PATH=/home/phil/Projects/aws-explorer

# Define the flags to pass to inotifywait
WATCH_ARGS=(
    # The events to watch for
    --event close_write
    # Set in monitor mode, so that inotifywait will not exit after the first event
    --monitor
    # Recursively watch the directory
    --recursive
    # Exclude files matching <patten> <patten> <patten>
    --excludei '\.git'
    # The directory to watch, you can add more than one
    $WATCH_PATH
)

echo "WatchPath:  $WATCH_PATH"
echo "WatchFlags: ${WATCH_ARGS[@]}"

# ---------------------------------------------------------------------------- #
#                                  PrintHeader                                 #
# ---------------------------------------------------------------------------- #

print_header() {
    local header_text="$1"
    local line=""

    for i in {1..40}; do
        line="${line}-"
    done

    # Calculate the left and right padding
    local header_length=${#header_text}
    local total_length=42
    local padding=$(((total_length - header_length) / 2))

    # Construct the left and right padding strings
    local left_padding=""
    local right_padding=""
    for i in $(seq 1 $padding); do
        left_padding="${left_padding} "
        right_padding="${right_padding} "
    done

    printf "\n"
    printf "%s\n" "# ${line}#"
    printf "%s\n" "  ${left_padding}${header_text}${right_padding}"
    printf "%s\n" "# ${line}#"
    printf "\n"
}

# ---------------------------------------------------------------------------- #
#                                Event Functions                               #
# ---------------------------------------------------------------------------- #

is_python() {
    # Runs the workflow for python files
    print_header "${FUNCNAME[0]}"

    # Run black on the src directory
    print_header "black"
    python -m black --exclude __pycache__ "$WATCH_PATH/aws_explorer"
    # python -m black --exclude __pycache__ "$WATCH_PATH/tests"

    # Run isort on the src directory
    print_header "isort"
    python -m isort --profile black "$WATCH_PATH/aws_explorer"
    # python -m isort --profile black "$WATCH_PATH/tests"

    # Run flake8 on the src directory
    print_header "flake8"
    python -m flake8 --exit-zero --verbose "$WATCH_PATH/aws_explorer"
    # python -m flake8 --exit-zero --verbose "$WATCH_PATH/tests"

    # Run pylint on the src directory
    print_header "pylint"
    pylint --exit-zero --output-format colorized "$WATCH_PATH/aws_explorer"
    # pylint --exit-zero --output-format colorized "$WATCH_PATH/tests"

    # Run pytest on the src directory
    print_header "pytest"
    pytest --verbose "$WATCH_PATH/tests"
}

git_status() {
    # Outputs the git status
    print_header "git_status()"
    git -C $WATCH_PATH status --short --untracked-files

    print_header "git_diff()"
    git -C $WATCH_PATH diff --stat

}
# ---------------------------------------------------------------------------- #
#                                   GitStatus                                  #
# ---------------------------------------------------------------------------- #

#
catch() {
    printf "%s" "${FUNCNAME[0]}"
    # git status --porcelain
}

# Define the flags to pass to inotifywait
WATCH_ARGS=(
    # The events to watch for
    --event close_write
    # Set in monitor mode, so that inotifywait will not exit after the first event
    --monitor
    # Recursively watch the directory
    # --recursive
    # Exclude files matching <patten> <patten> <patten>
    --exclude '\.(git|pyc\.|pyc$|isorted$)'

    # The directory to watch, you can add more than one
    "$WATCH_PATH/aws_explorer"
    "$WATCH_PATH/scripts"
    "$WATCH_PATH/tests"
)
# ---------------------------------------------------------------------------- #
#                                   Main Loop                                  #
# ---------------------------------------------------------------------------- #
inotifywait "${WATCH_ARGS[@]}" | while read DIRECTORY EVENT FILE; do
    # Checks if the file extension is of a type we want to process
    # print_header "$FILE"

    if [[ $FILE =~ \.py$ ]]; then
        is_python "$FILE"

    elif [[ $FILE =~ \.sh$ ]]; then
        printf "Workflow not yet implemented (%s, %s)\n" "$DIRECTORY" "$FILE"

    elif [[ $FILE =~ \.md$ ]]; then
        printf "Workflow not yet implemented (%s, %s)\n" "$DIRECTORY" "$FILE"

    else
        printf "Workflow not yet implemented (%s, %s)\n" "$DIRECTORY" "$FILE"

    fi

    # After processing the file, print out the git status
    git_status

done
