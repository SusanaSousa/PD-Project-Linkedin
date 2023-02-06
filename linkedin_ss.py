#Nota  : Para iniciar a execução dos scripts foi necessário alterar a executionPolicy
#Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
#to install new libraries : 
#python -m pip install matplotlib
#pip install matplotlib
#%%
###1.Import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv


#%%
###2. Starting and Log In
email = "projecto.linkedin@gmail.com"
password = "susanadomtiago@2022"
driver = webdriver.Chrome("C:\\Users\\susys\\AppData\\Local\\Temp\\Temp1_chromedriver_win32.zip\\chromedriver.exe")
driver.get("https://linkedin.com/uas/login")
time.sleep(5)
driver.find_element(By.ID, 'username').send_keys(email)
driver.find_element(By.ID, 'password').send_keys(password)
time.sleep(6)
driver.find_element(By.XPATH,"//button[@type='submit']").click()

#Now we are logged into linkeding with our dummy account.

#%%
def ScrollDown():
	time.sleep(5) 
	#Now we will scroll into the button : 
	start = time.time()
	# will be used in the while loop
	initialScroll = 0
	finalScroll = 1000

	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		# this command scrolls the window starting from the pixel value stored in the initialScroll
		# variable to the pixel value stored at the finalScroll variable
		initialScroll = finalScroll
		finalScroll += 1000
		# we will stop the script for 3 seconds so that the data can load
		time.sleep(2)
		# You can change it as per your needs and internet speed
		end = time.time()
		# We will scroll for 10 seconds.You can change it as per your needs and internet speed
		if round(end - start) > 10:
			break
 
def linkedInLoadPage(url):
	driver.get(url)
	time.sleep(5) 
	#Now we will scroll into the button : 
	start = time.time()
	# will be used in the while loop
	initialScroll = 0
	finalScroll = 1000

	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		# this command scrolls the window starting from the pixel value stored in the initialScroll
		# variable to the pixel value stored at the finalScroll variable
		initialScroll = finalScroll
		finalScroll += 1000
		# we will stop the script for 3 seconds so that the data can load
		time.sleep(2)
		# You can change it as per your needs and internet speed
		end = time.time()
		# We will scroll for 10 seconds.You can change it as per your needs and internet speed
		if round(end - start) > 10:
			break

	src = driver.page_source
	soup = BeautifulSoup(src, 'html.parser')
	return soup

 
def linkedinIntro(soup):
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


def linkedinExperience(soup, user, experience_df):
	#print(user)
	#print(experience_df)
	#experience_section = soup.find_all('div', {'class': 'pvs-list__outer-container'})[3]
	#experience_list = soup.select("#experience ~ .pvs-list__outer-container .artdeco-list__item")
	#experience_dict = dict()
	#experience_df = pd.DataFrame(columns = ['user','job_name','job_company','job_date','job_local'])
	experience_list = soup.select("#experience ~ .pvs-list__outer-container .artdeco-list__item")

	for i in experience_list:
		exp = i.select(".display-flex.flex-row.justify-space-between")

		if len(exp) == 1:
			content_info=i.select(".display-flex.flex-row.justify-space-between .display-flex.flex-column.full-width .visually-hidden")
			try : 
				job_name=content_info[0].get_text().strip()
			except :
				job_name = "NA"
			try : 
				job_company=content_info[1].get_text().strip()
			except :
				job_company = "NA"
			try : 
				job_date=content_info[2].get_text().strip()
			except :
				job_date = "NA"
			try : 
				job_local=content_info[3].get_text().strip()
			except :
				job_local = "NA"

			current_experience_df = pd.DataFrame([{'user' : user ,'job_name': job_name ,'job_company':job_company,'job_date':job_date,'job_local':job_local}])
			experience_df = pd.concat([experience_df,current_experience_df])

		else:
			first = 1
			for j in exp:
				if first == 1:
					job_company=j.find_all('span', {'class': 'visually-hidden'})[0].get_text().strip()
					first = 0
				else :
					content_info = j.select(".display-flex.flex-row.justify-space-between .visually-hidden")
					try:
						job_name = content_info[0].get_text().strip()
					except : 
						job_name="NA"
					try:
						job_date = content_info[1].get_text().strip()
					except : 
						job_date="NA"
					try:
						job_local = content_info[2].get_text().strip()
					except : 
						job_local="NA"
						#job_name=j.find_all('span', {'class': 'visually-hidden'})[0].get_text().strip()
						#job_date=j.find_all('span', {'class': 'visually-hidden'})[1].get_text().strip()
						#job_local=j.find_all('span', {'class': 'visually-hidden'})[2].get_text().strip()
					current_experience_df = pd.DataFrame([{'user' : user ,'job_name': job_name ,'job_company':job_company,'job_date':job_date,'job_local':job_local}])
					experience_df = pd.concat([experience_df,current_experience_df])

	return experience_df

# %% MAIN ##################################################################
# %%
#########_________Get users list from natixis page
#users_url ="https://www.linkedin.com/company/natixis-in-portugal/people/"
#users_page = linkedInLoadPage(users_url)

#people_list = users_page.select(".scaffold-finite-scroll__content .app-aware-link.link-without-visited-state")
#usernames_list = []
#init = "/in/"
#end = "?mini"
#for user in people_list:
#	try:
#		user_link = user.get("href")
#		username = user_link[user_link.index(init)-1 + len(init) + 1: user_link.index(end)]
#		usernames_list.append(username)
#	except:
#		print("Something failed")

#%%
#########_________Go inside a profile page
#user = "susanapsousa"
#profile_url = "https://www.linkedin.com/in/"+user+"/"
#experience_df = pd.DataFrame(columns = ['user','job_name','job_company','job_date','job_local'])
#usernames_list_short = usernames_list[-10:]

#for i in usernames_list_short:
#	profile_url = "https://www.linkedin.com/in/"+i+"/"
#	profile_page = linkedInLoadPage(profile_url)
#	experience_df = linkedinExperience(profile_page,i,experience_df)
#	time.sleep(5)

#experience_df.to_csv('data.csv', index=False)



# %% More tests to get a list from the search

def getPeopleBySearch(search_words):
	#Search the desired words in the People category
	search = driver.find_element(By.CLASS_NAME, 'search-global-typeahead__input')
	search.click()
	search.send_keys(search_words)
	search.send_keys(Keys.ENTER)
	time.sleep(5)
	people_bt = driver.find_element(By.XPATH, '//button[text()="People"]')
	people_bt.click()

	#Loop into the list of people to get the username of the profile.
	#The username will be saved and then used to extract the info in a second step
	i=0
	loop_limit = 20 #it will be multiplied by 10 as it is the max number of people presented by page
	usernames_list = []
	while i < loop_limit :
		time.sleep(10)
		people_soup = BeautifulSoup(driver.page_source, 'html.parser')	
		people_list = people_soup.select(".reusable-search__result-container .app-aware-link.scale-down ")
		
		init = "/in/"
		end = "?mini"
		for user in people_list:
			try:
				user_link = user.get("href")
				username = user_link[user_link.index(init)-1 + len(init) + 1: user_link.index(end)]
				usernames_list.append(username)
			except:
				print("Something failed")
				return usernames_list
		#print(usernames_list)
		ScrollDown()

		next_bt = driver.find_element(By.XPATH,("//button[@aria-label='Next']"))
		next_bt.click()
		i=i+1
	return usernames_list


# %%  MAIN 
search_words = "Natixis in Portugal"
usernames_list = getPeopleBySearch(search_words)
usernames_list_short = usernames_list[-10:]


users_df = pd.DataFrame(data={"user": usernames_list})
users_df.to_csv('users.csv', index=False)

# %%
#Reading the users from the previous created list
users = pd.read_csv('users.csv')
usernames_list = users['user']
#%%
experience_df = pd.DataFrame(columns = ['user','job_name','job_company','job_date','job_local'])

for i in usernames_list:
	try:
		print(i)
		profile_url = "https://www.linkedin.com/in/"+i+"/"
		profile_page = linkedInLoadPage(profile_url)
		experience_df = linkedinExperience(profile_page,i,experience_df)
		time.sleep(5)
	except:
		experience_df.to_csv('data.csv', index=False)

experience_df.to_csv('data.csv', index=False)
# %%
