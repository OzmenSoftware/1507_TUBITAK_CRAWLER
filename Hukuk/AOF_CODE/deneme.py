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

# Uzantının yolu
extension_path = r'C:\Users\Çağdaş Halil Bacanak\OneDrive\Masaüstü\addguard.crx'

# Dosya yolu
base_path = r'C:\Users\Çağdaş Halil Bacanak\OneDrive\Masaüstü\Backround\1507 Crawlers\Hukuk\AOF'
# Dosya isimleri
baslik = 'aof_soru_cevap_df'

# CSV ve TXT dosyalarının yolları
csv_file_path = os.path.join(base_path, f'{baslik}.csv')
txt_file_path = os.path.join(base_path, 'aof_soru_cevap.txt')

# Web üzerinden User-Agent dizgilerini çek
ua = UserAgent()
random_user_agent = ua.random

# Chrome seçenekleri
options = Options()
options.add_extension(extension_path)  # Uzantıyı ekle
options.add_experimental_option("detach", True)
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--start-maximized")
options.add_argument(f"user-agent={random_user_agent}")

# WebDriver servisi
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://aof.sorular.net/adalet-bolumu')

wait = WebDriverWait(driver, 20)

# Banned yazıyı tanımlayın
banned_texts = [
    "Temel Bilgi Teknolojileri 1 Dersi Deneme Sınavları",
    "Almanca 1 Dersi Deneme Sınavları",
    "Fransızca 1 Dersi Deneme Sınavları",
    "Ingilizce 1 Dersi Deneme Sınavları",
    "Almanca 2 Dersi Ünite Özetleri ve Çalışma Soru Cevapları",
    "Temel Bilgi Teknolojileri 2 Dersi Deneme Sınavları",
    "Fransızca 2 Dersi Deneme Sınavları",
    "Ingilizce 2 Dersi Deneme Sınavları",
    "Atatürk İlkeleri Ve İnkılap Tarihi 1 Dersi Deneme Sınavları",
    "Türk Dili 1 Dersi Deneme Sınavları",
    "Atatürk İlkeleri Ve İnkılap Tarihi 2 Dersi Deneme Sınavları",
    "Türk Dili 2 Dersi Deneme Sınavları",
    "İnsan Hakları Ve Kamu Özgürlükleri Dersi Ünite Özetleri ve Çalışma Soru Cevapları"
]

time.sleep(20)

# AdBlock uzantısının açtığı sayfayı kapatıp ana sayfaya dön
def close_adblock_page():
    original_window = driver.current_window_handle
    for window in driver.window_handles:
        if window != original_window:
            driver.switch_to.window(window)
            driver.close()
    driver.switch_to.window(original_window)

close_adblock_page()  # AdBlock sayfasını kapat

# Hedef sayfayı tekrar yükle
driver.get('https://aof.sorular.net/adalet-bolumu')

# 'col-12 col-lg-8' sınıfına sahip tüm elementleri bekle
adalet_bolumu_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'col-12.col-lg-8')))

# Orijinal sekmeyi kaydet
original_window = driver.current_window_handle

# Verileri TXT dosyasına kaydet
def write_to_file(text, file_path):
    """Verilen metni belirtilen dosyaya yazar."""
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(text + '\n')

# CSV dosyasını başlat
df = pd.DataFrame(columns=['Soru', 'Cevap'])
df.to_csv(csv_file_path, index=False, encoding='utf-8')

for element in adalet_bolumu_elements:
    links = element.find_elements(By.TAG_NAME, 'a')  # Linkleri bul
    for link in links:
        try:
            # JavaScript kullanarak bağlantıyı yeni sekmede açma
            driver.execute_script("window.open(arguments[0]);", link.get_attribute('href'))
            
            # Yeni sekmeye geçiş yap
            new_window = [window for window in driver.window_handles if window != original_window][0]
            driver.switch_to.window(new_window)
            
            # Sayfanın yüklenmesini bekle
            time.sleep(5)

            # Sayfanın içeriğini kontrol et
            page_text = driver.page_source
            if any(banned_text in page_text for banned_text in banned_texts):
                print("Sayfada yasaklı yazı bulundu")
                driver.close()
                driver.switch_to.window(original_window)
                continue  # Bir sonraki linke geç
            
            # Sayfadaki tüm 'deneme_sinavlari' öğelerini bekle
            deneme_sinavlari = wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div/div[2]')))

            # Orijinal sekmeyi kaydet
            original_window_second = driver.current_window_handle

            for deneme_sinavi in deneme_sinavlari:
                try:
                    # Her deneme_sinavi öğesi bir bağlantı ise, bağlantıyı tıklamak için aşağıdaki kodu kullanın
                    time.sleep(1.5)
                    links = deneme_sinavi.find_elements(By.CLASS_NAME, 'btn.bg-primary.btn-labeled.btn-sm.ml-1.mb-1')

                    for link in links:
                        try:
                            
                            # JavaScript kullanarak bağlantıyı yeni bir sekmede açma
                            driver.execute_script("window.open(arguments[0], '_blank');", link.get_attribute('href'))
                            
                            # Yeni sekmeye geçiş yap
                            second_window = [window for window in driver.window_handles if window != driver.current_window_handle][1]
                            driver.switch_to.window(second_window)
                            
                            # 'sorular' içindeki tüm elemanları al
                            sorular = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'w-100.order-2.order-md-1')))
                            
                            click_count = 0
                            
                            while click_count < 20:                     
                                try:
                                    # Butonu bekleyin ve bulmaya çalışın
                                    buton = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn.btn-light.btn-sm.soru-secenek-harf')))
                                    
                                    if buton:
                                        # Butona tıklayın
                                        buton.click()
                                        print("Butona tıklandı.")

                                        # Tıklamalar arasında kısa bir bekleme süresi koyun
                                        time.sleep(0)
                                        
                                        click_count += 1
                                    else:
                                        # Buton bulunamazsa döngüden çıkın
                                        print("Buton bulunamadı, döngü bitiriliyor.")
                                        break

                                except Exception as e:
                                    # Hata oluşursa, hata mesajını yazdırın ve döngüyü bitirin
                                    print(f"Bir hata oluştu: {e}")
                                    break
                               
                            for soru in sorular:
                                try:
                                    # 'card' sınıfına sahip olan elemanları bul
                                    cards = soru.find_elements(By.CLASS_NAME, 'card')
                                    
                                    for card in cards:
                                        # 'card' elemanı içerisindeki <h4> etiketlerini bul
                                        h4_elements = card.find_elements(By.TAG_NAME, 'h4')
                                        
                                        for h4 in h4_elements:
                                            # 'h4' etiketinin içeriğini al
                                            question_text = h4.text
                                            
                                            # 'Yanıt Açıklaması:' metnini içeren 'strong' etiketi yerine doğru bir yaklaşım
                                            try:
                                                # Cevap metnini almak için ilgili XPath ifadesi
                                                answer_text = card.find_element(By.XPATH, ".//following-sibling::div[contains(@id,'divAnswer')]/p").text
                                            except Exception as e:
                                                answer_text = "Cevap bulunamadı"

                                            # Veriyi CSV ve TXT dosyalarına yaz
                                            data_entry = [question_text, answer_text]
                                            data_df = pd.DataFrame([data_entry], columns=['Soru', 'Cevap'])
                                            data_df.to_csv(csv_file_path, mode='a', header=False, encoding='utf-8', index=False)

                                            # Yazma fonksiyonunu çağırarak soruyu ve cevabı TXT dosyasına kaydet
                                            write_to_file(f"Soru: {question_text}", txt_file_path)
                                            write_to_file(f"Cevap: {answer_text}\n", txt_file_path)

                                except Exception as e:
                                    print(f"Bir hata oluştu: {e}")
                                      
                            driver.close()
                            driver.switch_to.window(original_window_second)
                        except Exception as e:
                            print(f"Bağlantıyı yeni sekmede açarken veya işlem yaparken hata oluştu: {e}")
                            continue
                        
                except Exception as e:
                    print(f"Bağlantıyı yeni sekmede açarken veya işlem yaparken hata oluştu: {e}")
                    continue

            # Yeni sekmeyi kapat ve önceki sekmeye dön
            driver.close()
            driver.switch_to.window(original_window)
            
            # Geri döndükten sonra sayfanın yeniden yüklenmesini bekle
            time.sleep(5)
        except Exception as e:
            print(f"Linke tıklanırken veya sayfayı geri alırken hata oluştu: {e}")

# Tarayıcıyı kapat
driver.quit()
