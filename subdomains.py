#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import socket
import time
from utils import clear, print_banner, gradient_print, gradient_input

COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk",
    "ns2", "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap", "test",
    "ns", "blog", "pop3", "dev", "www2", "admin", "forum", "news", "vpn", "ns3",
    "mail2", "new", "mysql", "old", "lists", "support", "mobile", "mx", "static",
    "docs", "beta", "shop", "sql", "secure", "demo", "cp", "calendar", "wiki",
    "web", "media", "email", "images", "img", "download", "dns", "piwik", "stats",
    "dashboard", "portal", "manage", "start", "info", "apps", "video", "sip",
    "dns2", "api", "cdn", "mssql", "remote", "server", "ftp2", "stage", "vps"
]

def get_subdomains_crtsh(domain):
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            subdomains = set()
            for entry in data:
                name = entry.get('name_value', '')
                for part in name.split('\n'):
                    part = part.strip().lower()
                    if part.endswith(domain):
                        subdomains.add(part)
            return sorted(subdomains)
        else:
            return []
    except Exception:
        return []

def brute_force_subdomains(domain):
    found = []
    for sub in COMMON_SUBDOMAINS:
        test_domain = f"{sub}.{domain}"
        try:
            socket.gethostbyname(test_domain)
            found.append(test_domain)
        except socket.gaierror:
            pass
    return found

def subdomains_interactive():
    clear()
    print_banner()
    gradient_print(" === Subdomain scanner (crt.sh + dns brute) ===", 0.03)
    domain = gradient_input(" Enter domain (e.g. google.com): ").strip().lower()
    if not domain:
        gradient_print(" Domain not entered.", 0.03)
        time.sleep(1)
        return
    gradient_print(f"\n Collecting subdomains for {domain}...", 0.04)
    time.sleep(0.5)
    from_crt = get_subdomains_crtsh(domain)
    if from_crt:
        gradient_print(f" [crt.sh] Found {len(from_crt)} subdomains", 0.025)
    else:
        gradient_print(" [crt.sh] None or error", 0.025)
    from_brute = brute_force_subdomains(domain)
    if from_brute:
        gradient_print(f" [DNS brute] Found {len(from_brute)} subdomains", 0.025)
    all_subs = sorted(set(from_crt + from_brute))
    if not all_subs:
        gradient_print("\n No subdomains found.", 0.03)
    else:
        gradient_print(f"\n Total found: {len(all_subs)}", 0.025)
        for sub in all_subs:
            gradient_print(f"   • {sub}", 0.02)
            time.sleep(0.02)
    print()
    gradient_input(" Press Enter to return to menu...")