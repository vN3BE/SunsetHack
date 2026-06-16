#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import requests
from utils import clear, print_banner, gradient_print, gradient_input

def get_ip_info(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,continent,continentCode,country,countryCode,region,regionName,city,timezone,isp,org"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data.get('status') == 'success':
            return {
                'success': True,
                'continent': f"{data.get('continent', 'Unknown')} ({data.get('continentCode', '?')})",
                'country': f"{data.get('country', 'Unknown')} ({data.get('countryCode', '?')})",
                'region': f"{data.get('regionName', 'Unknown')} ({data.get('region', '?')})",
                'city': data.get('city', 'Unknown'),
                'timezone': data.get('timezone', 'Unknown'),
                'isp': data.get('isp', 'Unknown'),
                'org': data.get('org', 'Unknown')
            }
        else:
            return {'success': False, 'error': f"Failed: {data.get('message', 'unknown error')}"}
    except Exception as e:
        return {'success': False, 'error': f"Connection error: {e}"}

def ipinfo_interactive():
    clear()
    print_banner()
    ip = gradient_input(" Enter IP address → ").strip()
    if not ip:
        gradient_print(" IP not entered.", 0.03)
        time.sleep(1)
        return
    gradient_print(f"\n Fetching data for {ip}...", 0.04)
    time.sleep(0.5)
    res = get_ip_info(ip)
    if not res['success']:
        gradient_print(f" [Error] {res['error']}", 0.03)
    else:
        lines = [
            f" [Continent] {res['continent']}",
            f" [Country] {res['country']}",
            f" [Region] {res['region']}",
            f" [City] {res['city']}",
            f" [Timezone] {res['timezone']}",
            f" [ISP] {res['isp']}",
            f" [Organization] {res['org']}"
        ]
        for line in lines:
            gradient_print(line, 0.025)
            time.sleep(0.1)
    print()
    gradient_input(" Press Enter to return to menu...")