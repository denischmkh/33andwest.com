import os
import datetime
import subprocess
import sys
import time

from load_django import *
from parser_app.models import Status


scripts = [
    "1_33andwest.com.py",
    "2_atc-live.com.py",
    "6_chameleon.unitedtalent.com.py",
    "8_highroadtouring.com.py",
    "9_itb.co.uk.py",
    "10_mbartists.co.uk.py",
    "11_prensadanna.com.py",
    "13_soundtalentgroup.com.py",
    "14_spinartistagency.com.py",
    "15_tbaagency.com.py",
    "18_wmeagency.com.py",
    "20_pitchperfectpr.com.py",
    "21_pitchandsmith.com.py",
    "22_talentxent.com.py",
    "26_audibletreats.com.py",
    "27_bighassle.com.py",
    "29_tellallyourfriendspr.com.py",
    "30_biz3.net.py",
    "31_orienteer.us.py",
    "33_murraychalmers.com.py",
    "35_chuffmedia.com.py",
    "37_tkoco.com.py",
    "38_rocnation.com.py",
    "40_feldman-agency.com.py",
    "41_atomsplitterpr.com.py",
    "42_sropr.com.py",
    "44_13artists.com.py",
    "45_satellite414.com.py",
    "46_continentaltouring.us.py",
    "47_freetradeagency.co.uk.py",
    "48_girlieaction.com.py",
    "49_publiccitypr.com.py",
    '55_wecarealotpr.com.py',
    "60_ebmediapr.com.py",
    "61_7smgmt.com.py",
    "63_qprime.com.py",
    "66_imran-malik.com.py",
    "68_ayita.com.py",
    "72_sheltermusic.com.py",
    "73_4ad.com.py",
    "74_minttalentgroup.com.py",
    "77_chromaticpr.com.py",
    "80_asgard-uk.com.py",
    "81_concertedefforts.com.py",
    "82_tbaagency.com.py",
    "88_outermostagency.com.py",
    "90_getinpr.com.py",
    "91_dawbell.com.py",
    "92_motherartists.com_booking.py",
    "93_motherartists.com_mgmt.py",
    "95_republicrecords.com.py",
    "96_rcarecords.com.py",
    "97_onefiinix.com.py",
    "98_tmwrk.net.py",
    "99_crushmusic.com.py",
    "100_thenealagency.net.py",
    "101_hometown-talent.com.py",
    "102_anniversarygroup.com.py",
    "103_paladinartists.com.py",
    "106_independentartistgroup.com.py",
    "107_nge-booking.com.py",
    "108_warmagency.com.py",
    "118_makewake.net.py",
    "119_armige.com.py",
    "120_anna-agency.nl.py",
    "123_2bentertainment.net.py",
    "140_panacherock.com.py",
    "142_thekurlandagency.com.py",
    "55_wecarealotpr.com.py",
    "92_motherartists.com_booking.py",
    "93_motherartists.com_mgmt.py",
]


for script in scripts:
    full_path = os.path.join(os.path.dirname(__file__), script)
    print(f"\n🚀 Running {script}...\n")
    site_name = script.replace('.py', '')
    site_name = ''.join(site_name.split('_')[1:])
    try:
        result = subprocess.run(["python3", full_path], check=True, capture_output=True, text=True)
        print(result.stdout)
        Status.objects.update_or_create(
            site=site_name,
            defaults={
                'status': 'OK',
                'date': datetime.date.today()
            }
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script}:")
        print("stdout:\n", e.stdout)
        print("stderr:\n", e.stderr)
        Status.objects.update_or_create(
            site=site_name,
            defaults={
                'status': 'Error',
                'date': datetime.date.today()
            }
        )
    except Exception as e:
        print(f"❌ Unexpected error in {script}: {e}")
        Status.objects.update_or_create(
            site=site_name,
            defaults={
                'status': 'Error',
                'date': datetime.date.today()
            }
        )
    time.sleep(1)
