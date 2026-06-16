#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import threading
import subprocess
from utils import clear, print_banner, gradient_print, gradient_input

bot_processes = []
bot_lock = threading.Lock()

def stop_all_bots():
    global bot_processes
    with bot_lock:
        for p in bot_processes:
            if p.poll() is None:
                p.terminate()
        time.sleep(0.5)
        for p in bot_processes:
            if p.poll() is None:
                p.kill()
        bot_processes = []
    gradient_print(" All bots stopped.", 0.03)

def start_botnet():
    clear()
    print_banner()

    host = gradient_input(" Server IP: ").strip()
    if not host:
        gradient_print(" IP not entered.", 0.03)
        time.sleep(1)
        return

    port_str = gradient_input(" Port (default 25565): ").strip()
    port = int(port_str) if port_str.isdigit() else 25565

    version = gradient_input(" Minecraft version: ").strip()
    if not version:
        version = "1.16.5"

    count_str = gradient_input(" Number of bots: ").strip()
    if not count_str.isdigit():
        gradient_print(" Invalid number.", 0.03)
        time.sleep(1)
        return
    count = int(count_str)
    if count > 100:
        gradient_print(" Too many bots (max 100).", 0.03)
        time.sleep(1)
        return

    commands_file = gradient_input(" Path to commands file (leave empty if none): ").strip()
    if commands_file and not os.path.exists(commands_file):
        gradient_print(f" File {commands_file} not found. No commands will be executed.", 0.03)
        commands_file = ""

    global bot_processes
    with bot_lock:
        if bot_processes:
            stop_all_bots()

    gradient_print(f"\n Launching {count} bots with 5 second interval...", 0.03)
    stop_reading = threading.Event()

    for i in range(1, count + 1):
        bot_name = f"Bot_{i}"
        cmd = ["node", "bot.js", host, str(port), version, bot_name]
        if commands_file:
            cmd.append(commands_file)
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                encoding='utf-8',
                errors='replace'
            )
            with bot_lock:
                bot_processes.append(proc)

            def read_output(p, name, stop_event):
                try:
                    for line in iter(p.stdout.readline, ''):
                        if stop_event.is_set():
                            break
                        if line:
                            print(f"\033[36m[{name}]\033[0m {line.strip()}")
                except:
                    pass
                finally:
                    p.stdout.close()

            t = threading.Thread(target=read_output, args=(proc, bot_name, stop_reading), daemon=True)
            t.start()

            gradient_print(f" Launched {bot_name}", 0.01)
            if i < count:
                time.sleep(5)
        except Exception as e:
            gradient_print(f" Error launching {bot_name}: {e}", 0.03)

    with bot_lock:
        bot_processes[:] = [p for p in bot_processes if p.poll() is None]

    gradient_print(f"\n Launched {len(bot_processes)} bots.", 0.03)
    if commands_file:
        gradient_print(f" Bots will execute commands from {commands_file}", 0.02)

    gradient_print("\n === DEBUG MODE ===", 0.02)
    gradient_print(" Bot output (commands, chat) will appear above.", 0.02)
    gradient_print(" Type 'stop' to terminate all bots and return to menu.", 0.02)

    while True:
        try:
            user_input = input().strip().lower()
            if user_input == 'stop':
                break
            else:
                print(" Unknown command. Type 'stop' to exit.")
        except KeyboardInterrupt:
            break

    stop_reading.set()
    stop_all_bots()
    gradient_print(" Returning to main menu...", 0.03)
    time.sleep(1)