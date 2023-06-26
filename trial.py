import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import os
import requests
import PyPDF2

def download_pdf(url):
    # Instantiating undetected chromedriver for avoiding CloudFlare verification while logging in chatgpt
    chrome_opt = uc.ChromeOptions()
    prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    chrome_opt.add_experimental_option("prefs", prefs)
    driver = uc.Chrome(options=chrome_opt, executable_path=r'C:\path\to\chromedriver.exe')

    # XPaths for href elements
    xpath_list = [
        '//*[@id="bodyMainLayout"]/div[1]/div/div/div[2]/div[2]/table/tbody/tr[1]/td[4]/a',
        '//*[@id="bodyMainLayout"]/div[1]/div/div/div[2]/div[2]/table/tbody/tr[2]/td[4]/a',
        '//*[@id="bodyMainLayout"]/div[1]/div/div/div[2]/div[2]/table/tbody/tr[3]/td[4]/a',
        '//*[@id="bodyMainLayout"]/div[1]/div/div/div[2]/div[2]/table/tbody/tr[4]/td[4]/a',
        '//*[@id="bodyMainLayout"]/div[1]/div/div/div[2]/div[2]/table/tbody/tr[5]/td[4]/a',
        '//*[@id="bodyMainLayout"]/div[1]/div/div/div[2]/div[2]/table/tbody/tr[6]/td[4]/a'
    ]
    language_list = [
        'English',
        'French',
        'Spanish',
        'Arabic',
        'Russian',
        'Chinese',
    ]
    href_list = []  # Initialize the list to store href values
    file_language_list=[] #if href exist in the below code,i would append the language from language_list

    folder_index = 1  # Initialize the folder index
    # website is opened
    driver.get(url)
    time.sleep(5)

    # Create the demo folder if it doesn't exist
    os.makedirs("./demo", exist_ok=True)

    # locating download btns
    for i in range(0, 2):
        # tr_tags = driver.find_elements(By.CSS_SELECTOR, 'tr')
        tr_tags = driver.find_elements(By.CSS_SELECTOR, 'tr')[3:]


        for num, tr_tag in enumerate(tr_tags):
            if num > 0:
                # Open the link in a new tab or window
                actions = webdriver.ActionChains(driver)
                actions.key_down(Keys.CONTROL).click(tr_tag).key_up(Keys.CONTROL).perform()
                time.sleep(2)

                # Switch to the newly opened tab or window
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)

                # Retrieve href values from elements matching the XPaths
                count=0
                for xpath in xpath_list:
                    try:
                        element = driver.find_element(By.XPATH, xpath)
                        href = element.get_attribute("href")
                        href_list.append(href)
                        if(element):
                            file_language_list.append(language_list[count])
                            count=count+1

                    except:
                        count=count+1
                        pass  # Ignore if element not found
                print(file_language_list)
                print()
                if href_list:
                    folder_path = f"./demo/{folder_index}"
                    os.makedirs(folder_path, exist_ok=True)

                    for index, href in enumerate(href_list):
                        response = requests.get(href)
                        file_path = os.path.join(folder_path, f"{file_language_list[index]}.pdf")

                        # Save the PDF locally
                        with open(file_path, "wb") as file:
                            file.write(response.content)

                        # Open the PDF file
                        with open(file_path, "rb") as file:
                            # Initialize a PDF reader object
                            reader = PyPDF2.PdfReader(file)

                            # Extract text from each page
                            text = ""
                            for page in reader.pages:
                                text += page.extract_text()
                                # hello

                    folder_index += 1

                href_list = []

                # Close the current tab or window
                driver.close()

                # Switch back to the main tab or window
                driver.switch_to.window(driver.window_handles[0])
            else:
                num += 1

        # locating next_button
        time.sleep(2)
        next_button = driver.find_element(By.CLASS_NAME, 'k-i-arrow-60-right')
        time.sleep(5)
        next_button.click()
        time.sleep(5)

if __name__ == '__main__':
    url = 'https://juris.ohchr.org/SearchResult'
    download_pdf(url)
