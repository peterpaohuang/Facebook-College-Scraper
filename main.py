from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from utils import *
from scraper import Scraper

email = ""
password = ""
fb_group_id = "297925267524391"
major_key_word = ["computer science", "cs", "comp sci"]

driver =  webdriver.Chrome('./chromedriver')
driver.get("https://mobile.facebook.com/")

# initialize nlp and capitalization engines 
print("Initializing...")
ent_info = initializers()

print("Initialized. Navigating to posts...")
fb_scraper = Scraper(driver, email, password, fb_group_id)
fb_scraper.login()
fb_scraper.bypass_popup()
fb_scraper.goto_search()

print("Extracting Data...")
df = pd.DataFrame(columns=["name", "where"])

# search group for major key word
for key_word in major_key_word:

	fb_scraper.search(key_word)
	fb_scraper.scroll_bottom()
	all_posts_index = fb_scraper.get_all_posts()
	
	print("Number of posts: {}".format(len(all_posts_index)))

	for i, url in enumerate(all_posts_index):
		successful = False
		while not successful:
			try:
				username, locations = fb_scraper.click_extract_post(url, ent_info)

				successful = True

				print("{} is from {}: ***{}***".format(username,locations,i))
				df.append({"name": username, "where": locations}, ignore_index=True)

				fb_scraper.go_back()
			except:
				fb_scraper.scroll_bottom()

# # remove repeat usernames
df = df.drop_duplicates(subset='name', keep="first")

df.to_csv("major_data.csv")
