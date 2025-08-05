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
    "3_august.agency.py",
    "4_billions.com.py",
    "5_caa.com.py",
    "6_chameleon.unitedtalent.com.py",
    "7_groundcontroltouring.com.py",
    "8_highroadtouring.com.py",
    "9_itb.co.uk.py",
    "10_mbartists.co.uk.py",
    "11_prensadanna.com.py",
    "12_primarytalent.com.py",
    "13_soundtalentgroup.com.py",
    "14_spinartistagency.com.py",
    "15_tbaagency.com.py",
    "16_teamwass.com.py",
    "17_unitedtalent.com.py",
    "18_wmeagency.com.py",
    "19_xraytouring.com.py",
    "20_pitchperfectpr.com.py",
    "21_pitchandsmith.com.py",
    "22_talentxent.com.py",
    "23_beacons.ai.py",
    "24_loaded.gg.py",
    "25_stokedpr.com.py",
    "26_audibletreats.com.py",
    "27_bighassle.com.py",
    "28_grandstandhq.com.py",
    "29_tellallyourfriendspr.com.py",
    "30_biz3.net.py",
    "31_orienteer.us.py",
    "32_sacksco.com.py",
    "33_murraychalmers.com.py",
    "34_mbcpr.com.py",
    "35_chuffmedia.com.py",
    "36_braceyourselfpr.com.py",
    "37_tkoco.com.py",
    "38_rocnation.com.py",
    "39_redlightmanagement.com.py",
    "40_feldman-agency.com.py",
    "41_atomsplitterpr.com.py",
    "42_sropr.com.py",
    "43_dynamictalent.com.py",
    "44_13artists.com.py",
    "45_satellite414.com.py",
    "46_continentaltouring.us.py",
    "47_freetradeagency.co.uk.py",
    "48_girlieaction.com.py",
    "49_publiccitypr.com.py",
    "60_ebmediapr.com.py",
    "61_7smgmt.com.py",
    "62_highrisepr.com.py",
    "63_qprime.com.py",
    "64_thedigitaldept.com.py",
    "65_indegoot.com.py",
    "66_imran-malik.com.py",
    "67_earth-agency.com.py",
    "68_ayita.com.py",
    "69_newfrontiertouring.com.py",
    "70_paquinentertainment.com.py",
    "71_reybee.com.py",
    "72_sheltermusic.com.py",
    "73_4ad.com.py",
    "74_minttalentgroup.com.py",
    "76_arrivalartists.com.py",
    "77_chromaticpr.com.py",
    "78_platformartists.com.py",
    "79_artistww.com.py",
    "80_asgard-uk.com.py",
    "81_concertedefforts.com.py",
    "82_tbaagency.com.py",
    "83_teamwass.com.py",
    "84_tourpeachy.com.py",
    "85_liaisonartists.com.py",
    "86_selectmusic.com.py",
    "87_radiusartists.com.py",
    "88_outermostagency.com.py",
    "89_www.relianttalent.com.py",
    "90_getinpr.com.py",
    "91_dawbell.com.py",
    "92_motherartists.com_booking.py",
    "93_motherartists.com_mgmt.py",
    "94_insideout.agency.py",
    "95_republicrecords.com.py",
    "96_rcarecords.com.py",
    "97_onefiinix.com.py",
    "98_tmwrk.net.py",
    "99_crushmusic.com.py",
    "100_thenealagency.net.py",
    "101_hometown-talent.com.py",
    "102_anniversarygroup.com.py",
    "103_paladinartists.com.py",
    "104_lb-agency.net.py",
    "105_tap-music.com.py",
    "106_independentartistgroup.com.py",
    "107_nge-booking.com.py",
    "108_warmagency.com.py",
    "109_corsonagency.com.py",
    "110_paramountartists.com.py",
    "112_pure-represents.com.py",
    "115_curtisbrown.co.uk.py",
    "116_insanity.com.py",
    "117_analog-a.com.py",
    "118_makewake.net.py",
    "119_armige.com.py",
    "120_anna-agency.nl.py",
    "122_culturewave.la.py",
    "123_2bentertainment.net.py",
    "124_r-m.art.py",
    "127_intertalentgroup.com.py",
    "128_arcade-talent.com.py",
    "130_thebullittagency.com.py",
    "131_mushroombooking.com.py",
    "133_amodeagency.com.py",
    "136_t-s-agency.com.py",
    "140_panacherock.com.py",
    "142_thekurlandagency.com.py",

    "51_gersh.com.py",
    "53_thegreenroompr.com.py",
    "54_2911.us.py",
    "55_wecarealotpr.com.py",
    "56_nastylittleman.com.py",
    "137_kmgmt.com.py",
    "138_strangetalent.agency.py",
    "139_atcmanagement.com.py",
    "141_leadermgmt.com.py",
    "134_fatcatmusicgroup.com.py",
    "135_fatcatmusicgroup.com.py",
    "92_motherartists.com_booking.py",
    "93_motherartists.com_mgmt.py",
    "126_sequelmusicgroup.com.py",
    "125_clockworkartists.co.uk.py",
    "121_goodmachinepr.com.py",
    "111_mickmgmt.com.py",
    "113_ivpr.com.py",
    "114_unitedagents.co.uk.py",
    "52_utaspeakers.com.py"
]
import undetected_chromedriver as uc

driver = uc.Chrome()
driver.get('https://icons8.com/icons/set/clothing-store--style-office')
time.sleep(10)
print(driver.page_source)
sys.exit()

for script in scripts:
    full_path = os.path.join(os.path.dirname(__file__), script)
    print(f"\n🚀 Running {script}...\n")
    site_name = script.replace('.py', '')
    site_name = ''.join(site_name.split('_')[1:])
    try:
        result = subprocess.run(["python", full_path], check=True, capture_output=True, text=True)
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
    time.sleep(10)