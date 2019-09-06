#!/bin/bash

echo "Creating wallpaper..."

nice python3 generateWallpaper.py
retVal=$?
if [ $retVal -eq 0 ]; then
    sh setWallpaper.sh
else
    echo "Something went wrong"
fi
