#!/bin/bash
ls
# Specify the directory you want to open



# Start code-server and open the specified directory
code-server --auth none --bind-addr 0.0.0.0:$PORT /app