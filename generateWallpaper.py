from selenium import webdriver
from pyvirtualdisplay import Display
from PIL import Image
from wordcloud import WordCloud
import json
import os
import sys

display = Display(visible=0, size=(1400, 1000))
display.start()

try:
    browser = webdriver.Firefox()
except:
    print("ERROR: Install geckodriver, and make sure it's in your PATH. Install the latest version of firefox web browser.")
    sys.exit(-1)

country_codes = {'Argentina': 'AR', 'Australia': 'AU', 'Austria': 'AT', 'Belgium': 'BE', 
                 'Brazil': 'BR', 'Canada': 'CA', 'Chile': 'CL', 'Colombia': 'CO', 'Czechia': 'CZ', 
                 'Denmark': 'DK', 'Egypt': 'EG', 'Finland': 'FI', 'France': 'FR', 'Germany': 'DE', 
                 'Greece': 'GR', 'Hong Kong': 'HK', 'Hungary': 'HU', 'India': 'IN', 'Indonesia': 'ID', 
                 'Ireland': 'IE', 'Israel': 'IL', 'Italy': 'IT', 'Japan': 'JP', 'Kenya': 'KE', 
                 'Malaysia': 'MY', 'Mexico': 'MX', 'Netherlands': 'NL', 'New Zealand': 'NZ', 
                 'Nigeria': 'NG', 'Norway': 'NO', 'Philippines': 'PH', 'Poland': 'PL', 'Portugal': 'PT', 
                 'Romania': 'RO', 'Russia': 'RU', 'Saudi Arabia': 'SA', 'Singapore': 'SG', 
                 'South Africa': 'ZA', 'South Korea': 'KR', 'Sweden': 'SE', 'Switzerland': 'CH', 
                 'Taiwan': 'TW', 'Thailand': 'TH', 'Turkey': 'TR', 'Ukraine': 'UA', 'United Kingdom': 'GB', 
                 'United States': 'US', 'Vietnam': 'VN'}

country = "IN" #Set the country code from the above dictionary
days = 10      #Number of days
browser.get(f'https://trends.google.com/trends/trendingsearches/daily?geo={country}')

browser.implicitly_wait(10)

for i in range(1,days+1):
    if i == 1:
        k = 1
    else:
        k = 2
    try:
        link_div = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div[{}]".format(k))
        link_div.click()
    except:
        print("\nERROR: Please check if the country code entered is correct.\n")
        for country, code in country_codes.items():
            print(country + " : " + code)
        print("NOTE: If you do not see your country in the above list, it means daily search trend data is not available for your country in https://trends.google.com/trends/trendingsearches/daily?geo=AR")
        sys.exit(-1)

trending_list = []
trending_dict = {}

for i in range (1,days+1):
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
