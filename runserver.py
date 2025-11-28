import os
import subprocess

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "talentstar_backend.settings")
subprocess.run(["python", "manage.py", "runserver", "0.0.0.0:8000"])
