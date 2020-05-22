# Facebook College Scraper
## Python scraper for your __college/university's Facebook group__ to find and understand the __demographic__ of people in your major

### Current data scraper can extract based on major keywords (e.g. comp sci, cs, computer science):
1. Username
2. Location
3. More coming soon...

## Installation
Download project using pip
```
pip install git+https://github.com/peterpaohuang/Facebook-College-Scraper.git
```
If using macOS:
```python
python setup.py
```
For other operating systems, please complete the following instructions:
1. Install required packages `pip install -r requirements.txt`
2. Download [Chrome Driver](https://chromedriver.storage.googleapis.com/81.0.4044.138/).
	Once downloaded, unzip the file and move the resulting chromedriver.exe into facebook_scraper
3. Download [language model](https://github.com/nreimers/truecaser/releases/download/v1.0/english_distributions.obj.zip).
	Once downloaded, unzip the file and move the resulting distributions.obj into facebook_scraper

## Command Usage

```
Usage:
python main.py -e [username] -p [password] -group_id [facebook group ID] -m "[key words 1]" "[key words 2]" "key words 3" -o [outpath]

Example:
python main.py -e example_email@gmail.com -p password123 -group_id 297925267524391 -m "comp sci" "cs" "computer science" -o extracted_data.csv

Flags:
	--email, -e 					string				email to login to your Facebook account
	--password, -p 					string				password to login to your Facebook account
	--group_id 					int 				Facebook group ID script will scrape
	--major_key_word, -m 				string 				key words for your major to search for
	--outpath, -o   				string				outpath for CSV file storing the extracted data
```

## Built With
* [Truecaser](https://github.com/nreimers/truecaser) - Capitalize geography
* [Geograpy3](https://github.com/jmbielec/geograpy3) - Detect location from text

## License
This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgements
* University of Illinois at Urbana Champaign Class of 2020 Facebook Groupchat for motivation behind this project
