# coding=utf-8
#!/usr/bin/env python3

import requests
import json
from libs.utils import print_success, print_error, print_status

def find_proxies():
    """
    Fetches high-quality rotating proxies from your Proxifly API.
    """
    api_key = "8oeNKZreputk37mjiajRCKkk7BiPQSfZYgpjcm6qnnjz"
    url = "https://api.proxifly.dev/get-proxy"
    payload = {
        "apiKey": api_key,
        "https": True,
        "quantity": 50
    }
    
    print_status("Fetching premium proxies...")
    try:
        response = requests.post(url, json=payload, timeout=20)
        if response.status_code == 200:
            data = response.json()
            proxy_list = []
            
            items = data if isinstance(data, list) else [data]
            
            for item in items:
                if 'proxy' in item:
                    p = item['proxy'].replace('http://', '').replace('https://', '').replace('socks5://', '')
                    proxy_list.append(p)
            
            # Save to file for reuse
            with open('proxies.txt', 'w') as f:
                for p in proxy_list:
                    f.write(p + '\n')
            
            print_success(f"Successfully fetched {len(proxy_list)} premium proxies and saved to 'proxies.txt'.")
            return proxy_list
        else:
            print_error(f"API Error: {response.status_code}")
            return []
    except Exception as e:
        print_error(f"API Connection error: {e}")
        return []
