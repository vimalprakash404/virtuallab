#!/bin/bash

# Clone the Git repository at runtime
git clone $GIT_REPO /app

# Install Python packages (add your package names as needed)


# Start code-server
code-server --auth none --bind-addr 0.0.0.0:$PORT /app
