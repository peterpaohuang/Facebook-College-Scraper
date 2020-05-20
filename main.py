from scraper import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-e", "--email", help="Email", required=True)
parser.add_argument("-p", "--password", help="Password", required=True)
parser.add_argument("-group_id", "--group_id", help="Facbook group ID", required=True)
parser.add_argument("-m", "--major_key_word", help="Key word for major", nargs="*", required=True)
parser.add_argument("-o", "--outpath", help="Outpath for data", required=True)

args = parser.parse_args()

email = args.email
password = args.password
fb_group_id = args.group_id
major_key_word = args.major_key_word
outpath = args.outpath



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

	for i, url in enumerate(all_posts_index):
		successful = False
		unsuccessful_count = 0
		while not successful:
			try:
				username, locations = fb_scraper.click_extract_post(url, ent_info)

				successful = True

				df.append({"name": username, "where": locations}, ignore_index=True)
			except:
				unsuccessful_count+=1
				if unsuccessful_count > 3:
					continue
				else:
					pass
			finally:
				fb_scraper.go_back()

# # remove repeat usernames
df = df.drop_duplicates(subset='name', keep="first")
df.to_csv(outpath)
