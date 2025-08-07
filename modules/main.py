import os
import subprocess
from pyvirtualdisplay import Display
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from _3_august_agency import parse3
from _4_billions_com import parse4
from _5_caa_com import parse5
from config import VERSION_MAIN

DISPLAY_NUM = ":99"
LOCK_FILE = f"/tmp/.X{DISPLAY_NUM[1:]}-lock"

# Установить переменную окружения для DISPLAY
os.environ["DISPLAY"] = DISPLAY_NUM


# Проверка на висячий дисплей
def clean_display():
    if os.path.exists(LOCK_FILE):
        print(f"[!] Найден lock-файл дисплея {DISPLAY_NUM}: {LOCK_FILE}")
        try:
            # Найти PID Xvfb по lock-файлу
            with open(LOCK_FILE, 'r') as f:
                pid = int(f.read().strip())
            print(f"[!] PID процесса Xvfb: {pid}")

            # Убить процесс
            subprocess.run(["kill", "-9", str(pid)], check=True)
            print("[+] Xvfb процесс завершён.")
        except Exception as e:
            print(f"[!] Не удалось завершить Xvfb: {e}")

        # Удалить lock-файл
        try:
            os.remove(LOCK_FILE)
            print("[+] Lock-файл удалён.")
        except Exception as e:
            print(f"[!] Не удалось удалить lock-файл: {e}")


# Очищаем старый дисплей, если он завис
clean_display()

# Запускаем новый виртуальный дисплей
dp = Display(visible=0, size=(1280, 720), display=99)
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
scripts = [parse3, parse4, parse5]

for script in scripts:
    print(f"🔄 Функция {script.__name__} начала отрабатывать")
    script(driver=driver)
    print(f"✅ Функция {script.__name__} отработала")

# Завершение работы
driver.quit()
dp.stop()
print("[+] Дисплей и браузер закрыты.")