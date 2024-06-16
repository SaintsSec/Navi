#!/bin/python3
import subprocess, os, platform, psutil, requests, socket, cryptography
from datetime import datetime
from typing import List
from navi_shell import tr, get_ai_name, llm_chat, get_user
from navi import get_ip_address, get_hostname, get_parameters, get_command_path

# Navi Command System Variables
command = "GetSys"
use = "Prints out system information"
aliases = ['sysinfo', 'sys']

#global variables 
get_ai_name = "Navi> "
get_user = "Alex"
breakline = "======="

def get_system_info():
    return {
        'Platform': platform.system(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor()
    }

def get_memory_info():
    memory = psutil.virtual_memory()
    return {
        'Total Memory': f"{memory.total / (1024 * 1024)} MB",
        'Available Memory': f"{memory.available / (1024 * 1024)} MB"
    }

def get_disk_info():
    disk = psutil.disk_usage('/')
    return {
        'Total Disk Space': f"{disk.total / (1024 * 1024 * 1024)} GB",
        'Used Disk Space': f"{disk.used / (1024 * 1024 * 1024)} GB",
        'Free Disk Space': f"{disk.free / (1024 * 1024 * 1024)} GB"
    }

def get_uptime_info():
    boot_time = psutil.boot_time()
    uptime = datetime.now() - datetime.fromtimestamp(boot_time)
    return {
        'Uptime': str(uptime).split('.')[0]
    }

def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text.strip()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 0))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip 



def run(arguments=None):
    #setup variables
    public_ip = get_public_ip()
    local_ip = get_local_ip()
    system_info = get_system_info()
    memory_info = get_memory_info()
    disk_info = get_disk_info()
    uptime_info = get_uptime_info()
    
    #Main functions
    response_message = llm_chat("Give me a really simple quip about getting my systems specs. Dont include commands or references to operating systems.")
    clean_text = str(response_message).replace("(", "").replace(")", "").replace(", 200", "").replace("\"", "").replace("\\n", "")
    tr(f"{get_ai_name} {clean_text}")

    print(breakline)
    tr(f"{get_ai_name} System Information:\n")
    for key, value in system_info.items():
        tr(f"{key}: {value}")

    print(breakline)    
    tr(f"{get_ai_name} Memory Information:\n")
    for key, value in memory_info.items():
        tr(f"{key}: {value}")
    
    print(breakline)
    tr(f"{get_ai_name} Disk Space Information:\n")
    for key, value in disk_info.items():
        tr(f"{key}: {value}")

    print(breakline)
    tr(f"{get_ai_name} Uptime Information:\n")
    for key, value in uptime_info.items():
        tr(f"{key}: {value}")

    print(breakline)
    tr(f"{get_ai_name} Network Information: \n")
    tr(f"Your local ip is: {local_ip}")
    tr(f"Your public ip is: redacted -- Nice try")
    print(breakline)
