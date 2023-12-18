#!/bin/bash

# Check if the Container ID and Name are provided as arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <CONTAINER_ID> <FILE_NAME>"
    exit 1
fi

# Set the Container ID and Local Destination
CONTAINER_ID=$1
NAME=$2
LOCAL_DESTINATION="./files/$NAME"

# Check if the file already exists locally and delete it
if [ -e "$LOCAL_DESTINATION" ]; then
    echo "Deleting existing file: $LOCAL_DESTINATION"
    rm -rf "$LOCAL_DESTINATION"
fi

# Copy files from the container to the local machine
docker cp "$CONTAINER_ID:/app" "$LOCAL_DESTINATION"
echo "Files copied from container $CONTAINER_ID to $LOCAL_DESTINATION"
