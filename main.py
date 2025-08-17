import os
import subprocess
import sys
import traceback
import colorama
from log import log
from pathlib import Path
import win32api
import win32event
import json

_ARDUINO_CLI_PATH = Path() / "bin" / "arduino-cli.exe"

_VERSION = "2.0.0"

_LOGO = """
 ██████╗██╗   ██╗███████╗███╗   ██╗███████╗██╗   ██╗
██╔════╝╚██╗ ██╔╝██╔════╝████╗  ██║██╔════╝╚██╗ ██╔╝
██║      ╚████╔╝ █████╗  ██╔██╗ ██║█████╗   ╚████╔╝ 
██║       ╚██╔╝  ██╔══╝  ██║╚██╗██║██╔══╝    ╚██╔╝  
╚██████╗   ██║   ██║     ██║ ╚████║███████╗   ██║   
 ╚═════╝   ╚═╝   ╚═╝     ╚═╝  ╚═══╝╚══════╝   ╚═╝ 
"""

_TITLE = f"""
Arduino ESP32 Core Installer
version: {_VERSION}
"""


def get_expected_version():
    log(colorama.Fore.YELLOW + colorama.Style.BRIGHT + "开始查询esp32:esp32版本号信息，请稍等")
    ret = subprocess.run(
        [_ARDUINO_CLI_PATH, "core", "search", "esp32:esp32", "-a", "--json"], check=True, shell=True, encoding="utf-8", capture_output=True
    )
    json_obj = json.loads(ret.stdout)
    log(colorama.Fore.YELLOW + "\033[1;33m所有esp32:esp32版本号:\033[0m")
    versions = set()
    for index, version in enumerate(json_obj["platforms"][0]["releases"].items(), start=1):
        versions.add(version[0])
        print(colorama.Fore.MAGENTA + colorama.Style.BRIGHT + f"{version[0]}".ljust(12), end="")
        if index % 4 == 0:
            print("")
        else:
            print("", end=" ")

    while True:
        version = input("\033[1;33m" "请输入需要安装的版本号（格式 X.Y.Z，例如：3.2.0，留空代表安装最新版）→ 按回车确认:\n" "\033[0m")
        version = version.strip()

        if version == "":
            return None
        elif version in versions:
            return version
        else:
            log(colorama.Fore.RED + colorama.Style.BRIGHT + f"输入的版本号 {version} 不存在，请重新输入：")


def install():
    log(f"workspace: {Path().absolute()}")

    log(f"arduino cli path: {_ARDUINO_CLI_PATH}")

    version = get_expected_version()
    if version is None:
        log(colorama.Fore.YELLOW + colorama.Style.BRIGHT + f"开始安装最新版esp32:esp32，请稍等")
    else:
        log(colorama.Fore.YELLOW + colorama.Style.BRIGHT + f"开始安装 esp32:esp32@{version}，请稍等")

    log("core esp32:esp32 uninstalling")
    subprocess.run([_ARDUINO_CLI_PATH, "core", "uninstall", "esp32:esp32"], check=False, shell=True)

    package_index_json_path = Path(os.getenv("LOCALAPPDATA")) / "Arduino15" / "package_index.json"
    log("removing package_index.json")
    package_index_json_path.unlink(missing_ok=True)

    # subprocess.run([_ARDUINO_CLI_PATH, "core", "search", "esp32:esp32"], check=True, shell=True)

    log("core list")
    subprocess.run([_ARDUINO_CLI_PATH, "core", "list"], check=True, shell=True)

    log("modifying package_index.json")
    with package_index_json_path.open("r+", encoding="utf-8") as f:
        content = f.read().replace("https://github.com/", "https://gh-proxy.com/https://github.com/")
        f.seek(0)
        f.write(content)

    if version is None:
        log("core esp32:esp32 installing")
        subprocess.run([_ARDUINO_CLI_PATH, "core", "install", "esp32:esp32"], check=True, shell=True)
    else:
        log(f"core esp32:esp32 {version} installing")
        subprocess.run([_ARDUINO_CLI_PATH, "core", "install", f"esp32:esp32@{version}"], check=True, shell=True)

    log("core list")
    subprocess.run([_ARDUINO_CLI_PATH, "core", "list"], check=True, shell=True)

    log("core esp32:esp32 install completed")


try:
    colorama.init(autoreset=True)
    print(colorama.Fore.CYAN + colorama.Style.BRIGHT + _LOGO)
    print(colorama.Fore.YELLOW + colorama.Style.BRIGHT + _TITLE)
    log(f"platform: {sys.platform}")
    if not sys.platform.startswith("win32"):
        raise Exception(f"不支持当前操作系统: {sys.platform}")
    mutex = win32event.CreateMutex(None, False, "cyfney_arduino_esp32_core_installer")
    if win32api.GetLastError() == 183:
        raise RuntimeError("检测到程序已在运行，请关闭其他实例后重试")
    install()
    log(colorama.Fore.GREEN + colorama.Style.BRIGHT + "安装成功")
except Exception:
    log(colorama.Fore.RED + traceback.format_exc())
    log(colorama.Fore.RED + colorama.Style.BRIGHT + "安装失败")

log(colorama.Fore.YELLOW + colorama.Style.BRIGHT + "请输入任意按键关闭窗口")
input()
