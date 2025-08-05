import os
import datetime
import subprocess
from load_django import *
from parser_app.models import Status


scripts = [
    '7_groundcontroltouring.com.py',
    '12_primarytalent.com.py',
    '18_wmeagency.com.py',
    '20_pitchperfectpr.com.py',
    '32_sacksco.com.py',
    '34_mbcpr.com.py',
    '36_braceyourselfpr.com.py',
    '39_redlightmanagement.com.py',
    '43_dynamictalent.com.py',
    '130_thebullittagency.com.py',
    
]


for script in scripts:
    full_path = os.path.join(os.path.dirname(__file__), script)
    print(f"\n🚀 Running {script}...\n")
    site_name = script.replace('.py', '')
    site_name = ''.join(site_name.split('_')[1:])
    try:
        result = subprocess.run(["xvfb-run", "-a", "python3", full_path], check=True, capture_output=True, text=True)
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
