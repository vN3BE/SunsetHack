#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import json
import struct
import time
from utils import clear, print_banner, gradient_print, gradient_input

def varint_to_bytes(value):
    result = bytearray()
    while True:
        if value & ~0x7F == 0:
            result.append(value)
            break
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    return bytes(result)

def read_varint(sock):
    result = 0
    shift = 0
    while True:
        b = sock.recv(1)
        if not b:
            raise ConnectionError("Connection lost")
        b = b[0]
        result |= (b & 0x7F) << shift
        shift += 7
        if (b & 0x80) == 0:
            break
    return result

def read_varint_from_bytes(data):
    result = 0
    shift = 0
    idx = 0
    while True:
        if idx >= len(data):
            raise ValueError("Not enough data")
        b = data[idx]
        idx += 1
        result |= (b & 0x7F) << shift
        shift += 7
        if (b & 0x80) == 0:
            break
    return result, idx

def ping_minecraft_server(host, port=25565, timeout=5):
    try:
        start_time = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        protocol_version = 754
        server_address = host
        server_port = port
        next_state = 1
        handshake = bytearray()
        handshake.append(0x00)
        handshake.extend(varint_to_bytes(protocol_version))
        handshake.extend(varint_to_bytes(len(server_address)))
        handshake.extend(server_address.encode('utf-8'))
        handshake.extend(struct.pack('>H', server_port))
        handshake.append(next_state)
        data = varint_to_bytes(len(handshake)) + handshake
        sock.send(data)
        sock.send(varint_to_bytes(1) + b'\x00')
        length = read_varint(sock)
        packet_data = b''
        while len(packet_data) < length:
            packet_data += sock.recv(length - len(packet_data))
        if packet_data[0] != 0x00:
            raise Exception("Invalid server response")
        json_length, offset = read_varint_from_bytes(packet_data[1:])
        json_str = packet_data[1+offset:1+offset+json_length].decode('utf-8')
        sock.close()
        ping_time = int((time.time() - start_time) * 1000)
        return json.loads(json_str), ping_time
    except Exception:
        return None, None

def scan_server(host, port=25565, timeout=5):
    data, ping_ms = ping_minecraft_server(host, port, timeout)
    if data is None:
        return {
            'success': False,
            'host': host,
            'port': port,
            'error': 'Could not connect or server did not respond'
        }
    description = data.get('description')
    motd = description.get('text', str(description)) if isinstance(description, dict) else str(description) if description else "No MOTD"
    players = data.get('players', {})
    online = players.get('online', 0)
    max_players = players.get('max', 0)
    sample = players.get('sample', [])
    player_names = [p.get('name', '?') for p in sample[:5]]
    players_str = ", ".join(player_names) if player_names else "no data"
    version_info = data.get('version', {})
    version_name = version_info.get('name', 'Unknown')
    protocol = version_info.get('protocol', 0)
    enforces_secure_chat = data.get('enforcesSecureChat', False)
    secure_chat_str = "true" if enforces_secure_chat else "false"
    return {
        'success': True,
        'host': host,
        'port': port,
        'motd': motd,
        'version': version_name,
        'protocol': protocol,
        'online': online,
        'max_players': max_players,
        'players_sample': players_str,
        'ping_ms': ping_ms,
        'secure_chat': secure_chat_str
    }

def scan_server_interactive():
    clear()
    print_banner()
    server_input = gradient_input(" Enter IP:port (default port 25565) → ").strip()
    if ':' in server_input:
        host, port_str = server_input.split(':', 1)
        try:
            port = int(port_str)
        except:
            gradient_print(" Invalid port. Using 25565", 0.03)
            port = 25565
    else:
        host = server_input
        port = 25565
    if not host:
        gradient_print(" IP not entered. Aborted.", 0.03)
        time.sleep(1.5)
        return
    time.sleep(0.5)
    result = scan_server(host, port, timeout=5)
    if not result['success']:
        gradient_print(f"\n{result['error']}", 0.03)
    else:
        lines = [
            f" [IPPort] {result['host']}:{result['port']}",
            f" [MOTD] {result['motd']}",
            f" [Version] {result['version']}",
            f" [Protocol] {result['protocol']}",
            f" [Connected] {result['online']}/{result['max_players']}",
            f" [Players] {result['players_sample']}",
            f" [Ping] {result['ping_ms']} ms",
            f" [SecureChat] {result['secure_chat']}"
        ]
        for line in lines:
            gradient_print(line, 0.025)
            time.sleep(0.1)
    print()
    gradient_input(" Press Enter to return to menu...")