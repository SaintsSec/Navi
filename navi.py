import re


def get_ip_address(input_str):
    if re.match(r'(\d{1,3}\.){3}\d{1,3}', input_str):
        return input_str
    else:
        return None


def get_hostname(input_str):
    if re.match(r'[a-zA-Z0-9\-]+\.[a-zA-Z]{2,3}', input_str):
        return input_str
    else:
        return None
