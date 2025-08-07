import os
import subprocess
import signal
from pyvirtualdisplay import Display
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from _3_august_agency import parse3
from _4_billions_com import parse4
from _5_caa_com import parse5
from _7_groundcontroltouring_com import parse7
from _12_primarytalent_com import parse12
from _16_teamwass_com import parse16
from _17_unitedtalent_com import parse17
from _19_xraytouring_com import parse19
from _23_beacons_ai import parse23
from _24_loaded_gg import parse24
from _25_stokedpr_com import parse25
from _28_grandstandhq_com import parse28
from _32_sacksco_com import parse32
from _34_mbcpr_com import parse34
from _36_braceyourselfpr_com import parse36
from _39_redlightmanagement_com import parse39
from _43_dynamictalent_com import parse43
from _51_gersh_com import parse51
from _53_thegreenroompr_com import parse53
from _54_2911_us import parse54
from _56_nastylittleman_com import parse56
from _62_highrisepr_com import parse62
from _64_thedigitaldept_com import parse64
from _65_indegoot_com import parse65
from _67_earth_agency_com import parse67
from _69_newfrontiertouring_com import parse69
from _70_paquinentertainment_com import parse70
from _71_reybee_com import parse71
from _76_arrivalartists_com import parse76
from _78_platformartists_com import parse78
from _79_artistww_com import parse79
from _83_teamwass_com import parse83
from _84_tourpeachy_com import parse84
from _85_liaisonartists_com import parse85
from _86_selectmusic_com import parse86
from _87_radiusartists_com import parse87
from _89_relianttalent_com import parse89
from config import VERSION_MAIN

scripts = [
    parse3, parse4, parse5, parse7, parse12, parse16, parse17, parse19, parse23, parse24, parse25, parse28, parse32,
    parse34, parse36, parse39, parse43, parse51, parse53, parse54, parse56, parse62, parse64, parse65, parse67,
    parse69, parse70, parse71, parse76, parse78, parse79, parse83, parse84, parse85, parse86, parse87, parse89
]

# Проверка на висячий дисплей
def kill_xvfb():
    try:
        result = subprocess.run(
            ["pgrep", "-f", "Xvfb"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        pids = result.stdout.strip().split("\n")
        for pid in pids:
            if pid.isdigit():
                os.kill(int(pid), signal.SIGKILL)
                print(f"🔴 Убил Xvfb с PID: {pid}")
        if not pids or pids == ['']:
            print("✅ Нет активных Xvfb-процессов")
    except Exception as e:
        print(f"⚠️ Ошибка при завершении Xvfb: {e}")

kill_xvfb()

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


for script in scripts:
    print(f"🔄 Функция {script.__name__} начала отрабатывать")
    script(driver=driver)
    print(f"✅ Функция {script.__name__} отработала")

# Завершение работы
driver.quit()
dp.stop()
print("[+] Дисплей и браузер закрыты.")