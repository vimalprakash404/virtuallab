#!/bin/bash

# Check if the Container ID is provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <CONTAINER_ID>"
    exit 1
fi

# Set the Container ID and Local Destination
CONTAINER_ID=$1
NAME=$2
LOCAL_DESTINATION="./files/$NAME"

# Copy files from the container to the local machine
docker cp $CONTAINER_ID:/app $LOCAL_DESTINATION
