TYPE=$1
LEVEL=$2

echo "Setting wallpaper brightness..."

WALLPAPER_PATH="$(pwd)/wallpaper.png"

nice python3 adjustWallpaper.py $TYPE $LEVEL $WALLPAPER_PATH
retVal=$?

if [ $retVal -eq 0 ]; then
  sh setWallpaper.sh
else
  echo "Something went wrong"
  echo "You can raise an issue at https://github.com/shardul08/Google-Trend-Wallpaper/issues"
fi