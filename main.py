import os
import subprocess
import sys
import traceback
import colorama
from log import log
from pathlib import Path
import win32api
import win32event


def install():
    log(f"workspace: {Path().absolute()}")

    arduino_cli_path = Path() / "bin" / "arduino-cli.exe"

    log(f"arduino cli path: {arduino_cli_path}")

    log("core esp32:esp32 uninstalling")
    subprocess.run([arduino_cli_path, "core", "uninstall", "esp32:esp32"], check=False, shell=True)

    package_index_json_path = Path(os.getenv("LOCALAPPDATA")) / "Arduino15" / "package_index.json"
    log("removing package_index.json")
    package_index_json_path.unlink(missing_ok=True)

    subprocess.run([arduino_cli_path, "core", "search", "esp32:esp32"], check=True, shell=True)

    log("core list")
    subprocess.run([arduino_cli_path, "core", "list"], check=True, shell=True)

    log("modifying package_index.json")
    with package_index_json_path.open("r+", encoding="utf-8") as f:
        content = f.read().replace("https://github.com/", "https://gh-proxy.com/https://github.com/")
        f.seek(0)
        f.write(content)

    log("core esp32:esp32 installing")
    subprocess.run([arduino_cli_path, "core", "install", "esp32:esp32"], check=True, shell=True)

    log("core list")
    subprocess.run([arduino_cli_path, "core", "list"], check=True, shell=True)

    log("core esp32:esp32 install completed")


VERSION = "1.1.0"

LOGO = """
 ██████╗██╗   ██╗███████╗███╗   ██╗███████╗██╗   ██╗
██╔════╝╚██╗ ██╔╝██╔════╝████╗  ██║██╔════╝╚██╗ ██╔╝
██║      ╚████╔╝ █████╗  ██╔██╗ ██║█████╗   ╚████╔╝ 
██║       ╚██╔╝  ██╔══╝  ██║╚██╗██║██╔══╝    ╚██╔╝  
╚██████╗   ██║   ██║     ██║ ╚████║███████╗   ██║   
 ╚═════╝   ╚═╝   ╚═╝     ╚═╝  ╚═══╝╚══════╝   ╚═╝ 
"""

TITLE = f"""
Arduino ESP32 Core Installer
version: {VERSION}
"""

try:

    colorama.init(autoreset=True)
    print(colorama.Fore.CYAN + LOGO)
    print(colorama.Fore.YELLOW + TITLE)
    log(f"platform: {sys.platform}")
    if not sys.platform.startswith("win32"):
        raise Exception(f"unsupport platform: {sys.platform}")
    mutex = win32event.CreateMutex(None, False, "cyfney_arduino_esp32_core_installer")
    if win32api.GetLastError() == 183:
        raise RuntimeError("检测到程序已在运行，请关闭其他实例后重试")
    install()
    log(colorama.Fore.GREEN + "Installation succeeded")
except Exception:
    log(colorama.Fore.RED + traceback.format_exc())
    log(colorama.Fore.RED + "Installation failed")

log(colorama.Fore.YELLOW + "Press any key to close the window")
input()
