#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import requests
from utils import clear, print_banner, gradient_print, gradient_input

def get_ip_history(domain):
    try:
        url = f"https://api.hackertarget.com/reverseiplookup/?q={domain}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.text.strip()
            if data.startswith("error") or "not found" in data.lower():
                return {'success': False, 'error': data}
            ips = [line.strip() for line in data.split('\n') if line.strip()]
            if not ips:
                return {'success': False, 'error': "No IP addresses found"}
            return {'success': True, 'ips': ips, 'count': len(ips)}
        else:
            return {'success': False, 'error': f"HTTP error {resp.status_code}"}
    except Exception as e:
        return {'success': False, 'error': f"Error: {e}"}

def iphistory_interactive():
    clear()
    print_banner()
    domain = gradient_input(" Enter domain (e.g. google.com) → ").strip()
    if not domain:
        gradient_print(" Domain not entered.", 0.03)
        time.sleep(1)
        return
    gradient_print(f"\n Searching IP addresses for {domain}...", 0.04)
    time.sleep(0.5)
    res = get_ip_history(domain)
    if not res['success']:
        gradient_print(f" [Error] {res['error']}", 0.03)
    else:
        gradient_print(f" [Domain] {domain}", 0.025)
        gradient_print(f" [Found IPs] {res['count']}", 0.025)
        gradient_print(" [IP list]:", 0.025)
        for ip in res['ips']:
            gradient_print(f"   • {ip}", 0.02)
            time.sleep(0.05)
    print()
    gradient_input(" Press Enter to return to menu...")