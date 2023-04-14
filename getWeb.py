# get text, emojis and images/videos from the latest browsing
# test: get from history
# not working yet!!!

import browserhistory as bh
from bs4 import BeautifulSoup
import requests


# get the latest url and take it as current
dict_obj = bh.get_browserhistory()
current_url=dict_obj['firefox'][0] # to-do: if new url!=old url, update

# scrape and sort
current_url="https://www.tiktok.com/@aa.vision/video/6893835274506292482?q=photography&t=1677849155294" # for test
page = requests.get(current_url)
soup = BeautifulSoup(page.content, 'html.parser')
result=soup.find('div',
                 attrs={'id':'wc-power-page'})

