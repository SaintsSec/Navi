import requests
from mods import mods
from mods import keyring

apiKey = keyring.key_virustotal
command = "/vthunt"
use = "Virus Total Search"
def run():
    main()

def main():
    art = mods.vthuntArt
    print(art)
    print("Navi> Here are the current options for VTHunt:")
    print("1. Virus Total Hash Search")
    print("2. Virus Total IP Search")
    print("3. Virus Total Domain Search")

    option = input("\nNavi> Please select an option (ex: hash, ip, domain)\n=> ").lower()

    if option == "hash":
        ioc = input("Navi> What hash do you want to search?\n=> ")
        VT_Hash(ioc)
    elif option == "ip":
        ioc = input("Navi> What IP do you want to search?\n=> ")
        VT_IP(ioc)
    elif option == "domain":
        ioc = input("Navi> What domain do you want to search?\n=> ")
        VT_Domain(ioc)
    else:
        print("Navi> [!] - Please select a valid option")

# Virus Total hash check
def VT_Hash(ioc):
    url = f"https://www.virustotal.com/api/v3/files/{ioc}"
    headers = {
        "accept": "application/json",
        "x-apikey": apiKey
    }
    response = requests.get(url, headers=headers)
    response_json = response.json()

    last_analysis_stats = response_json["data"]["attributes"]["last_analysis_stats"]
    permalink = response_json["data"]["links"]["self"]

    print("Last Analysis Stats:")
    for key, value in last_analysis_stats.items():
        print(f"{key}: {value}")

    print("Permalink:", permalink)

# Virus Total IP check
def VT_IP(ioc):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ioc}"
    headers = {
        "accept": "application/json",
        "x-apikey": apiKey
    }
    response = requests.get(url, headers=headers)
    response_json = response.json()

    last_analysis_stats = response_json["data"]["attributes"]["last_analysis_stats"]
    permalink = response_json["data"]["links"]["self"]

    print("Last Analysis Stats:")
    for key, value in last_analysis_stats.items():
        print(f"{key}: {value}")

    print("Permalink:", permalink)

# Virus Total Domain check
def VT_Domain(ioc):
    url = f"https://www.virustotal.com/api/v3/domains/{ioc}"
    headers = {
        "accept": "application/json",
        "x-apikey": apiKey
    }
    response = requests.get(url, headers=headers)
    response_json = response.json()

    last_analysis_stats = response_json["data"]["attributes"]["last_analysis_stats"]
    permalink = response_json["data"]["links"]["self"]

    print("Last Analysis Stats:")
    for key, value in last_analysis_stats.items():
        print(f"{key}: {value}")

    print("Permalink:", permalink)

