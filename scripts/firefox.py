# import csv, os, re, shutil, time, json
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service
# from fake_useragent import UserAgent
# from webdriver_manager.firefox import GeckoDriverManager


# def get_random_headers():
#     ua = UserAgent()
#     headers = {
#         "User-Agent": ua.random,
#         "Accept-Language": "en-US,en;q=0.5"
#     }
#     return headers


# def get_firefox_options():
#     headers = get_random_headers()
#     print(headers)

#     options = Options()
#     options.set_preference("intl.accept_languages", "en-US, en")
#     options.set_preference("general.useragent.override", headers["User-Agent"])
    
#     # Preferences to enable translation
#     options.set_preference("browser.translation.detectLanguage", True)
#     options.set_preference("browser.translation.engine", "Google")
#     options.set_preference("browser.translation.neverForLanguages", "")
#     options.set_preference("browser.translation.ui.show", True)
#     options.set_preference("services.sync.prefs.sync.browser.translation.ui.show", True)
    
#     return options


# def scrap_second_page():
#     try:
#         options = get_firefox_options()
        
#         # Create a new Firefox profile
#         profile = webdriver.FirefoxProfile()
        
#         # Pass the profile to the WebDriver
#         driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options, firefox_profile=profile)
#         driver.maximize_window()
#         driver.get("https://www.studycheck.de/suche")

#         # Wait for the translation bar to appear
#         time.sleep(5)  # Wait for the page to load

#         # Check if the translation prompt appears
#         try:
#             translate_button = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'translate')]//button[contains(text(),'Translate')]"))
#             )
#             translate_button.click()
#         except:
#             print("Translation bar did not appear, proceeding with scraping.")

#         # Proceed with your scraping logic here
#         # ...

#     finally:
#         driver.quit()


# if __name__ == "__main__":
#     scrap_second_page()








from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))


import time
time.sleep(5)  # Wait for the page to load








##############################################################################################333






# import csv, os, re, shutil, time, json
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service as ChromiumService
# from webdriver_manager.core.os_manager import ChromeType
# from fake_useragent import UserAgent


# def get_random_headers():
#     ua = UserAgent()
#     headers = {
#         "User-Agent": ua.random,
#         "Accept-Language": "en-US,en;q=0.5"
#     }
#     return headers


# def get_chromedrvier_options():
#     headers = get_random_headers()
#     print(headers)
#     # Set Chrome options
#     options = Options()
#     # options.headless = True
#     options.add_argument("--enable-logging")
#     options.add_argument("--log-level=0")
#     # options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
#     options.add_argument(f'user-agent={headers["User-Agent"]}')
#     options.add_argument("--no-sandbox")
#     prefs = {
#         "translate_whitelists": {"de":"en"},  # "de" is for German, "en" is for English
#         "translate":{"enabled":True}
#     }
#     options.add_experimental_option("prefs", prefs)
#     return options


# def scrap_second_page():
#     try:
#         parent_table = None
#         retry = True
#         while retry:
#             try:
#                 options = get_chromedrvier_options()
#                 driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#                 driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager().install()), options=options)
#                 driver.maximize_window()
#                 driver.get("https://www.studycheck.de/suche")
#                 driver.get("https://www.studycheck.de/suche")
#                 driver.get("https://www.studycheck.de/suche")
                
#                 try:
#                     translate_button = WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'translate')]//button[contains(text(),'Translate')]"))
#                     )
#                     translate_button.click()
#                 except:
#                     print("Translation bar did not appear, proceeding with scraping.")
                
#                 driver.refresh()
#                 driver.refresh()
                
#                 content = driver.page_source
#                 print(content)
#                 time.sleep(20)  # Waiting for page to load
                
#                 retry= False
                
#                 html_content = driver.page_source
#                 if html_content:
#                     soup = BeautifulSoup(html_content, "html.parser")
#                     # Extracting table data
#                     parent_table = soup.find('table', {'width': '100%', 'border': '0', 'bgcolor': 'WHITE'})
#                     if parent_table:
#                         retry = False
#                     else :
#                         print(f"\n\n\n************** RETRY THE ________ ")
#                         retry= True
#                 else:
#                     retry= True
#             except:
#                 retry= True
#             finally:
#                 print("QUIT WEB DRIVER ______________")
#                 if driver:
#                     driver.quit()

#             # if parent_table:
                
#             #     pass
#             # else:
#             #     print("______________________problem ______________________")
#             #     print(f"Skipping  due to failure in fetching HTML")
#     except Exception as e:
#         print(e)



# def sysInit():
#     scrap_second_page()


# sysInit()