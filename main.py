#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import sys
from utils import clear, print_banner, gradient_print, gradient_input
from botnet import stop_all_bots

# Import all modules (filenames stay English)
from scanner import scan_server_interactive
from uuid_lookup import uuid_interactive
from botnet import start_botnet
from ipinfo import ipinfo_interactive
from iphistory import iphistory_interactive
from dnslookup import dns_lookup_interactive
from checker import check_accounts_interactive
from resolver import resolver_interactive
from seeker import seeker_interactive
from websearch import websearch_interactive
from subdomains import subdomains_interactive
from port_scanner import port_scanner_interactive
from listening import listening_interactive
from proxy import proxy_interactive
from fakeproxy import fakeproxy_interactive
from connect import connect_interactive
from sendcmd import sendcmd_interactive
from rcon import rcon_interactive
from brutercon import brutercon_interactive
from bruteauth import bruteauth_interactive
from kick import kick_interactive
from kickall import kickall_interactive

def auth():
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        clear()
        print_banner()
        if attempt > 1:
            gradient_print(f" Invalid login or password. Attempt {attempt} of {max_attempts}", 0.03)
            print()
        login = gradient_input(" Login: ")
        password = gradient_input(" Password: ")
        if login == "123" and password == "123":
            gradient_print("\n Login successful! Welcome.", 0.03)
            time.sleep(1)
            return True
    clear()
    print_banner()
    gradient_print("\n Access denied. Too many failed attempts.", 0.03)
    return False

def print_menu():
    # Categories
    server_items = [
        ("1", "Server Scan"),
        ("2", "Get UUID by nickname"),
        ("3", "Botnet (spawn bots)"),
        ("4", "Domain -> IP resolve"),
        ("5", "Connect bot (no commands)"),
        ("6", "Send commands from file"),
        ("7", "RCON connection"),
        ("8", "Brute-force RCON"),
        ("9", "Brute-force /login"),
        ("10", "Empty"),
        ("11", "Empty")
    ]
    network_items = [
        ("12", "IP geolocation"),
        ("13", "IP history (reverse IP)"),
        ("14", "DNS lookup"),
        ("15", "Listening check (TCP)"),
        ("16", "Proxy tester"),
        ("17", "FakeProxy (Velocity)"),
        ("18", "Port scanner"),
        ("19", "Subdomain scanner"),
        ("20", "WebSearch (monitoring sites)")
    ]
    utils_items = [
        ("21", "Account checker (email:pass)"),
        ("22", "Seeker (Discord bot token)"),
        ("0", "Exit")
    ]
    
    # Column headers
    col_headers = ["SERVER", "NETWORK", "UTILS"]
    
    # Format items as "[number] text"
    def format_items(items):
        return [f"[{num}] {text}" for num, text in items]
    
    col1 = format_items(server_items)
    col2 = format_items(network_items)
    col3 = format_items(utils_items)
    
    # Compute max width per column (including header)
    max_width = max(
        max((len(line) for line in col1), default=0),
        max((len(line) for line in col2), default=0),
        max((len(line) for line in col3), default=0),
        len(col_headers[0]), len(col_headers[1]), len(col_headers[2])
    ) + 2
    
    # Print headers
    header_line = f"{col_headers[0]:<{max_width}}{col_headers[1]:<{max_width}}{col_headers[2]}"
    gradient_print(f" {header_line}", 0.02)
    gradient_print("", 0.01)  # empty line separator
    
    max_rows = max(len(col1), len(col2), len(col3))
    for i in range(max_rows):
        line = ""
        if i < len(col1):
            line += f"{col1[i]:<{max_width}}"
        else:
            line += " " * max_width
        if i < len(col2):
            line += f"{col2[i]:<{max_width}}"
        else:
            line += " " * max_width
        if i < len(col3):
            line += col3[i]
        gradient_print(f" {line.rstrip()}", 0.02)

def main():
    while True:
        clear()
        print_banner()
        gradient_print(" Welcome to SunsetHack! Read readme.txt to learn about the functions", 0.04)
        print()
        print_menu()
        print()
        choice = gradient_input(" Choose an option → ")

        if choice == "0":
            stop_all_bots()
            clear()
            print_banner()
            gradient_print(" Goodbye!", 0.03)
            time.sleep(1)
            break
        elif choice == "1":
            scan_server_interactive()
        elif choice == "2":
            uuid_interactive()
        elif choice == "3":
            start_botnet()
        elif choice == "4":
            resolver_interactive()
        elif choice == "5":
            connect_interactive()
        elif choice == "6":
            sendcmd_interactive()
        elif choice == "7":
            rcon_interactive()
        elif choice == "8":
            brutercon_interactive()
        elif choice == "9":
            bruteauth_interactive()
        elif choice == "10":
            gradient_print("Not work")
        elif choice == "11":
            gradient_print("Not work")
        elif choice == "12":
            ipinfo_interactive()
        elif choice == "13":
            iphistory_interactive()
        elif choice == "14":
            dns_lookup_interactive()
        elif choice == "15":
            listening_interactive()
        elif choice == "16":
            proxy_interactive()
        elif choice == "17":
            fakeproxy_interactive()
        elif choice == "18":
            port_scanner_interactive()
        elif choice == "19":
            subdomains_interactive()
        elif choice == "20":
            websearch_interactive()
        elif choice == "21":
            check_accounts_interactive()
        elif choice == "22":
            seeker_interactive()
        else:
            clear()
            print_banner()
            gradient_print(" Invalid choice. Try again.", 0.03)
            time.sleep(1.5)

if __name__ == "__main__":
    try:
        if auth():
            main()
        else:
            time.sleep(2)
    except KeyboardInterrupt:
        stop_all_bots()
        print("\n\n\033[91mProgram terminated.\033[0m")