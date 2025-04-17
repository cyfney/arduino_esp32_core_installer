import os
import subprocess
import sys
import traceback
import colorama
from log import log

version = "1.0.1"


def install():

    if getattr(sys, "frozen", False):
        workspace = os.path.dirname(sys.executable)
    else:
        workspace = os.path.dirname(os.path.abspath(__file__))

    log(f"workspace: {workspace}")

    arduino_cli_path = os.path.join(workspace, "bin", "arduino-cli.exe")

    log(f"arduino cli path: {arduino_cli_path}")

    log("core esp32:esp32 uninstalling")
    subprocess.run(
        [arduino_cli_path, "core", "uninstall", "esp32:esp32"], check=False, shell=True
    )

    package_index_json_path = os.path.join(
        os.getenv("LOCALAPPDATA"), "Arduino15", "package_index.json"
    )

    if os.path.exists(package_index_json_path):
        log("removing package_index.json")
        os.remove(package_index_json_path)

    log("core list")
    subprocess.run([arduino_cli_path, "core", "list"], check=True, shell=True)

    log("modifying package_index.json")
    with open(
        package_index_json_path,
        "r",
        encoding="utf-8",
    ) as f:
        replaced_data = f.read().replace("https://github.com/", "https://bgithub.xyz/")

    with open(
        package_index_json_path,
        "w",
        encoding="utf-8",
    ) as f:
        f.write(replaced_data)

    log("core esp32:esp32 installing")
    subprocess.run(
        [arduino_cli_path, "core", "install", "esp32:esp32"], check=True, shell=True
    )

    log("core list")
    subprocess.run([arduino_cli_path, "core", "list"], check=True, shell=True)

    log("core esp32:esp32 install completed")


logo = """
 ██████╗██╗   ██╗███████╗███╗   ██╗███████╗██╗   ██╗
██╔════╝╚██╗ ██╔╝██╔════╝████╗  ██║██╔════╝╚██╗ ██╔╝
██║      ╚████╔╝ █████╗  ██╔██╗ ██║█████╗   ╚████╔╝ 
██║       ╚██╔╝  ██╔══╝  ██║╚██╗██║██╔══╝    ╚██╔╝  
╚██████╗   ██║   ██║     ██║ ╚████║███████╗   ██║   
 ╚═════╝   ╚═╝   ╚═╝     ╚═╝  ╚═══╝╚══════╝   ╚═╝ 
"""

title = f"""
Arduino ESP32 Core Installer
version: {version}
"""

try:

    colorama.init(autoreset=True)
    print(colorama.Fore.CYAN + logo)
    print(colorama.Fore.YELLOW + title)
    log(f"platform: {sys.platform}")
    if not sys.platform.startswith("win32"):
        raise Exception(f"unsupport platform: {sys.platform}")
    install()
    log(colorama.Fore.GREEN + "Installation succeeded")
except Exception:
    log(colorama.Fore.RED + traceback.format_exc())
    log(colorama.Fore.RED + "Installation failed")

log(colorama.Fore.YELLOW + "Press any key to close the window")
input()
