from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# ChromeDriver'ı otomatik olarak indirip kuracak
service = Service(ChromeDriverManager().install())

# Chrome WebDriver nesnesini oluştur
driver = webdriver.Chrome(service=service)

# Ekran görüntüsü almak için bir fonksiyon
def take_screenshot(step_name):
    folder_path = 'screenshots'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    driver.save_screenshot(f"{folder_path}/{step_name}_{int(time.time())}.png")

# Fırat Üniversitesi Mühendislik Fakültesi web sayfasını aç
driver.get('https://muhendislikf.firat.edu.tr/tr')
take_screenshot('homepage')

# Web sayfasının başlığını kontrol et
expected_title = "Ana Sayfa | Fırat Üniversitesi"
actual_title = driver.title
assert expected_title in actual_title, f"Beklenen başlık '{expected_title}' bulunamadı. Gerçek başlık: '{actual_title}'"

# 'Bölümler' linkini bul ve tıkla
try:
    departments_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Bölümlerimiz'))
    )
    departments_link.click()
    take_screenshot('departments_page')
except TimeoutException:
    print("Bölümlerimiz linki bulunamadı veya tıklanabilir değil.")

# 'Yazılım Mühendisliği' bölümüne git
try:
    yazilim_müh_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Yazılım Mühendisliği'))
    )
    # Elementin görünür olmasını sağla
    driver.execute_script("arguments[0].scrollIntoView(true);", yazilim_müh_link)
    # JavaScript ile tıklama işlemi yap
    driver.execute_script("arguments[0].click();", yazilim_müh_link)
    take_screenshot('yazilim_müh')
except TimeoutException:
    print("Yazılım Mühendisliği linki bulunamadı veya tıklanabilir değil.")
except ElementClickInterceptedException:
    print("Yazılım Mühendisliği linkine tıklanamadı, başka bir element engelliyor olabilir.")

# Testler tamamlandıktan sonra tarayıcıyı kapat
driver.quit()
