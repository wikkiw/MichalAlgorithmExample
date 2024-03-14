#!/bin/bash

# Check for exactly one argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

DIRECTORY=$1

# Change to the specified directory
cd "$DIRECTORY" || { echo "Directory $DIRECTORY not found"; exit 1; }
mkdir Results

directories=()

# Find all Python scripts and organize them with the template contents
find . -maxdepth 1 -name "*.py" -exec bash -c '
for script; do
    dir="${script%.*}"                              # Remove file extension to get dir name
    mkdir "$dir"
    cp -r "./template/." "$dir"              # Copy template contents to new directory
    cp "$script" "$dir/Algorithms/"                 # Copy the script to the Algorithms subdirectory
done
' bash {} +

# Iterate over the directories containing the scripts
find . -maxdepth 1 -type d ! -path . -exec bash -c '
for dir in "$@"; do
    dir_name=$(basename "$dir")
    if [ "$dir_name" = "template" ] || [ "$dir_name" = "Results" ]; then      # Skip the template directory
        continue
    fi
    session_name=$(basename "$dir")                 # Use directory name for the session
    tmux new-session -d -s "$session_name"          # Create a new detached tmux session
    tmux send-keys -t "$session_name" "cd $dir; source ~/.venv/bin/activate; python Run_wrapper.py; cp Results/* ../Results/; touch DONE" C-m
done
' bash {} +

for entry in ./*; do
    if [ -d "$entry" ] && [ "$(basename "$entry")" != "template" ] && [ "$(basename "$entry")" != "Results" ]; then
        # Append the directory name to the array
        directories+=("$entry")
    fi
done

done_files=()
for dir in "${directories[@]}"; do
    done_files+=("$dir/DONE")
done

all_done=0
while [ $all_done -eq 0 ]; do
    all_done=1
    for file in "${done_files[@]}"; do
        if [ ! -f "$file" ]; then
            all_done=0
            break
        fi
    done
    sleep 5 # Check every 5 seconds
done

echo "All tmux sessions have completed their scripts."
echo "Cleaning up"
for dir in "${directories[@]}"; do
    rm -r "$dir"
done

echo "Script processing complete."
