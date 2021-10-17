import configparser
import datetime
import requests
import re


config = configparser.ConfigParser()

config.read("config.ini")

REBOOT_PAGE_URL = config["ROUTER"]["REBOOT_PAGE_URL"]
REBOOT_ENDPOINT_URL = config["ROUTER"]["REBOOT_ENDPOINT_URL"]
USER = config["ROUTER"]["USER"]
PASSWORD = config["ROUTER"]["PASSWORD"]
SESSION_KEY_REGEX = config["ROUTER"]["SESSION_KEY_REGEX"]


reboot_page = requests.get(REBOOT_PAGE_URL, auth=(USER, PASSWORD))
if reboot_page.status_code != 200:
    raise Exception("router reboot failed, router returned status code other than 200")

try:
    session_key = re.search(SESSION_KEY_REGEX, reboot_page.text).group(1)
except AttributeError:
    print("failed to find the session key in the router response")
    exit(1)

reboot_url = REBOOT_ENDPOINT_URL + session_key

reboot_endpoint = requests.get(reboot_url, auth=(USER, PASSWORD))
if reboot_endpoint.status_code != 200:
    raise Exception(
        "router reboot failed, reboot endpoint returned status code other than 200"
    )

print(f"Router reset successful at {datetime.datetime.now()}")
