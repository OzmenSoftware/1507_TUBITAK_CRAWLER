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

# Web üzerinden User-Agent dizgilerini çek
"""ua = UserAgent()
random_user_agent = ua.random"""

# CSV ve TXT dosyaların yolu 
csv_file_path = r'C:\Users\User\OneDrive\Masaüstü\Backround\1507 Crawlers\Sağlık\MEMORIAL\saglikrehberi.csv'
txt_file_path = r'C:\Users\User\OneDrive\Masaüstü\Backround\1507 Crawlers\Sağlık\MEMORIAL\saglikrehberi.txt'

# Chrome seçenekleri
chrome_path = r"C:\Users\User\OneDrive\Masaüstü\Backround\1507 Crawlers\chromedriver.exe"

options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--start-maximized")
#options.add_argument(f"user-agent={random_user_agent}")

# WebDriver servisi
service = Service(chrome_path)
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.memorial.com.tr/')

wait = WebDriverWait(driver, 20)

time.sleep(2)

dict_makaleler = {'Soru':[],'Cevap':[]}

def click_element(xpath, wait):
    element = wait.until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    element.click()
    
time.sleep(2)
    
# Cookie
click_element('//*[@id="cookieseal-banner-accept"]', wait)
time.sleep(1.5)
# Makale
click_element('/html/body/div[5]/header/nav/div/div[2]/ul/li[7]/a', wait)
time.sleep(1.5)
# Sağlık 
click_element('/html/body/main/section[2]/div/div/div[2]/a/span', wait)
time.sleep(1.5)

# Orijinal sekmeyi kaydet
original_window = driver.current_window_handle

while True:
    # Bütün makaleleri al
    makale_kapsayici = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="articleList"]')))

    # Makale bağlantılarını al
    links = makale_kapsayici.find_elements(By.CLASS_NAME, 'col-6')

    for link_element in links:
        try:
            link = link_element.find_element(By.TAG_NAME, 'a').get_attribute('href')

            driver.execute_script("window.open(arguments[0]);", link)

            new_window = [window for window in driver.window_handles if window != original_window][0]
            driver.switch_to.window(new_window)
            time.sleep(1.5)
 
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            
            body_text = driver.find_element(By.TAG_NAME, 'body').text
            if "Not Found" in body_text:
                print(f"{link} adresinde 404 Not Found hatası oluştu.")
                driver.close()
                driver.switch_to.window(original_window)
                continue

            articles = driver.find_elements(By.CLASS_NAME, 'article.general-title-style')

            for article in articles:
                try:
                    h_elements = article.find_elements(By.XPATH, './/h2 | .//h3')
                    for header in h_elements:
                        soru = header.text
                        
                        cevap_element = header.find_element(By.XPATH, "following-sibling::*[self::p or self::ul or self::ol or self::li]")
                
                        cevap_element.tag_name in ['ul', 'ol']
                        cevap = "\n".join([li.text for li in cevap_element.find_elements(By.TAG_NAME, 'li')])
                        cevap = cevap_element.text
                    
                        dict_makaleler['Soru'].append(soru)
                        dict_makaleler['Cevap'].append(cevap)
                        
                except Exception as e:
                    print(e)
            
            # Veriyi CSV ve TXT olarak kaydet
            df = pd.DataFrame(dict_makaleler)
            df.to_csv(csv_file_path, index=False, encoding='utf-8')
            with open(txt_file_path, 'w', encoding='utf-8') as file:
                for soru, cevap in zip(dict_makaleler['Soru'], dict_makaleler['Cevap']):
                    file.write(f"Soru: {soru}\nCevap: {cevap}\n\n")

            # Sekmeyi kapat ve geri dön
            driver.close()
            driver.switch_to.window(original_window)

        except Exception as e:
            print(f"Aldığınız Hata mesajı: {e}")
    
    # Pagination (sayfalandırma) ile bir sonraki sayfaya geçiş yap
    try:
        # "Sonraki Sayfa" butonuna tıkla
        next_page_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'next-arrow'))
        )
        next_page_button.click()
        time.sleep(2)  # Bir sonraki sayfanın yüklenmesini bekleyin
    except Exception as e:
        print(f"Sonraki sayfaya geçişte hata: {e}")
        continue  
