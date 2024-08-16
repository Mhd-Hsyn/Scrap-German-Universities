

import csv, os, re, shutil, time, json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromiumService
from fake_useragent import UserAgent


def get_random_headers():
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "en-US,en;q=0.5"
    }
    return headers


def get_chromedrvier_options():
    headers = get_random_headers()
    print(headers)
    # Set Chrome options
    options = Options()
    # options.headless = True
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    # options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
    options.add_argument(f'user-agent={headers["User-Agent"]}')
    options.add_argument("--no-sandbox")
    prefs = {
        "translate_whitelists": {"de":"en"},  # "de" is for German, "en" is for English
        "translate":{"enabled":True}
    }
    options.add_experimental_option("prefs", prefs)
    return options



def scrap_all_uni_links(html):
    
    all_data= []
    soup= BeautifulSoup(html, "html.parser")
    all_divs= soup.find_all("div", {"class": "rfv1-media-layout__row rfv1-media-layout__row--relative rfv1-display--flex"})
    # print(f"Found {len(all_divs)} divs")
    if all_divs:
        for div in all_divs:
            a_tag= div.find("a", href=True)
            name_main_div= div.find("div", {"class": "rfv1-font-size--h3 rfv1-font-color--primary rfv1-mb--0"})
            name_a_tag= name_main_div.find("a", {"class": "rfv1-font-style--none"})
            name=name_a_tag.text.strip()
            # if a_tag:
            # print(f"\n\nFound name: {name}")
            # print(f"Found link: {a_tag['href']}\n\n")
            data= (name, a_tag["href"])
            print(type(data), data)
            all_data.append(data)

    return all_data



def scrap_second_page():
    try:
       
        options = get_chromedrvier_options()
        # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager().install()), options=options)
        driver.maximize_window()
        driver.get("https://www.studycheck.de/suche")
        driver.get("https://www.studycheck.de/suche")
        driver.get("https://www.studycheck.de/suche")
        
        try:
            translate_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'translate')]//button[contains(text(),'Translate')]"))
            )
            translate_button.click()
        except:
            print("Translation bar did not appear, proceeding with scraping.")
        
        driver.refresh()
        driver.refresh()
        
        html = driver.page_source
        time.sleep(2)  # Waiting for page to load

        all_links_data = []

        for i in range(1, 60):  # Fetching 1 to 59 pages
            print(f"\n\n\n\nPage {i}:\n")
            link = f"https://www.studycheck.de/suche?page={i}"
            driver.get(link)

            try:
                translate_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'translate')]//button[contains(text(),'Translate')]"))
                )
                translate_button.click()
            except:
                print("Translation bar did not appear, proceeding with scraping.")
            time.sleep(2)

            time.sleep(2)  # Waiting for page to load
            html = driver.page_source
            all_links_data += scrap_all_uni_links(html)
            print(f"Found {len(all_links_data)} universities")
            time.sleep(2)  # Waiting for page to load
        
        with open('uniersities.json', 'w') as outfile:
            json.dump(all_links_data, outfile, indent=4)
            print("Data saved to universities.json")
            print("Scraping completed.")

    except Exception as e:
        print("An error occurred./n/n", e)
    finally:
        print("QUIT WEB DRIVER ______________")
        if driver:
            driver.quit()



def sysInit():
    scrap_second_page()


sysInit()