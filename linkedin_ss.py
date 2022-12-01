#https://code.visualstudio.com/docs/python/python-tutorial
#https://www.geeksforgeeks.org/scrape-linkedin-using-selenium-and-beautiful-soup-in-python/
#https://medium.com/mlearning-ai/how-to-build-a-web-scraper-for-linkedin-6b49b6b6adfc
#python -m pip install matplotlib

#from selenium import webdriver
#from bs4 import BeautifulSoup
#from urllib.request import urlopen
#import pandas as pd


#url = "http://olympus.realpython.org/profiles/dionysus"
#page = urlopen(url)
#html = page.read().decode("utf-8")
#soup = BeautifulSoup(html, "html.parser")

#print(soup.get_text())

#Nota  : Para iniciar a execução dos scripts foi necessário alterar a executionPolicy
#Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

#%%
###1.Import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

#%%
###2. Creating a webdriver instance
driver = webdriver.Chrome("C:\\Users\\Susana\\AppData\\Local\\Temp\\Temp1_chromedriver_win32.zip\\chromedriver.exe")

#Tenho de fazer o starter do driver sempre ? 
# This instance will be used to log into LinkedIn

#%%
###3. Initializing credentials:
email = "projecto.linkedin@gmail.com"
password = "susanadomtiago@2022"

#%%
###4. Opening linkedIn's login page
driver.get("https://linkedin.com/uas/login")

#%% 
###5. Log in in the initial page
time.sleep(5)

driver.find_element(By.ID, 'username').send_keys(email)
driver.find_element(By.ID, 'password').send_keys(password)
time.sleep(6)
driver.find_element(By.XPATH,"//button[@type='submit']").click()

#Now we are logged into linkeding with our dummy account.

#%%
###6. Enter into the profile page
#profile_url = "https://www.linkedin.com/in/john-snow-7995b2256/"
profile_url = "https://www.linkedin.com/in/susanapsousa/"
#profile_url = "https://www.linkedin.com/in/josesousabi/details/experience/"
#https://www.linkedin.com/in/susanapsousa/details/experience/

#%%
###7. Using the selenium driver to get the information profile.
#Then we will scroll the entire page to make sure we load the entire page.
driver.get(profile_url)
time.sleep(5) 
#Now we will scroll into the button : 
start = time.time()

# will be used in the while loop
initialScroll = 0
finalScroll = 1000

while True:
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	# this command scrolls the window starting from
	# the pixel value stored in the initialScroll
	# variable to the pixel value stored at the
	# finalScroll variable
	initialScroll = finalScroll
	finalScroll += 1000

	# we will stop the script for 3 seconds so that
	# the data can load
	time.sleep(3)
	# You can change it as per your needs and internet speed

	end = time.time()

	# We will scroll for 10 seconds.
	# You can change it as per your needs and internet speed
	if round(end - start) > 10:
		break

src = driver.page_source

#%% 
###8. Now using beautiful soup
soup = BeautifulSoup(src, 'html.parser')

#%% 
####INTRO BOX ####
# Extracting the HTML of the complete introduction box that contains the name, company name, and the location
intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
name = intro.find("h1").get_text().strip() # strip() is used to remove any extra blank spaces
work_description = intro.find("div", {'class': 'text-body-medium'}).get_text().strip()

## Let's retrieve location : 
intro_location  = soup.find('div', {'class': 'pv-text-details__left-panel mt2'})
location = intro_location.find("span", {'class': 'text-body-small'}).get_text().strip()

print("Name -->", name,
      "\nWorks At -->", work_description,
      "\nLocation -->", location)

#%%####Experience BOX####
#profile_url = "https://www.linkedin.com/in/josesousabi/details/experience/"
#experience = soup.find_all('div', {'class': 'pvs-list__outer-container'}).find('ul').find('div').find('a').find('h3')

# %%
experience_section = soup.find_all('div', {'class': 'pvs-list__outer-container'})[3]
#experience_section = soup.find_all('div', {'class': 'scaffold-finite-scroll__content'})[2]

#experience_list = experience_section.find('ul').find_all('li','artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
#experience_list = experience_section.find('ul').find_all('li','pvs-list__paged-list-item')
experience_list = soup.select("#experience ~ .pvs-list__outer-container .artdeco-list__item")
#%%
for i in experience_list:
	#print(i.find_all('span'))
	job_name=i.find_all('span', {'class': 'visually-hidden'})[0].get_text().strip()
	job_company=i.find_all('span', {'class': 'visually-hidden'})[1].get_text().strip()
	job_date=i.find_all('span', {'class': 'visually-hidden'})[2].get_text().strip()
	job_local=i.find_all('span', {'class': 'visually-hidden'})[3].get_text().strip()
	print("job name " + job_name)
	print("job company " + job_company)
	print("job date " + job_date)
	print("job local " + job_local)
	print("--------------------------------------------------------------------------")
	#i.find_all('span')
	#i.find_all('span', {'class': 'visually-hidden'})[0].get_text().strip()
	#experience_section.find_all('span', {'class': 'visually-hidden'})[1].get_text().strip()
	#experience_list.find_all('span', {'class': 'visually-hidden'})[2].get_text().strip()
	#experience_list.find_all('span', {'class': 'visually-hidden'})[3].get_text().strip()


#ajuda do mano 
# len(soup.select("#experience ~ .pvs-list__outer-container .artdeco-list__item"))	
#soup.select("div.pvs-list__outer-container")
#soup.select("div.pvs-list__outer-container:nth-child(3)")
#len(soup.select("#experience ~ .pvs-list__outer-container .artdeco-list__item"))

#exp = driver.find_element(By.ID, 'experience')
#exp.find_element(By.TAG_NAME, 'li')
#li_tags = experience.find('div')


#%%





# %%
