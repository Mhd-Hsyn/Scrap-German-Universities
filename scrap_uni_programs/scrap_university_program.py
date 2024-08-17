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
from googletrans import Translator


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




def translate_german_to_english(german_text):
    # Initialize the Translator
    translator = Translator()
    # Translate from German to English
    translation = translator.translate(german_text, src='de', dest='en')
    # Output the translated text
    return translation.text



def scrap_uni_program_data(html):
    all_data = {
        "university_name": "",
        "university_link": "",
        "program_name": "",
        "program_link": "",
        "full_name": "",
        "description": "",
        "rating": "",
        "information": {},
    }
    soup= BeautifulSoup(html, "html.parser")

    # For Course Full Name
    heading_tag= soup.find("h1", {"class": "course-title"})
    all_data["full_name"] = heading_tag.text.strip() if heading_tag else ""

    # For Course Description
    desc_tag= soup.find("div", {"class": "courses-details"})
    
    if desc_tag:
        description = desc_tag.text.strip() if desc_tag else ""

        if description:
            try:
                translated_description = translate_german_to_english(description)
                all_data["description"] = translated_description
            
            except Exception as e:
                description = desc_tag.find('p')
                description = description.text.strip()  if description else ""
                try:
                    translated_description = translate_german_to_english(description)
                    all_data["description"] = translated_description
                except:
                    pass

    # MAin Div
    main_div = soup.find("div", {"id": "tab-0"})
    if main_div:
        # For Rating
        rating_div = main_div.find("div", {"class": "rating-value"})
        all_data["rating"] = rating_div.text.strip() if rating_div else ""

        # For Information
        all_info_div = main_div.find_all("div", {"class": "card-row"})
        if all_info_div:
            for info_div in all_info_div:
                key_ele = info_div.find("div", {"class": "card-row-label"})
                key = key_ele.text.strip().replace(" ", "_") if key_ele else ""
                
                value_ele = info_div.find("div", {"class": "card-row-content"})
                value = value_ele.text.strip() if value_ele else ""
                
                all_data["information"][key] = value



    return all_data












def scrap_uni_page():
    # try:
       
        options = get_chromedrvier_options()
        # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager().install()), options=options)
        driver.maximize_window()
        driver.get("https://www.studycheck.de/suche")
        # driver.get("https://www.studycheck.de/hochschulen/asc/bewertungen")
        # # driver.get("https://www.studycheck.de/hochschulen/hs-albsig")
        time.sleep(2)  # Waiting for page to load
        driver.refresh()
        time.sleep(2)  # Waiting for page to load
        
        try:
            translate_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'translate')]//button[contains(text(),'Translate')]"))
            )
            translate_button.click()
        except:
            print("Translation bar did not appear, proceeding with scraping.")
        
        driver.refresh()

        with open("all_university_data.json", "r") as file:
            all_uni_links = json.load(file)
            
        
        

        for index, uni_data in enumerate(all_uni_links, start=1):
            university_name = uni_data.get("uni_name", "")
            university_link = uni_data.get("uni_link", "")
            # university_name = re.sub(r'[^\w\s-]', '', university_name)  # Remove everything except alphanumeric, space, dash
            # university_name = re.sub(r'[\s]+', '_', university_name)  # Replace spaces with underscores
            
            print(f"\n\n\n\n *********** Scraping UNIVERSITY {university_name} *************\n")

            degree_programs = uni_data.get("degree_programs", [])
            for program_name, program_link in degree_programs:
                try:
                    with open(f"all_data/all_uni_program_data.json", "r") as file:
                        all_programs_data = json.load(file)
                        
                except:
                    all_programs_data = []

                print(f"\n Name of program is _________________ {program_name}")
                print(f"Link of program is _________________ {program_link}")

                driver.get(program_link)
                time.sleep(2)  # Waiting for page to load
                driver.refresh()
                
                try:
                    translate_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'translate')]//button[contains(text(),'Translate')]"))
                    )
                    translate_button.click()
                except:
                    print("Translation bar did not appear, proceeding with scraping.")
                
                time.sleep(2)  # Waiting for page to load

                data = scrap_uni_program_data(driver.page_source)
                data["university_name"] = university_name
                data["university_link"] = university_link
                data["program_link"] = program_link
                data['program_name'] = program_name
                all_programs_data.append(data)

                with open(f"all_data/all_uni_program_data.json", "w") as file:
                    json.dump(all_programs_data, file, indent=4)
                    print("Data saved to all_uni_program_data.json")


        if driver:
            driver.quit()

    # except Exception as e:
    #     print("An error occurred./n/n", e)
    # finally:
    #     print("QUIT WEB DRIVER ______________")
    #     if driver:
    #         driver.quit()



def sysInit():
    scrap_uni_page()


sysInit()