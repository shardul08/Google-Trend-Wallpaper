import sys
from PIL import Image, ImageEnhance

argumentList = sys.argv

adjust_type = sys.argv[1]
try:
    adjust_level = int(sys.argv[2])
except ValueError:
    sys.exit('Invalid brightness argument. Usage "adjustWallpaper.py dim|brighten XX"\n'
             'Example: "adjustWallpaper.py dim 20" #### This would reduce the image brightness by 20%')
wallpaper_path = sys.argv[3]

brightness_change = 1

if adjust_type.lower() == "dim":
    target_level = 100 - adjust_level
    target_level = target_level / 100
    brightness_change = target_level
elif adjust_type.lower() == "brighten":
    target_level = 100 + adjust_level
    target_level = target_level / 100
    brightness_change = target_level
else:
    sys.exit("Invalid argument use 'dim' or 'brighten' to adjust the wallpaper brightness")

try:
    img = Image.open(wallpaper_path)
    enhancer = ImageEnhance.Brightness(img)
    enhanced_img = enhancer.enhance(brightness_change)
    enhanced_img.save(wallpaper_path)
except FileNotFoundError:
    sys.exit(f'{wallpaper_path} file not found. Please run updateWallpaper.sh first to generate the wallpaper.')
