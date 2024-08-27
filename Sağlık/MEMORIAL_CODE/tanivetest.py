import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

# CSV ve TXT dosyaların yolu 
csv_file_path = r'C:\Users\User\OneDrive\Masaüstü\Backround\1507 Crawlers\Sağlık\MEMORIAL\tanivetest.csv'
txt_file_path = r'C:\Users\User\OneDrive\Masaüstü\Backround\1507 Crawlers\Sağlık\MEMORIAL\tanivetest.txt'

# Chrome seçenekleri
chrome_path = r"C:\Users\User\OneDrive\Masaüstü\Backround\1507 Crawlers\chromedriver.exe"

options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--start-maximized")
# User-Agent kullanmak isterseniz
# ua = UserAgent()
# random_user_agent = ua.random
# options.add_argument(f"user-agent={random_user_agent}")

# WebDriver servisi
service = Service(chrome_path)
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.memorial.com.tr/')

wait = WebDriverWait(driver, 20)

# Dictionary to store articles
dict_makaleler = {'Soru': [], 'Cevap': []}

def click_element(xpath, wait):
    element = wait.until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    element.click()

time.sleep(2)

# Accept cookies
click_element('//*[@id="cookieseal-banner-accept"]', wait)
time.sleep(1.5)

# Navigate to Articles section
click_element('/html/body/div[5]/header/nav/div/div[2]/ul/li[7]/a', wait)
time.sleep(1.5)

# Navigate to Health section
click_element('/html/body/main/section[2]/div/div/div[5]/a/span', wait)
time.sleep(1.5)

# Save original window handle
original_window = driver.current_window_handle

while True:
    try:
        # Get all articles container
        makale_kapsayici = wait.until(EC.presence_of_element_located((By.ID, 'testList')))

        # Get all article links
        links = makale_kapsayici.find_elements(By.CLASS_NAME, 'col-3.mini-image-box')

        for link_element in links:
            link = link_element.find_element(By.TAG_NAME, 'a').get_attribute('href')

            # Open link in new tab
            driver.execute_script("window.open(arguments[0]);", link)
            time.sleep(1.5)

            # Switch to new tab
            new_window = [window for window in driver.window_handles if window != original_window][0]
            driver.switch_to.window(new_window)

            # Wait for the body of the page to load
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            body_text = driver.find_element(By.TAG_NAME, 'body').text

            # Check if "Not Found" error exists
            if "Not Found" in body_text:
                print("404 Not Found hatası bulundu çıkılıyor")
                driver.close()
                driver.switch_to.window(original_window)
                continue

            # Find all articles
            articles = driver.find_elements(By.CLASS_NAME, 'article.general-title-style')

            for article in articles:
                # Find h2 and h3 elements
                h_elements = article.find_elements(By.XPATH, './/h2 | .//h3')
                for header in h_elements:
                    soru = header.text

                    # Get the following sibling elements (p, ul, ol, li)
                    try:
                        cevap_element = header.find_element(By.XPATH, "following-sibling::*[self::p or self::ul or self::ol or self::li]")
                        if cevap_element.tag_name in ['ul', 'ol']:
                            cevap = "\n".join([li.text for li in cevap_element.find_elements(By.TAG_NAME, 'li')])
                        else:
                            cevap = cevap_element.text
                    except:
                        cevap = ''

                    dict_makaleler['Soru'].append(soru)
                    dict_makaleler['Cevap'].append(cevap)

            # Save data to CSV and TXT files
            df = pd.DataFrame(dict_makaleler)
            df.to_csv(csv_file_path, index=False, encoding='utf-8')

            with open(txt_file_path, 'w', encoding='utf-8') as file:
                for soru, cevap in zip(dict_makaleler['Soru'], dict_makaleler['Cevap']):
                    file.write(f"Soru: {soru}\nCevap: {cevap}\n\n")

            # Close current tab and switch back to original
            driver.close()
            driver.switch_to.window(original_window)
            time.sleep(1.5)

    except Exception as e:
        print(f"Hata: {e}")
        break  # Exit the loop in case of error
