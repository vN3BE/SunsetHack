#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from utils import clear, print_banner, gradient_print, gradient_input

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

def dns_lookup_interactive():
    clear()
    print_banner()
    if not DNS_AVAILABLE:
        gradient_print(" [Error] dnspython library not installed.", 0.03)
        gradient_print(" Install: pip install dnspython", 0.03)
        gradient_input("\n Press Enter...")
        return
    domain = gradient_input(" Enter domain (e.g. google.com) → ").strip()
    if not domain:
        gradient_print(" Domain not entered.", 0.03)
        time.sleep(1)
        return
    gradient_print(f"\n Querying DNS for {domain}...", 0.04)
    time.sleep(0.5)
    records = {}
    for rtype in ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME']:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            if rtype == 'MX':
                records[rtype] = [f"{r.preference} {r.exchange}" for r in answers]
            elif rtype == 'TXT':
                records[rtype] = [''.join(r.strings) if r.strings else '' for r in answers]
            else:
                records[rtype] = [str(r) for r in answers]
        except:
            records[rtype] = []
    has_data = any(records.values())
    if not has_data:
        gradient_print(" [Error] Could not retrieve DNS records for this domain.", 0.03)
    else:
        for rtype, values in records.items():
            if values:
                gradient_print(f" [Record {rtype}]", 0.02)
                for val in values:
                    gradient_print(f"   {val}", 0.02)
                time.sleep(0.1)
    print()
    gradient_input(" Press Enter to return to menu...")