# Google-Trend-Wallpaper
A python and shell script to set the wallpaper to a wordcloud of the most trending google searches. 

This project is inspired from [process-wallpaper](https://github.com/anirudhajith/process-wallpaper). You can check it out for the wordcloud of most resource hungry processes running in your system.

![Screenshot](https://github.com/shardul08/Google-Trend-Wallpaper/blob/master/screenshot.png)  


## Dependencies

* `python3`
* `gsettings` or `feh`  To set the generated wordcloud as the wallpaper
* `xvfb`  To simulate a display and run everything in memory
* `firefox` web browser

### Python dependencies

```bash
pip install -r requirements.txt
```

* `selenium`  To scrape the data from [Google trends](https://trends.google.com/trends/trendingsearches/daily?geo=IN)
* `pyvirtualdisplay` Python wrapper for `xvfb`
* `wordcloud` To generate the wordcloud
* `PIL`  Python imaging library

**NOTE** You will need to download the webdriver for `selenium`. [Geckodriver](https://github.com/mozilla/geckodriver/) (webdriver for firefox) can be downloaded from [here](https://github.com/mozilla/geckodriver/releases). 

## Setup

* Clone this repo

```bash
git clone https://github.com/shardul08/Google-Trend-Wallpaper.git
```

* Change directory to the repo

```bash
cd Google-Trend-Wallpaper
```

* Run `setup.sh` with

```bash
./setup.sh
```

This will install all the required dependencies and set the wallpaper.

## Usage

Run `./updateWallpaper.sh` to update the wallpaper to the wordcloud of the latest trends.

You can set your region/country to get the trending searches in `line #30` of [`generateWallpaper.py`](https://github.com/shardul08/Google-Trend-Wallpaper/blob/master/generateWallpaper.py)

You can set the number of days for which you want the trending searches in `line #31` of [`generateWallpaper.py`](https://github.com/shardul08/Google-Trend-Wallpaper/blob/master/generateWallpaper.py)

**NOTE** If the wallpaper is not set automatically, you can set `wallpaper.png` as the wallpaper manually.

If you want the wallpaper to refresh/update every hour, you can add a cron job to run the script every hour.

To add a cron job, run

```bash
crontab -e
```

append the following

```
0 * * * * cd path/to/script/directory && ./updateWallpaper.sh > /tmp/wallpaper.log > 2>&1
```

This will refresh the wallpaper every hour. You can customize this command to refresh the wallpaper as often you want.

