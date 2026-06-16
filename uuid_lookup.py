#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import json
import time
from utils import clear, print_banner, gradient_print, gradient_input

def get_uuid_by_username(username):
    username = username.strip().lower()
    if not username:
        return {'success': False, 'error': 'Username cannot be empty'}
    try:
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            if 'id' in data:
                uuid_raw = data['id']
                uuid_formatted = f"{uuid_raw[:8]}-{uuid_raw[8:12]}-{uuid_raw[12:16]}-{uuid_raw[16:20]}-{uuid_raw[20:32]}"
                return {'success': True, 'nickname': data['name'], 'uuid': uuid_formatted}
            else:
                return {'success': False, 'error': f"Player with username '{username}' not found"}
    except urllib.error.HTTPError as e:
        if e.code == 204:
            return {'success': False, 'error': f"Player '{username}' not found"}
        else:
            return {'success': False, 'error': f"HTTP error {e.code}"}
    except Exception as e:
        return {'success': False, 'error': f"Connection error: {e}"}

def uuid_interactive():
    clear()
    print_banner()
    username = gradient_input(" Enter Minecraft username → ").strip()
    if not username:
        gradient_print(" [Error] Username cannot be empty.", 0.03)
        time.sleep(1.5)
        return
    time.sleep(0.5)
    result = get_uuid_by_username(username)
    if not result['success']:
        if "not found" in result['error'].lower():
            gradient_print(f" [Error] Player '{username}' not found (username may not exist).", 0.03)
        else:
            gradient_print(f" [Error] {result['error']}", 0.03)
    else:
        gradient_print(f" [Username] {result['nickname']}", 0.025)
        gradient_print(f" [UUID] {result['uuid']}", 0.025)
    print()
    gradient_input(" Press Enter to return to menu...")