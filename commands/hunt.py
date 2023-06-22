import requests
import sys
import json
from mods import mods 
from mods import keyring

apiKey = keyring.key_virustotal
# API key
vt_api = f"{apiKey}"

command = "/vthunt"
use = "Virus Total Hunt"

art = mods.vthuntArt

def run():
    main()

def main():
    print(art)
    print("Navi> Here are the current options for VTHunt:")
    print("1. Virus Total Hash Seach")
    print("2. Virus Total IP Search")
    print("3. Virus Total Domain Search")

    option = input("\nNavi> Please select an option(ex: hash,ip,domain)\n=> ").lower()

    if option == "hash":
        ioc = input("Navi> What hash do you want to search\n=> ")
        VT_Hash(ioc)
    elif option == "ip":
        ioc = input("Navi> What IP do you want to search\n=> ")
        VT_IP(ioc)
    elif option == "domain":
        ioc = input("Navi> What domain do you want to search\n=> ")
        VT_Domain(ioc)
    else:
        print("Navi> [!] - Please select a valid option")

# Virus Total hash check
def VT_Hash(ioc):
    url = "https://www.virustotal.com/api/v3/files/" + ioc

    headers = {
        "accept": "application/json",
        "x-apikey": vt_api
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()  # Parse response as JSON

    last_analysis_stats = response_json["data"]["attributes"]["last_analysis_stats"]
    permalink = response_json["data"]["links"]["self"]
    output = {
        "last_analysis_stats": last_analysis_stats,
        "permalink": permalink
    }
    print(json.dumps(output, indent=4))  # Print formatted JSON

# Virus Total IP check
def VT_IP(ioc):
    url = "https://www.virustotal.com/api/v3/ip_addresses/" + ioc

    headers = {
        "accept": "application/json",
        "x-apikey": vt_api
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()  # Parse response as JSON

    last_analysis_stats = response_json["data"]["attributes"]["last_analysis_stats"]
    permalink = response_json["data"]["links"]["self"]
    output = {
        "last_analysis_stats": last_analysis_stats,
        "permalink": permalink
    }
    print(json.dumps(output, indent=4))  # Print formatted JSON

# Virus Total Domain check
def VT_Domain(ioc):
    url = "https://www.virustotal.com/api/v3/domains/" + ioc

    headers = {
        "accept": "application/json",
        "x-apikey": vt_api
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()  # Parse response as JSON

    last_analysis_stats = response_json["data"]["attributes"]["last_analysis_stats"]
    permalink = response_json["data"]["links"]["self"]
    output = {
        "last_analysis_stats": last_analysis_stats,
        "permalink": permalink
    }
    print(json.dumps(output, indent=4))  # Print formatted JSON
