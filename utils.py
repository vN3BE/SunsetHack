#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_gradient_color(position, total):
    ratio = position / max(total, 1)
    # Нежный градиент: от светло-голубого (173,216,230) до светло-розового (255,182,193)
    r1, g1, b1 = 173, 216, 230   # нежно-голубой
    r2, g2, b2 = 255, 182, 193   # нежно-розовый
    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)
    return f"\033[38;2;{r};{g};{b}m"

def gradient_print(text, delay=0.02):
    total = len(text)
    for i, char in enumerate(text):
        color = get_gradient_color(i, total)
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\033[0m\n")

def gradient_prompt(text, delay=0.02):
    total = len(text)
    for i, char in enumerate(text):
        color = get_gradient_color(i, total)
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\033[0m")
    sys.stdout.flush()

def gradient_input(prompt):
    gradient_prompt(prompt)
    return input()

def print_banner():
    banner = r'''  /$$$$$$                                            /$$     /$$   /$$                     /$$      
 /$$__  $$                                          | $$    | $$  | $$                    | $$      
| $$  \__/ /$$   /$$ /$$$$$$$   /$$$$$$$  /$$$$$$  /$$$$$$  | $$  | $$  /$$$$$$   /$$$$$$$| $$   /$$
|  $$$$$$ | $$  | $$| $$__  $$ /$$_____/ /$$__  $$|_  $$_/  | $$$$$$$$ |____  $$ /$$_____/| $$  /$$/
 \____  $$| $$  | $$| $$  \ $$|  $$$$$$ | $$$$$$$$  | $$    | $$__  $$  /$$$$$$$| $$      | $$$$$$/ 
 /$$  \ $$| $$  | $$| $$  | $$ \____  $$| $$_____/  | $$ /$$| $$  | $$ /$$__  $$| $$      | $$_  $$ 
|  $$$$$$/|  $$$$$$/| $$  | $$ /$$$$$$$/|  $$$$$$$  |  $$$$/| $$  | $$|  $$$$$$$|  $$$$$$$| $$ \  $$
 \______/  \______/ |__/  |__/|_______/  \_______/   \___/  |__/  |__/ \_______/ \_______/|__/  \__/
              TG: @SunSetHack // coder: @vN3BE // sposnor: @m0nifest // ver: beta                          '''

    lines = banner.split('\n')
    total_length = sum(len(line) for line in lines)
    current_pos = 0
    print()
    for line in lines:
        for char in line:
            color = get_gradient_color(current_pos, total_length)
            sys.stdout.write(color + char)
            current_pos += 1
        sys.stdout.write("\033[0m\n")
    print()