#!/bin/bash

# Clone the Git repository at runtime
git clone $GIT_REPO /app

# Change to the repository directory
cd /app

# Install Python packages (add your package names as needed)

# Specify the directory you want to open
DIR_TO_OPEN="./files/"+$FILE_PATH

# Start code-server and open the specified directory
code-server --auth none --bind-addr 0.0.0.0:$PORT $DIR_TO_OPEN
