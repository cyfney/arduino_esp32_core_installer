import subprocess
import os
import shutil
import zipfile

subprocess.run(
    [
        "pyinstaller.exe",
        "-F",
        "main.py",
        "--distpath",
        "./build",
        "-n",
        "arduino_esp32_core_installer",
    ],
    check=True,
    shell=True,
)


if os.path.exists(os.path.join("docs", "html")):
    shutil.rmtree(os.path.join("docs", "html"))

subprocess.run(
    ["doxygen", "./doxygen_config/project.cfg"],
    check=True,
    shell=True,
)

if not os.path.exists(os.path.join("docs", "resource")):
    os.makedirs(os.path.join("docs", "resource"))

with zipfile.ZipFile(
    os.path.join("docs", "resource", "arduino_esp32_core_installer.zip"),
    "w",
    zipfile.ZIP_DEFLATED,
) as zip_file:
    zip_file.write(
        os.path.join("build", "arduino_esp32_core_installer.exe"),
        arcname="arduino_esp32_core_installer.exe",
    )
    zip_file.write(
        os.path.join("bin", "arduino-cli.exe"),
        arcname="bin/arduino-cli.exe",
    )
