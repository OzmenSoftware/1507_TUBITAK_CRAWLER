import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver_path = 'C:/Users/Çağdaş Halil Bacanak/OneDrive/Masaüstü/chromedriver.exe'

options = Options()
options.add_experimental_option('prefs', {
    "download.default_directory": r"C:\Users\Çağdaş Halil Bacanak\OneDrive\Masaüstü\Backround\1507 Crawlers\Finans\PKF",
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
})
options.add_experimental_option("detach", True)

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# Ana sayfayı aç
driver.get('https://www.pkfizmir.com/ekonomi_makaleleri.php?lang=tr')
wait = WebDriverWait(driver, 20)

try:
    ekonomi_makaleler = wait.until(EC.presence_of_element_located((By.ID, 'content')))

    linkler = ekonomi_makaleler.find_elements(By.TAG_NAME, 'a')

    for index, link in enumerate(linkler):
        href = link.get_attribute('href')
        if href:
            original_window = driver.current_window_handle
            driver.execute_script("window.open(arguments[0]);", href)
            time.sleep(2)

except Exception as e:
    print("Bir hata oluştu:")
    print(str(e))
    traceback.print_exc()

finally:
    driver.quit()