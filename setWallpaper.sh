#!/bin/bash

echo "Setting wallpaper..."

WALLPAPER_PATH="$(pwd)/wallpaper.png"


if command -v gsettings
then
  gsettings set org.gnome.desktop.background picture-uri "file://$WALLPAPER_PATH"
  echo "Success"
elif command -v feh
then
  feh --bg-fill $WALLPAPER_PATH
  echo "Success"
else
  echo "ERROR: Unable to automatically set wallpaper on your system. Manually set your wallpaper to ${WALLPAPER_PATH}."
fi
echo "If something went wrong, raise an issue at https://github.com/shardul08/Google-Trend-Wallpaper/issues"

