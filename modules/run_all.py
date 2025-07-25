import os
import datetime
import subprocess
from load_django import *
from parser_app.models import Status


scripts = [
    "33andwest.com.py",
    "spinartistagency.com.py",
    "mbartists.co.uk.py",
    "teamwass.com.py",
    "tbaagency.com.py",
    "unitedtalent.com.py",
    "wmeagency.com.py",
    "primarytalent.com.py",
    "highroadtouring.com.py",
    "caa.com.py",
    "august.agency.py",
    "prensadanna.com.py",
    "chameleon.unitedtalent.com.py",
    "billions.com.py",
    "itb.co.uk.py",
    "groundcontroltouring.com.py",
    "xraytouring.com.py",
    "atc-live.com.py",
    "soundtalentgroup.com.py",
    "soundtalentgroup.com.py"
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