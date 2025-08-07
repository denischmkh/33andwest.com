import os
import subprocess
from pyvirtualdisplay import Display
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from _3_august_agency import parse3
from _4_billions_com import parse4
from _5_caa_com import parse5
from _7_groundcontroltouring_com import parse7
from _12_primarytalent_com import parse12
from _16_teamwass_com import parse16
from config import VERSION_MAIN


# Проверка на висячий дисплей
try:
    subprocess.run(["pkill", "-f", "Xvfb"], check=True)
    print("🔴 Старые Xvfb-дисплеи завершены")
except subprocess.CalledProcessError:
    print("✅ Нет активных Xvfb-дисплеев")


# Запускаем новый виртуальный дисплей
dp = Display(visible=False, size=(1280, 720))
dp.start()
print("[+] Новый виртуальный дисплей запущен.")

# Настройки Chrome
options = uc.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-notifications")
options.add_argument("--lang=en-US")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

# Запуск Chrome
driver = uc.Chrome(options=options, version_main=VERSION_MAIN)
wait = WebDriverWait(driver, 20)

# Скрипты
scripts = [parse3, parse4, parse5, parse7, parse12, parse16]

for script in scripts:
    print(f"🔄 Функция {script.__name__} начала отрабатывать")
    script(driver=driver)
    print(f"✅ Функция {script.__name__} отработала")

# Завершение работы
driver.quit()
dp.stop()
print("[+] Дисплей и браузер закрыты.")