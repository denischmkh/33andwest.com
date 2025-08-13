import os
import datetime
import re
import subprocess
import sys
import time

from load_django import *
from parser_app.models import Status

from _1_33andwest_com import parse1
from _2_atc_live_com import parse2
from _6_chameleon_unitedtalent_com import parse6
from _8_highroadtouring_com import parse8
from _9_itb_co_uk import parse9
from _10_mbartists_co_uk import parse10
from _11_prensadanna_com import parse11
from _13_soundtalentgroup_com import parse13
from _14_spinartistagency_com import parse14
from _15_tbaagency_com import parse15
from _18_wmeagency_com import parse18
from _20_pitchperfectpr_com import parse20
from _21_pitchandsmith_com import parse21
from _22_talentxent_com import parse22
from _26_audibletreats_com import parse26
from _27_bighassle_com import parse27
from _29_tellallyourfriendspr_com import parse29
from _30_biz3_net import parse30
from _31_orienteer_us import parse31
from _33_murraychalmers_com import parse33
from _35_chuffmedia_com import parse35
from _37_tkoco_com import parse37
from _38_rocnation_com import parse38
from _41_atomsplitterpr_com import parse41
from _42_sropr_com import parse42
from _44_13artists_com import parse44
from _45_satellite414_com import parse45
from _46_continentaltouring_us import parse46
from _47_freetradeagency_co_uk import parse47
from _48_girlieaction_com import parse48
from _49_publiccitypr_com import parse49
from _54_2911_us import parse54
from _55_wecarealotpr_com import parse55
from _60_ebmediapr_com import parse60
from _61_7smgmt_com import parse61
from _63_qprime_com import parse63
from _66_imran_malik_com import parse66
from _68_ayita_com import parse68
from _72_sheltermusic_com import parse72
from _73_4ad_com import parse73
from _74_minttalentgroup_com import parse74
from _77_chromaticpr_com import parse77
from _80_asgard_uk_com import parse80
from _81_concertedefforts_com import parse81
from _82_tbaagency_com import parse82
from _88_outermostagency_com import parse88
from _90_getinpr_com import parse90
from _91_dawbell_com import parse91
from _92_motherartists_com_booking import parse92
from _93_motherartists_com_mgmt import parse93
from _95_republicrecords_com import parse95
from _96_rcarecords_com import parse96
from _97_onefiinix_com import parse97
from _98_tmwrk_net import parse98
from _99_crushmusic_com import parse99
from _100_thenealagency_net import parse100
from _101_hometown_talent_com import parse101
from _102_anniversarygroup_com import parse102
from _103_paladinartists_com import parse103
from _106_independentartistgroup_com import parse106
from _107_nge_booking_com import parse107
from _108_warmagency_com import parse108
from _118_makewake_net import parse118
from _119_armige_com import parse119
from _120_anna_agency_nl import parse120
from _123_2bentertainment_net import parse123
from _140_panacherock_com import parse140
from _142_thekurlandagency_com import parse142

scripts = [
    parse1, parse2, parse6, parse8,
    parse9, parse10,
    parse11, parse13,
    parse14,
    parse15,
    parse18,
    parse20,
    parse21,
    parse22,
    parse26,
    parse27,
    parse29,
    parse30,
    parse31,
    parse33,
    parse35,
    parse37,
    parse38,
    parse41,
    parse42,
    parse44,
    parse45,
    parse46,
    parse47,
    parse48,
    parse49,
    parse54,
    parse55,
    parse60,
    parse61,
    parse63,
    parse66,
    parse68,
    parse72,
    parse73,
    parse74,
    parse77,
    parse80,
    parse81,
    parse82,
    parse88,
    parse90,
    parse91,
    parse92,
    parse93,
    parse95,
    parse96,
    parse97,
    parse98,
    parse99,
    parse100,
    parse101,
    parse102,
    parse103,
    parse106,
    parse107,
    parse108,
    parse118,
    parse119,
    parse120,
    parse123,
    parse140,
    parse142
]


# for script in scripts:
#     full_path = os.path.join(os.path.dirname(__file__), script)
#     print(f"\n🚀 Running {script}...\n")
#     site_name = script.replace('.py', '')
#     site_name = ''.join(site_name.split('_')[1:])
#     try:
#         result = subprocess.run(["python3", full_path], check=True, capture_output=True, text=True)
#         print(result.stdout)
#         Status.objects.update_or_create(
#             site=site_name,
#             defaults={
#                 'status': 'OK',
#                 'date': datetime.date.today()
#             }
#         )
#     except subprocess.CalledProcessError as e:
#         print(f"❌ Error running {script}:")
#         print("stdout:\n", e.stdout)
#         print("stderr:\n", e.stderr)
#         Status.objects.update_or_create(
#             site=site_name,
#             defaults={
#                 'status': 'Error',
#                 'date': datetime.date.today()
#             }
#         )
#     except Exception as e:
#         print(f"❌ Unexpected error in {script}: {e}")
#         Status.objects.update_or_create(
#             site=site_name,
#             defaults={
#                 'status': 'Error',
#                 'date': datetime.date.today()
#             }
#         )
#     time.sleep(1)

def extract_domain(module_name: str) -> str:
    name = re.sub(r"^_\d+_", "", module_name)
    domain = name.replace("_", ".")
    return domain


for script in scripts:
    print(f"Function {script.__name__} {script.__module__} has started")
    site_name = extract_domain(script.__module__)
    try:
        artists_found, new, deleted = script()
        Status.objects.update_or_create(
            site=site_name,
            defaults={
                'status': 'OK',
                "scraped": artists_found,
                "new": new,
                'deleted': deleted,
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
