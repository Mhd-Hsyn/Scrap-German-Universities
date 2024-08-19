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



def scrap_uni_data(html):
    all_data = {
        "uni_name": "",
        "uni_link": "",
        "name": "",
        "logo": "",
        "web_url": "",
        "description": "",
        "facts": {},
        "contact_info": {},
        "degree_programs": [],
        "campus_info": [],
        "images": [],
    }
    soup= BeautifulSoup(html, "html.parser")
    
    # For Name
    name_div= soup.find("h1", {"class": "institute-title"})
    if name_div:
        all_data["name"]= name_div.text.strip()
        
    # For Link
    link_div= soup.find("a", {"class": "institute-link"})
    if link_div:
        all_data["web_url"]= link_div["href"]
            
    # For Logo
    logo_div= soup.find("img", {"class": "institute-logo"})
    if logo_div:
        all_data["logo"]= logo_div["src"]

    # For Images
    main_ul = soup.find("ul", {"class" :"js-thumbnails thumbnails nano-content"})
    if main_ul:
        images= []
        # li_tags= main_ul.find_all("li", {"class": "js-thumbnails-item thumbnails-item"})
        li_tags= main_ul.find_all("li")
        for li_tag in li_tags:
            image_div = li_tag.find("a", {"data-lightbox": "institute-gallery-2"})
            if image_div:
                img = "https://www.studycheck.de" + image_div["href"]
                images.append(img)

        all_data["images"]= images
    
    # For Background Images
    divs_with_background = soup.find_all("div", style=re.compile(r'background-image'))

    # List to store all the background image URLs with updated dimensions
    background_urls = []

    # Regular expression to extract URL from the style attribute
    url_pattern = re.compile(r'url\((.*?)\)')

    for div in divs_with_background:
        style = div.get('style')
        url_match = url_pattern.search(style)
        if url_match:
            # Extract the URL and strip any quotes
            background_url = url_match.group(1).strip('"').strip("'")
            
            # Replace the dimensions in the URL with "1000x850"
            updated_url = re.sub(r'\d+x\d+', '1000x850', background_url)
            
            background_urls.append(updated_url)
        
    
    all_data["images"] += background_urls


    # For Description
    main_div=  soup.find("div", {"class": ("tab-institute-description", "institute-description")})
    if main_div:
        description_text= main_div.text.strip()
        if description_text:
            description_translate= translate_german_to_english(description_text)
            all_data["description"]= description_translate

    # For Degree Programs
    body= soup.find("tbody", {"class": "js-list"})
    if body:
        degree_programs= []
        tr_tags= body.find_all("tr")
        for tr_tag in tr_tags:
            course_link_tag = tr_tag.find("a", {"class": "course-title"})
            if course_link_tag and course_link_tag.get("href"):
                course_link = course_link_tag.get("href")
                course_name= course_link_tag.text.strip()
                degree_programs.append((course_name, course_link))

        all_data["degree_programs"]= degree_programs

    # For FACTS 
    dl_facts = soup.find("dl", class_="institute-facts")

    # Extract all dt and dd pairs
    facts = {}
    if dl_facts:
        terms = dl_facts.find_all("dt")
        descriptions = dl_facts.find_all("dd")

        for term, description in zip(terms, descriptions):
            # Extract text and strip any extra whitespace
            key = term.text.strip()
            value = description.text.strip()
            key = re.sub(r'\s+', ' ', key)
            value = re.sub(r'\s+', ' ', value)
            facts[translate_german_to_english(key)] = translate_german_to_english(value)

    all_data["facts"] = facts


    # For Contact Info
    contactbox = soup.find('ul', class_='contactbox')
    # Initialize a dictionary to store the data
    contact_info = {
        "address": "",
        "phone": "",
        "email": ""
    }
    # Extract the content inside each <li> tag
    if contactbox:
        address_div = contactbox.find('div', {'class': "content"})
        if address_div:
            all_address = address_div.find_all('p')
            address =  " ".join(re.sub(r'\s+', ' ', addr.text.strip()) for addr in all_address)
            contact_info['address'] = address

        email_div= contactbox.find_all('div', {'class': "content content-small"})
        if email_div:
            contact = email_div[0].find('p').text.strip() if len(email_div) >= 1 and email_div[0].find('p') else ""
            contact_info['phone'] = contact

            email = email_div[1].find('p').text.strip() if len(email_div) >= 2 and email_div[1].find('p') else ""
            contact_info['email'] = email

    all_data["contact_info"] = contact_info

    # For Campus Info
    contact_data = []
    # Find the list of locations
    locations_ul = soup.find('ul', class_='js-locations-list')
    locations= locations_ul.find_all('li') if locations_ul else []

    for location in locations:
        # Extract the location name
        location_name_span = location.find('span', class_='title')
        location_name= location_name_span.text.strip() if location_name_span else ""
        
        # Extract the Address Information
        address_lines_span = location.find('span', class_='adress')
        address =  address_lines_span.decode_contents().replace('<br/>', '').strip() if address_lines_span else ""
        address = re.sub(r'\s+', ' ', address)
        address = address.replace('\n ', ' ').strip()

        # Extract the Contact Information and email information
        all_divs= location.find_all('div', class_='content')
        if all_divs:
            # Extract the contact information
            contact = all_divs[0].text.strip() if len(all_divs) >= 1 else ""
            # Extract the email information
            email = all_divs[1].text.strip() if len(all_divs) >= 2 else ""

            # Store the extracted information
            contact_data.append({
                'location': location_name,
                'address': address,
                'phone': contact,
                'email': email
            })
        
    all_data["campus_info"] = contact_data

    return all_data












def scrap_uni_page():
    # try:
       
        options = get_chromedrvier_options()
        # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager().install()), options=options)
        driver.maximize_window()
        # driver.get("https://www.studycheck.de/suche")
        # driver.get("https://www.studycheck.de/hochschulen/asc/bewertungen")
        # # driver.get("https://www.studycheck.de/hochschulen/hs-albsig")
        
        # try:
        #     translate_button = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'translate')]//button[contains(text(),'Translate')]"))
        #     )
        #     translate_button.click()
        # except:
        #     print("Translation bar did not appear, proceeding with scraping.")
        
        # driver.refresh()
        # driver.refresh()

        with open("unique_universities.json", "r") as file:
            all_uni_links = json.load(file)
            
        
        

        for index, (name, link) in enumerate(all_uni_links, start=1):
            if index <= 244:
                print(f"Skipping page {index} as it has already been scraped.")
                continue

            print(f"\n\n\n\n *********** Scraping page {index} *************\n\n")
            print(f"Link is _________________ {link}")
            driver.get(link)
            time.sleep(2)  # Waiting for page to load
            driver.refresh()
            time.sleep(2)  # Waiting for page to loadme.s
            
            try:
                translate_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'translate')]//button[contains(text(),'Translate')]"))
                )
                translate_button.click()
            except:
                print("Translation bar did not appear, proceeding with scraping.")
            
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-target=".page-tab-courses"]'))
                )
                button.click()
            except :
                pass

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
            
            time.sleep(2)  # Waiting for page to load


            try:
                with open("all_university_data.json", "r") as file:
                    all_links_data = json.load(file)
            except FileNotFoundError:
                all_links_data = []
            
            print("\n\nAll University Links DATA loaded successfully.")
            print(f"Total universities: {len(all_links_data)}")
            print(f"Type of each field: {type(all_links_data)}")
            print("\n\n")
            
            time.sleep(2)  # Waiting for page to load
            html = driver.page_source
            link_data=  scrap_uni_data(html)
            link_data["uni_name"] = name
            link_data["uni_link"] = link
            
            print(f"\n\nData scraped for {name} successfully.\n\n")
            print(f"\nData is : ___________________ \n{json.dumps(link_data, indent=2)}\n\n")

            all_links_data.append(link_data)
            
            print(f"\n\n\n Total universities after scraping: _________ {len(all_links_data)}")
        
            with open('all_university_data.json', 'w') as outfile:
                json.dump(all_links_data, outfile, indent=4)
                print("\nData saved to all_university_data.json")
                print("Scraping completed.\n\n")
                
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