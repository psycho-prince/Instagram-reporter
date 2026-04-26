# coding=utf-8
#!/usr/bin/env python3

import argparse
import random
import time
from sys import exit
from os import _exit, path
from multiprocessing import Pool
from colorama import Fore, Style

from libs.check_modules import check_modules
from libs.logo import print_logo
from libs.utils import print_success, print_error, ask_question, print_status, parse_proxy_file
from libs.proxy_harvester import find_proxies
from libs.attack import report_profile_attack, report_video_attack

# Ensure modules are present
check_modules()

DEFAULT_TARGET = "_._alphonsa_._"

def attack_worker(args):
    """Worker function for the multiprocessing pool."""
    target, proxy, attack_type = args
    try:
        # Increase jitter to prevent bot detection and improve reliability
        time.sleep(random.uniform(5, 15))
        attack_type(target, proxy)
    except Exception as e:
        print_error(f"Process error: {e}")

def start_attack(target, proxies, attack_type, rounds=1, batch_delay=10):
    # Reduced concurrency to 2 to lower attack profile and improve stability
    max_concurrent = 2 
    
    if not proxies:
        print_status(f"No proxies provided. Running limited reports ({max_concurrent} concurrent).")
        proxies = [None] * max_concurrent
    else:
        print_status(f"{'Profile' if attack_type == report_profile_attack else 'Video'} complaint attack is starting!\n")
    
    total_rounds = rounds
    for r in range(1, total_rounds + 1):
        if total_rounds > 1:
            print_status(f"--- Round {r} of {total_rounds} ---")
            
        pool_args = [(target, proxy, attack_type) for proxy in proxies]
        total = len(proxies)
        print_status(f"Starting {total} transactions in this round with {max_concurrent} concurrent workers...")
        
        try:
            with Pool(processes=max_concurrent) as pool:
                for i, _ in enumerate(pool.imap_unordered(attack_worker, pool_args), 1):
                    if i % 5 == 0 or i == total:
                        print_status(f"Progress: {i}/{total} transactions completed in round {r}...")
        except Exception as e:
            print_error(f"Pool error: {e}")
        
        if r < total_rounds:
            print_status(f"Round {r} complete. Waiting {batch_delay} seconds before next round (Rate Limiting)...")
            time.sleep(batch_delay)
    
    print_success("All reporting sequences complete!")

def main():
    parser = argparse.ArgumentParser(description="Instagram Account Reporter Tool by rhyugen")
    parser.add_argument("-u", "--username", help="Target Instagram username")
    parser.add_argument("-v", "--video", help="Target Instagram video URL")
    parser.add_argument("-p", "--proxy", help="Path to proxy file")
    parser.add_argument("--auto-proxy", action="store_true", help="Automatically gather proxies from the internet")
    parser.add_argument("--rounds", type=int, default=1, help="Number of reporting rounds (default: 1)")
    parser.add_argument("--delay", type=int, default=10, help="Delay between batches in seconds (default: 10)")
    parser.add_argument("--limit", type=int, default=100, help="Limit the number of proxies/reports (default: 100)")
    
    args = parser.parse_args()

    print_logo()
    print_success("Modules loaded!\n")

    proxies = []
    
    # Proxy Logic
    if args.auto_proxy:
        print_status("Gathering proxies from the Internet! This may take a while.\n")
        proxies = find_proxies()
        if len(proxies) > args.limit:
            proxies = proxies[:args.limit]
            print_status(f"Limited to {args.limit} proxies for this session.")
    elif not args.username and not args.video:
        # Interactive mode if no args provided
        ret = ask_question("Would you like to use a proxy? [Y/N]")
        if ret.lower() == 'y':
            ret = ask_question("Gather proxies from internet? [Y/N]")
            if ret.lower() == 'y':
                print_status("Gathering proxies...\n")
                proxies = find_proxies()
            else:
                file_path = ask_question("Enter proxy file path")
                proxies = parse_proxy_file(file_path)

    # Target Logic
    if args.username:
        start_attack(args.username, proxies, report_profile_attack, args.rounds, args.delay)
    elif args.video:
        start_attack(args.video, proxies, report_video_attack, args.rounds, args.delay)
    else:
        print_status("1 - Report the profile.")
        print_status("2 - Report a video.")
        print_status(f"Default target: {DEFAULT_TARGET}")
        choice = ask_question("Please select method (Press Enter for Default Profile Report)")
        
        if choice == '1' or choice == '':
            target = ask_question(f"Enter username (Default: {DEFAULT_TARGET})")
            if not target: target = DEFAULT_TARGET
            rounds = int(ask_question("Enter number of rounds (Default: 1)") or "1")
            delay = int(ask_question("Enter delay between rounds in seconds (Default: 10)") or "10")
            start_attack(target, proxies, report_profile_attack, rounds, delay)
        elif choice == '2':
            target = ask_question("Enter video link")
            rounds = int(ask_question("Enter number of rounds (Default: 1)") or "1")
            delay = int(ask_question("Enter delay between rounds in seconds (Default: 10)") or "10")
            start_attack(target, proxies, report_video_attack, rounds, delay)
        else:
            print_error("Invalid choice.")
            exit(1)

if __name__ == "__main__":
    try:
        main()
        print(Style.RESET_ALL)
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[ * ] The program is closing!")
        print(Style.RESET_ALL)
        _exit(0)
