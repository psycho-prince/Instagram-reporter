# coding=utf-8
#!/usr/bin/env python3
from colorama import Fore, Back, Style
from random import choice

logo = """
  _____           _         _____                               _               
 |_   _|         | |       |  __ \                             | |              
   | |  _ __  ___| |_ __ _ | |__) |___ _ __   ___  _ __| |_ ___ _ __ 
   | | | '_ \/ __| __/ _` ||  _  // _ \ '_ \ / _ \| '__| __/ _ \ '__|
  _| |_| | | \__ \ || (_| || | \ \  __/ |_) | (_) | |  | ||  __/ |   
 |_____|_| |_|___/\__\__,_||_|  \_\___| .__/ \___/|_|   \__\___|_|   
                                      | |                             
                                      |_|                             """

def print_logo():
    print(Fore.CYAN + Style.BRIGHT + logo + Style.RESET_ALL + Style.BRIGHT +"\n")
    print(Fore.YELLOW + "      Instagram Account Reporter Tool by rhyugen" + Style.RESET_ALL + Style.BRIGHT)
    print(Fore.GREEN + "\n      Modified and maintained by rhyugen")
    print(Style.RESET_ALL + Style.BRIGHT)
