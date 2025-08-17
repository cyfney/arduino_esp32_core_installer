import subprocess

subprocess.run(["pyinstaller.exe", "-F", "main.py", "--distpath", ".", "-n", "arduino_esp32_core_installer"], check=True, shell=True)
