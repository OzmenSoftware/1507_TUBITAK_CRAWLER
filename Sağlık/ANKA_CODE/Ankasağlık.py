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

# Haberleri tutmak için bir sözlük oluşturma
dict_haber = {"URL": [], "Başlık": [], "Makale": []}

options = Options()
options.add_experimental_option("detach", True)

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
driver.get('https://ankahaber.net/')

wait = WebDriverWait(driver, 20)

search_key = 'Sağlık'

# Arama işlemleri
top_bar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'top-bar')))
search_icon = top_bar.find_element(By.CLASS_NAME, 'search-icon')
search_icon.click()

search_box = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'search-box')))
search_box.click()

search_box_input = search_box.find_element(By.ID, 'search')
search_box_input.send_keys(search_key)
search_box_input.send_keys(Keys.ENTER)
time.sleep(5)

# Sayacı başlat
click_count = 0

while True:
    try:
        # 'container' sınıfına sahip öğeyi bul
        container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'container')))
        
        # İçerideki 'btn btn-mod btn-border btn-large' sınıfına sahip butonu bul
        button = container.find_element(By.XPATH, '//*[@id="form1"]/section/div/div/div/div/div[3]/a')
        
        # Butonu görünür yapmak için kaydır
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(5)  # Öğenin tam olarak görünür hale gelmesi için bekle

        # Butonun tıklanabilir olup olmadığını kontrol et
        if button.is_displayed() and button.is_enabled():
            button.click()
            click_count += 1
            print(f"Butona {click_count}. kez tıklandı.")

            # Tıklamadan sonra 1 saniye bekle
            time.sleep(5)

            # 1000 tıklama sonrası döngüyü kır
            if click_count >= 100:
                print("100 tıklama tamamlandı, döngü sonlandırılıyor...")
                break

        else:
            print("Buton tıklanabilir değil, döngü devam ediyor...")

    except Exception as e:
        print("Butona tıklanırken hata oluştu veya buton bulunamadı:", e)
        # Hata oluştuğunda döngüyü sonlandırmak yerine devam edelim
        continue
    
try:
    
    # Makale bağlantılarını bulma
    container = wait.until(EC.presence_of_element_located((By.ID, 'KategoriHaberListesiAra')))
    links = container.find_elements(By.TAG_NAME, 'a')

    # Dosya yolu
    folder_path = r'C:\Users\User\OneDrive\Masaüstü\Backround\1507 Crawlers\Sağlık\ANKA'

    # Dosya isimleri search_key'e göre oluşturma
    csv_file_name = f'{search_key}.csv'
    txt_file_name = f'{search_key}.txt'

    # Dosya yollarını oluşturma
    csv_file_path = os.path.join(folder_path, csv_file_name)
    txt_file_path = os.path.join(folder_path, txt_file_name)

    # Her bir bağlantıyı döngüyle işleme
    for link in links:
        try:
            # Bağlantıyı yeni bir sekmede açın
            driver.execute_script("window.open(arguments[0]);", link.get_attribute('href'))
            wait.until(EC.number_of_windows_to_be(2))

            new_window = [window for window in driver.window_handles if window != driver.current_window_handle][0]
            driver.switch_to.window(new_window)

            # 2 saniye bekle
            time.sleep(2)

            # URL'yi alın
            url = driver.current_url

            try:
                # Başlığı ve makale metnini alın
                baslik_element = wait.until(EC.presence_of_element_located((By.ID, 'Baslik')))
                baslik = baslik_element.text

                makale_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'col-lg-9')))
                paragraflar = makale_element.find_elements(By.TAG_NAME, 'p')
                makale = ' '.join(paragraf.text for paragraf in paragraflar)

                # Verileri dict_haber'a ekleyin
                dict_haber["URL"].append(url)
                dict_haber["Başlık"].append(baslik)
                dict_haber["Makale"].append(makale)

                # Bilgileri yazdırın
                print(f"URL: {url}")
                print(f"Başlık: {baslik}")
                print(f"Makale: {makale[:200]}...")  # Makalenin sadece ilk 200 karakterini yazdır

                # Her bir makaleyi dosyaya yazın
                with open(txt_file_path, 'a', encoding='utf-8') as file:
                    file.write(f"URL: {url}\n")
                    file.write(f"Başlık: {baslik}\n")
                    file.write(f"Makale: {makale}\n")
                    file.write("\n" + "-"*80 + "\n\n")

                # CSV dosyasını güncelleyin
                df = pd.DataFrame(dict_haber)
                df.to_csv(csv_file_path, index=False)
                print(f"Veriler '{csv_file_path}' dosyasına yazıldı.")

            except Exception as inner_e:
                print(f"Makale bilgileri alınırken hata oluştu: {inner_e}")

            finally:
                # Yeni sekmeyi kapatın ve orijinal pencereye geri dönün
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[0])
                driver.close()

except Exception as e:
    print(f"Genel bir hata oluştu: {e}")