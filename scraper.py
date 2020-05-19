from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from utils import *


class Scraper:
	def __init__(self, driver, email, password, fb_group_id):
		self.driver = driver
		self.email = email
		self.password = password
		self.fb_group_id = fb_group_id
		self.post_list_url = ""

	def login(self):
		# login 
		email_text_field = self.driver.find_element_by_id("m_login_email")
		email_text_field.clear()
		email_text_field.send_keys(self.email)

		password_text_field = self.driver.find_element_by_id("m_login_password")
		password_text_field.clear()
		password_text_field.send_keys(self.password)

		log_in_button = self.driver.find_element_by_name("login")
		log_in_button.click()

	def bypass_popup(self):
		# bypass post login intermediate screen

		not_now_button = WebDriverWait(self.driver, 10).until(
			lambda x: x.find_element_by_xpath("//a[starts-with(@href, '/login/save')]"))
		not_now_button.click()

	def goto_search(self):
		# home screen 
		right_accordion_button = WebDriverWait(self.driver, 10).until(
			lambda x: x.find_element_by_name("More"))
		right_accordion_button.click()


		# click groups
		groups_link = WebDriverWait(self.driver, 10).until(
			lambda x: x.find_element_by_xpath("//a[contains(@href, '/groups/?')]"))
		groups_link.click()

		# select your_group button on top
		your_group_link = WebDriverWait(self.driver, 10).until(
			lambda x: x.find_element_by_xpath("//a[contains(@href, 'your_groups')]"))
		your_group_link.click()

		# select specified group 
		specified_group_link = WebDriverWait(self.driver, 10).until(
			lambda x: x.find_element_by_xpath("//a[contains(@href, '/groups/{}/?')]".format(self.fb_group_id)))
		specified_group_link.click()

		# click search button 
		search_button = WebDriverWait(self.driver, 10).until(
			lambda x: x.find_element_by_xpath("//a[@aria-label='Search']"))
		search_button.click()

	def search(self, key_word):
		search_input = WebDriverWait(self.driver, 10).until(
		lambda x: x.find_element_by_id("main-search-input"))
		search_input.click()
		search_input.clear()
		search_input.send_keys(key_word, Keys.ENTER)

		self.post_list_url = self.driver.current_url

	def scroll_bottom(self):
		# Scroll all the way down to return all results

		SCROLL_PAUSE_TIME = 1.5
		last_height = self.driver.execute_script("return document.body.scrollHeight")

		while True:
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(SCROLL_PAUSE_TIME)

			new_height = self.driver.execute_script("return document.body.scrollHeight")
			if new_height == last_height:
				break
			last_height = new_height

	def get_all_posts(self):
		all_posts_index = []
		# retrieve all unique image post url
		num_sections = len(WebDriverWait(self.driver, 10).until(
				lambda x: x.find_elements_by_xpath("//div[contains(@data-module-result-type, 'story')]")))

		for i in range(num_sections):
			section = WebDriverWait(self.driver, 10).until(
				lambda x: x.find_elements_by_xpath("//div[contains(@data-module-result-type, 'story')]"))[i]

			num_posts = len(section.find_elements_by_xpath("./div"))
			for k in range(num_posts):
				post = section.find_elements_by_xpath("./div")[k]
				all_posts_index.append(post.find_element_by_tag_name("img").get_attribute("src"))
		all_posts_index = list(dict.fromkeys(all_posts_index)) # remove duplicate posts/another posts

		return all_posts_index
	def click_extract_post(self, url, ent_info):
		post = WebDriverWait(self.driver, 10).until(
			lambda x: x.find_element_by_xpath("//img[@src='{}']".format(url)))
		self.driver.execute_script("arguments[0].click();", post)

		username = WebDriverWait(self.driver, 10).until(
			lambda x: x.find_element_by_xpath("//a[contains(@href, 'groupid=')]")).get_attribute("href")

		# get where poster is from
		text_div = self.driver.find_element_by_class_name("_5rgt")
		text = text_div.text
		
		capitalized_text = capitalize_ents(text, ent_info)
		locations = extract_location(capitalized_text, username)

		return username, locations

	def go_back(self):
		self.driver.get(self.post_list_url)
		self.scroll_bottom()

