from pyvirtualdisplay import Display
import os
import undetected_chromedriver as uc

import shutil
print("🔍 Xvfb path found by shutil.which():", shutil.which("Xvfb"))

display = Display(visible=False, size=(1280, 720))
display.start()
print("DISPLAY:", os.environ.get("DISPLAY"))  # должно быть НЕ ":0"

try:
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = uc.Chrome(options=options)
    driver.get("https://example.com")
    print("Title:", driver.title)
    driver.quit()

finally:
    display.stop()