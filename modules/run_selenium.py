import datetime
import os
import re
import subprocess
import signal
import time

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
from _94_insideout_agency import parse94
from _104_lb_agency_net import parse104
from _105_tap_music_com import parse105
from _109_corsonagency_com import parse109
from _110_paramountartists_com import parse110
from _111_mickmgmt_com import parse111
from _112_pure_represents_com import parse112
from _113_ivpr_com import parse113
from _114_unitedagents_co_uk import parse114
from _115_curtisbrown_co_uk import parse115
from _116_insanity_com import parse116
from _117_analog_a_com import parse117
from _121_goodmachinepr_com import parse121
from _122_culturewave_la import parse122
from _124_r_m_art import parse124
from _125_clockworkartists_co_uk import parse125
from _126_sequelmusicgroup_com import parse126
from _127_intertalentgroup_com import parse127
from _128_arcade_talent_com import parse128
from _130_thebullittagency_com import parse130
from _131_mushroombooking_com import parse131
from _133_amodeagency_com import parse133
from _134_fatcatmusicgroup_com import parse134
from _135_fatcatmusicgroup_com import parse135
from _136_t_s_agency_com import parse136
from _137_kmgmt_com import parse137
from _138_strangetalent_agency import parse138
from _139_atcmanagement_com import parse139
from _141_leadermgmt_com import parse141
from config import VERSION_MAIN
from parser_app.models import Status

scripts = [
    parse3, parse4, parse5, parse7, parse12, parse16, parse17, parse19, parse23, parse24, parse25, parse28, parse32,
    parse34, parse36, parse39, parse43, parse51, parse53, parse54, parse56, parse62, parse64, parse65, parse67,
    parse69, parse70, parse71, parse76, parse78, parse79, parse83, parse84, parse85, parse86, parse87, parse89,
    parse94, parse104, parse105, parse109, parse110, parse111, parse112, parse113, parse114, parse115,
    parse116, parse117, parse121, parse122, parse124, parse125, parse126, parse127, parse128, parse130,
    parse131, parse133, parse134, parse135, parse136, parse137, parse138, parse139, parse141
]

# Проверка на висячий дисплей
MAX_RETRIES = 5
RETRY_DELAY = 15  # секунд

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


def start_driver_with_retries():
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"\n🔁 Попытка запуска #{attempt}")
        kill_xvfb()
        time.sleep(1)

        try:
            dp = Display(visible=False, size=(1280, 720))
            dp.start()
            print(f"[+] Виртуальный дисплей запущен: :{dp.display}")
        except Exception as e:
            print(f"❌ Ошибка запуска дисплея: {e}")
            time.sleep(RETRY_DELAY)
            continue

        try:
            options = uc.ChromeOptions()
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-notifications")
            options.add_argument("--lang=en-US")
            options.add_argument(
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

            driver = uc.Chrome(options=options, version_main=VERSION_MAIN)
            wait = WebDriverWait(driver, 20)

            print("✅ Браузер успешно запущен.")
            return driver, dp  # успех, возвращаем driver и дисплей

        except Exception as e:
            print(f"❌ Ошибка запуска браузера: {e}")
            try:
                dp.stop()
            except Exception:
                pass
            time.sleep(RETRY_DELAY)

    print("🛑 Все попытки запуска не увенчались успехом.")
    return None, None


# Пробуем запустить браузер
driver, dp = start_driver_with_retries()
if not driver:
    exit(1)
wait = WebDriverWait(driver, 20)

# Скрипты

def extract_domain(module_name: str) -> str:
    name = re.sub(r"^_\d+_", "", module_name)
    domain = name.replace("_", ".")
    return domain

for script in scripts:
    print(f"Function {script.__name__} {script.__module__} has started")
    site_name = extract_domain(script.__module__)
    try:
        script(driver=driver)
        Status.objects.update_or_create(
            site=site_name,
            defaults={
                'status': 'OK',
                'date': datetime.date.today()
            }
        )
        print(f"Function {script.__name__} has been ended")
    except Exception as e:
        Status.objects.update_or_create(
            site=site_name,
            defaults={
                'status': 'Error',
                'date': datetime.date.today()
            }
        )
        print(f"Function {script.__name__} had errors: {e}")


# Завершение работы
driver.quit()
dp.stop()
print("[+] Дисплей и браузер закрыты.")