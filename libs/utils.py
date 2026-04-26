# coding=utf-8
#!/usr/bin/env python3

from colorama import Fore, Style
from os import path
import random
from sys import exit
          
def print_success(message, *argv):
    args_str = " ".join(map(str, argv))
    print(f"{Fore.GREEN}[ OK ] {Style.RESET_ALL}{Style.BRIGHT}{message} {args_str}")

def print_error(message, *argv):
    args_str = " ".join(map(str, argv))
    print(f"{Fore.RED}[ ERR ] {Style.RESET_ALL}{Style.BRIGHT}{message} {args_str}")

def print_status(message, *argv):
    args_str = " ".join(map(str, argv))
    print(f"{Fore.BLUE}[ * ] {Style.RESET_ALL}{Style.BRIGHT}{message} {args_str}")

def ask_question(message, *argv):
    args_str = " ".join(map(str, argv))
    prompt = f"{Fore.BLUE}[ ? ] {Style.RESET_ALL}{Style.BRIGHT}{message} {args_str}: "
    return input(prompt)

def parse_proxy_file(fpath):
    if not path.exists(fpath):
        print()
        print_error(f"Proxy file not found: {fpath}")
        print_error("Exiting!")
        exit(1)
      
    proxies = []
    try:
        with open(fpath, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    proxies.append(line)
    except Exception as e:
        print_error(f"Error reading proxy file: {e}")
        exit(1)
      
    if len(proxies) > 50:
        proxies = random.sample(proxies, 50)
          
    print()
    print_success(f"{len(proxies)} proxies found!")
    return proxies
