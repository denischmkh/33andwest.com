import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,NoSuchAttributeException, InvalidArgumentException,TimeoutException
from _3_august_agency import parse3
from _4_billions_com import parse4
from _5_caa_com import parse5
from pyvirtualdisplay import Display

dp = Display()
dp.start()


options = uc.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-notifications")
options.add_argument("--lang=en-US")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

from config import VERSION_MAIN
driver = uc.Chrome(options=options, version_main=VERSION_MAIN)
wait = WebDriverWait(driver, 20)


scripts = [parse3, parse4, parse5]

for script in scripts:
    print(f'Функция {script.__name__} начала отрабатывать')
    script(driver=driver)
    print('Функция отработала')


dp.stop()