import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver_path = r'C:\Users\User\OneDrive\Masaüstü\chromedriver.exe'
dict_haber = {"URL": [], "Başlık": [], "Alt Başlık": [], "Makale": []}
options = Options()
options.add_experimental_option("detach", True)

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
driver.get('https://www.aa.com.tr/tr')

wait = WebDriverWait(driver, 20)

# Cookie policy accept
cookie_policy_element = wait.until(EC.presence_of_element_located((By.ID, 'cookiepolicy')))
cookie_accept_button = cookie_policy_element.find_element(By.ID, 'cookieaccept')
cookie_accept_button.click()

# Click search button
ara_buton = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="arama-form"]/i')))
ara_buton.click()

# Enter "Ekonomi" into the search field and submit
arama_alani = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#arama-form > input')))
search_key = 'Finans'
arama_alani.send_keys(search_key)
arama_alani.send_keys(Keys.ENTER)

# Navigate to search results page
driver.get('https://www.aa.com.tr/tr/search/?s=Finans#')

# Select the appropriate option from the dropdown
form_control_elementi = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'form-control')))
form_control_elementi.click()

ekonomi_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="field-cat"]/option[6]')))
ekonomi_option.click()

arama_button = wait.until(EC.element_to_be_clickable((By.ID, 'arama')))
arama_button.click()

# Click "Daha" button until no more articles are loaded or max attempts reached
more_pages = True
sayac = 1  # Başlangıçta sayfa sayacını 1 olarak ayarlıyoruz
total_clicks = 0  # Toplam tıklama sayısı
max_total_clicks = 260  # Maksimum toplam tıklama sayısı
clicks_since_last_reset = 0  # Son sıfırlamadan bu yana yapılan tıklama sayısını artırıyoruz
previous_page_content = driver.page_source  # İlk sayfa içeriğini sakla

while more_pages and total_clicks < max_total_clicks:
    try:
        # Click the "Daha" button
        daha_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'button-daha')))
        daha_button.click()
        print(f"{sayac}. sayfaya tıklandı")  # Sayfa numarasını yazdırıyoruz
        sayac += 1  # Sayaç değerini bir artırıyoruz
        total_clicks += 1  # Toplam tıklama sayısını artırıyoruz
        clicks_since_last_reset += 1  # Son sıfırlamadan bu yana yapılan tıklama sayısını artırıyoruz

        # Wait for the new content to load
        time.sleep(2)  # Her sayfa arasında 1 saniye bekleyin

        if clicks_since_last_reset >= 10:
            # 10 tıklamadan sonra 10 saniye bekle
            print("10 tıklamadan sonra bekleniyor...")
            time.sleep(10)
            clicks_since_last_reset = 0  # Tıklama sayısını sıfırla

        # Check if the page content has changed
        current_page_content = driver.page_source  # Şu anki sayfa içeriğini al
        if current_page_content == previous_page_content:
            print("Sayfa içeriği değişmedi, site yenileniyor.")
            driver.refresh()  # Sayfayı yenile
            time.sleep(5)  # Yenileme sonrası bekleme süresi
            previous_page_content = driver.page_source  # Yeni sayfa içeriğini sakla
            clicks_since_last_reset = 0  # Tıklama sayısını sıfırla
            sayac = 1  # Sayacı sıfırla
        else:
            previous_page_content = current_page_content  # Sayfa içeriğini güncelle

    except Exception as e:
        print(f"Hata oluştu veya daha butonu bulunamadı: {e}")
        driver.refresh()  # Hata durumunda sayfayı yenile
        time.sleep(5)  # Yenileme sonrası bekleme süresi
        previous_page_content = driver.page_source  # Yeni sayfa içeriğini sakla
        clicks_since_last_reset = 0  # Tıklama sayısını sıfırla
        sayac = 1  # Sayacı sıfırla

# İşlem bittikten sonra sayfanın en üst kısmına kaydır
driver.execute_script("window.scrollTo(0, 0);")
print("Sayfanın en üst kısmına kaydırıldı")

# Get all article links
makale_basliklari = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="tab-content"]//h4')))

for baslik_element in makale_basliklari:
    try:
        baslik_text = baslik_element.text
        baslik_element.click()
        time.sleep(2)

        try:
            # Collect title and content details
            baslik = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'detay-spot-category')))
            baslik_metin = baslik.find_element(By.TAG_NAME, 'h1').text
            ikinci_baslik_metin = baslik.find_element(By.TAG_NAME, 'h4').text

            icerik = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'col-md-10')))
            icerik_paragraflar = icerik.find_elements(By.TAG_NAME, 'p')
            icerik_metni = '\n'.join([p.text for p in icerik_paragraflar])
            
            # Save data to dictionary
            dict_haber['URL'].append(driver.current_url)
            dict_haber['Başlık'].append(baslik_metin)
            dict_haber["Alt Başlık"].append(ikinci_baslik_metin)
            dict_haber["Makale"].append(icerik_metni)
            
            # Write to file
            file_path = r'C:\Users\User\OneDrive\Masaüstü\Backround\1507 Crawlers\Finans\AA\Finans.txt'
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(f"URL: {driver.current_url}\n")
                file.write(f"\nBaşlık: {baslik_metin}\n")
                file.write(f"Alt Başlık: {ikinci_baslik_metin}\n\n")
                file.write(f"Makale İçeriği:\n{icerik_metni}\n\n")
                
            # Write all articles to CSV
            df = pd.DataFrame(dict_haber)
            csv_file_path = r'C:\Users\User\OneDrive\Masaüstü\Backround\1507 Crawlers\Finans\AA\aa_finans_df.csv'
            os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
            df.to_csv(csv_file_path, index=False)
            print(f"Veriler '{csv_file_path}' dosyasına yazıldı.")
            
            print(f"Makale '{baslik_metin}' {file_path} dosyasına yazıldı.")
        except Exception as inner_e:
            print(f"Makale bilgileri alınırken hata oluştu: {inner_e}")
            driver.back()
            time.sleep(2)
            continue

    except Exception as e:
        print(f"Makale işlenirken hata oluştu: {e}")
        driver.back()
        time.sleep(2)
        continue

    driver.back()
    time.sleep(2)

# Cleanup
driver.quit()
