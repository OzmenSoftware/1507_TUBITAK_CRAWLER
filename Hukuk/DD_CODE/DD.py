import time                                                  
import os                                                    
import pandas as pd                                         
from selenium import webdriver                                 
from selenium.webdriver.chrome.service import Service            
from selenium.webdriver.chrome.options import Options          
from selenium.webdriver.common.by import By                     
from selenium.webdriver.support.ui import WebDriverWait           
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.action_chains import ActionChains 
from webdriver_manager.chrome import ChromeDriverManager       

options = Options()
options.add_experimental_option("detach", True)                       
options.add_experimental_option("useAutomationExtension", False)     
options.add_argument("--start-maximized")                            

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://donusumhukuk.com/50-soru-50-cevap-aile-hukuku/')

wait = WebDriverWait(driver, 20)

# Soruları ve cevapları saklayacak sözlük
q_a_dir = {"Soru": [], "Cevap": []}

try:
    # `mkd-post-content-column` sınıfına sahip elementleri bulun
    content_column = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'mkd-post-content-column')))
    
    # `mkd-post-content-column` içindeki `ul` elementlerini bulun
    ul_elements = content_column.find_elements(By.TAG_NAME, 'ul')

    for ul in ul_elements:
        b_elements = ul.find_elements(By.TAG_NAME, 'b')
        for b in b_elements:
            q_a_dir["Soru"].append(b.text)
        
        # `p` elementlerini bul
        p_elements = content_column.find_elements(By.TAG_NAME, 'p')
        for p in p_elements:
            q_a_dir["Cevap"].append(p.text)

    # Dosya yollarını ayarla
    base_path = r'C:\Users\User\OneDrive\Masaüstü\Backround\1507 Crawlers\Hukuk\DD'
    txt_file_path = os.path.join(base_path, 'soru_cevap.txt')
    csv_file_path = os.path.join(base_path, 'soru_cevap.csv')

    # Dizin varsa oluştur
    os.makedirs(os.path.dirname(txt_file_path), exist_ok=True)
    
    # CSV dosyasına veri ekleme
    df = pd.DataFrame(q_a_dir)
    df.to_csv(csv_file_path, index=False)
    
    # TXT dosyasına veri ekle
    try:
        with open(txt_file_path, 'a', encoding='utf-8') as file:
            min_length = min(len(q_a_dir["Soru"]), len(q_a_dir["Cevap"]))
            for i in range(min_length):
                file.write(f"Soru: {q_a_dir['Soru'][i]}\n")
                file.write(f"Cevap: {q_a_dir['Cevap'][i]}\n\n")
    except Exception as e:
        print(f"TXT dosyasına yazma hatası: {e}")
except Exception as e:
    print(e)