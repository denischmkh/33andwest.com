import os
import datetime
import subprocess
from load_django import *
from parser_app.models import Status


scripts = [
    # "1_33andwest.com.py",
    # "2_atc-live.com.py",
    # "3_august.agency.py",
    # "4_billions.com.py",
    # "5_caa.com.py",
    "6_chameleon.unitedtalent.com.py",
    # "7_groundcontroltouring.com.py",
    # "8_highroadtouring.com.py",
    # "9_itb.co.uk.py",
    # "10_mbartists.co.uk.py",
    # "11_prensadanna.com.py",
    # "12_primarytalent.com.py",
    # "13_soundtalentgroup.com.py",
    # "14_spinartistagency.com.py",
    # "15_tbaagency.com.py",
    # "16_teamwass.com.py",
    # "17_unitedtalent.com.py",
    # "18_wmeagency.com.py",
    # "19_xraytouring.com.py",
    # "20_pitchperfectpr.com.py",
    # "21_pitchandsmith.com.py",
    # "22_talentxent.com.py",
    # "23_addition-llc.com.py",
    # "24_loaded.gg.py",
    # "25_stokedpr.com.py",
    # "26_audibletreats.com.py",
    # "27_bighassle.com.py",
    # "28_grandstandhq.com.py",
    # "29_tellallyourfriendspr.com.py",
    # "30_biz3.net.py",
    # "31_orienteer.us.py",
    # "32_sacksco.com.py",
    # "33_murraychalmers.com.py",
    # "34_mbcpr.com.py",
    # "35_chuffmedia.com.py",
    # "36_braceyourselfpr.com.py",
    # "37_tkoco.com.py",
    # "38_rocnation.com.py",
    # "39_redlightmanagement.com.py",
    # "40_feldman-agency.com.py",
    # "41_atomsplitterpr.com.py",
    # "42_sropr.com.py",
    # "43_dynamictalent.com.py",
    # "44_13artists.com.py",
    # "45_satellite414.com.py",
    # "46_continentaltouring.us.py",
    # "47_freetradeagency.co.uk.py",
    # "48_girlieaction.com.py",
    # "49_publiccitypr.com.py"
]
for script in scripts:
    full_path = os.path.join(os.getcwd(), script)
    print(f"\n🚀 Running {script}...\n")
    site_name = script.replace('.py', '')
    try:
        result = subprocess.run(["python3", full_path], check=True, capture_output=True, text=True)
        print(result.stdout)
        Status.objects.create(site=site_name, status="OK", date=datetime.date.today())
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script}:")
        print(e.stderr)
        Status.objects.create(site=site_name, status="Error", date=datetime.date.today())
    except Exception as e:
        print(f"❌ Unexpected error in {script}: {e}")
        Status.objects.create(site=site_name, status="Error", date=datetime.date.today())