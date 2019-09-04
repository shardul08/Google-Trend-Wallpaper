from selenium import webdriver
from pyvirtualdisplay import Display
from PIL import Image
from wordcloud import WordCloud
import json
import os

display = Display(visible=0, size=(1400, 1000))
display.start()

browser = webdriver.Firefox()
country = "US" #set the country here
browser.get(f'https://trends.google.com/trends/trendingsearches/daily?geo={country}')

browser.implicitly_wait(10)

for i in range(1,15):
    if i == 1:
        k = 1
    else:
        k = 2
    link_div = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div[{}]".format(k))
    link_div.click()

trending_list = []
trending_dict = {}

for i in range (1,15):
    list_div = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div[1]/ng-include/div/div/div/div[{}]".format(i))
    details_divs = list_div.find_elements_by_class_name("details")

    for detail_div in details_divs:
        try:
            title = detail_div.find_element_by_class_name("details-top").find_element_by_xpath("div/span/a").text
            search_count = detail_div.find_element_by_xpath('..').find_element_by_class_name("search-count-title").text
            if 'M' in search_count:
                search_count = int(search_count.split('M')[0]) * 1000
            else:
                search_count = int(search_count.split('K')[0])
            if title.lower() in trending_list:
                for key in trending_dict.keys():
                    if key.lower() == title.lower():
                        trending_dict[key] += search_count
            else:
                trending_list.append(title.lower())
                trending_dict[title] = search_count
        except:
            pass
            
browser.quit()
display.stop()

width, height = None, None
try:
    width,height = ((os.popen("xrandr | grep '*'").read()).split()[0]).split("x")
except:
    pass

configJSON = json.loads(open("config.json", "r").read())

if height and width:
    configJSON["resolution"]["width"] = int(width)
    configJSON["resolution"]["height"] = int(height)
    with open('config.json', 'w') as f:
        json.dump(configJSON, f, indent=4)

wc = WordCloud(
    background_color = configJSON["wordcloud"]["background"],
    width = int(configJSON["resolution"]["width"] - 2 * configJSON["wordcloud"]["margin"]),
    height = int(configJSON["resolution"]["height"] - 2 * configJSON["wordcloud"]["margin"])
).generate_from_frequencies(trending_dict)

wc.to_file('wc.png')

wordcloud = Image.open("wc.png")
wallpaper = Image.new('RGB', (configJSON["resolution"]["width"], configJSON["resolution"]["height"]), configJSON["wordcloud"]["background"])
wallpaper.paste(
    wordcloud, 
    (
        configJSON["wordcloud"]["margin"],
        configJSON["wordcloud"]["margin"]
    )    
)
wallpaper.save("wallpaper.png")
