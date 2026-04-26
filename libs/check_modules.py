# coding=utf-8
#!/usr/bin/env python3

import sys

def check_modules():
    missing = []
    # asyncio is built-in, and proxybroker was unused.
    # curl_cffi is required by attack.py
    for module in ["requests", "colorama", "curl_cffi"]:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"[-] Missing packages: {', '.join(missing)}")
        print("[*] Please install them using: pip install -r requirements.txt")
        sys.exit(1)

    import warnings
    warnings.filterwarnings("ignore")

    from colorama import init
    init()
