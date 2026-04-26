# coding=utf-8
#!/usr/bin/env python3

import string
import random
import re
import time
import json
import os
from curl_cffi import requests
from libs.utils import print_success, print_error, print_status
from libs.user_agents import get_user_agent

class InstagramReporter:
    def __init__(self, proxy=None):
        self.session = requests.Session(impersonate="chrome120")
        self.user_agent = get_user_agent()
        self.proxy = proxy
        self.cookies_file = f"cookies_{hash(proxy) if proxy else 'direct'}.json"
        
        if proxy:
            self.session.proxies = {
                "https": f"http://{proxy}",
                "http": f"http://{proxy}"
            }
            
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "User-Agent": self.user_agent
        }

    def _warm_up_session(self):
        """Simulate human-like behavior to build session trust."""
        try:
            print_status("Warming up session...")
            # Visit landing page
            self.session.get("https://www.instagram.com/", headers=self.headers, timeout=15)
            time.sleep(random.uniform(3, 7))
            
            # Visit a popular public profile to look like a real user
            self.session.get("https://www.instagram.com/instagram/", headers=self.headers, timeout=15)
            time.sleep(random.uniform(5, 10))
            
            print_success("Session warmed up.")
            return True
        except Exception as e:
            print_error(f"Warm-up failed: {e}")
            return False

    def _get_tokens(self, form_id):
        try:
            if not self._warm_up_session():
                return None
            
            url = f"https://help.instagram.com/contact/{form_id}"
            res = self.session.get(url, headers=self.headers, timeout=20)
            
            if res.status_code != 200:
                print_error(f"Access Denied (Status {res.status_code}).")
                return None

            tokens = {
                "lsd": re.search(r'"lsd":"([^"]+)"', res.text).group(1) if re.search(r'"lsd":"([^"]+)"', res.text) else None,
                "fb_dtsg": re.search(r'\["DTSGInitialData",\[\],{"token":"([^"]+)"}', res.text).group(1) if re.search(r'\["DTSGInitialData",\[\],{"token":"([^"]+)"}', res.text) else None,
                "hsi": re.search(r'"hsi":"(\d+)"', res.text).group(1) if re.search(r'"hsi":"(\d+)"', res.text) else None,
                "rev": re.search(r'"server_revision":(\d+)', res.text).group(1) if re.search(r'"server_revision":(\d+)', res.text) else None,
                "jazoest": re.search(r'name="jazoest" value="(\d+)"', res.text).group(1) if re.search(r'name="jazoest" value="(\d+)"', res.text) else "2723"
            }
            return tokens
        except Exception as e:
            print_error(f"Stealth Init Error: {e}")
            return None

    def report_profile(self, username):
        if "instagram.com/" in username:
            username = username.split("instagram.com/")[1].split("?")[0].split("/")[0]
            
        form_id = "497253480400030"
        tokens = self._get_tokens(form_id)
        if not tokens or not tokens["lsd"]:
            print_error("Security Layer 1 Failure: Bot detection.")
            return False

        report_headers = {**self.headers, "X-FB-LSD": tokens["lsd"], "Content-Type": "application/x-www-form-urlencoded", "Origin": "https://help.instagram.com", "Referer": f"https://help.instagram.com/contact/{form_id}", "X-Requested-With": "XMLHttpRequest"}
        payload = {
            "jazoest": tokens["jazoest"], "lsd": tokens["lsd"], "instagram_username": username,
            "Field241164302734019_iso2_country_code": "US", "Field241164302734019": "United States",
            "support_form_id": form_id, "support_form_hidden_fields": "{}", "__a": "1", "__req": "1"
        }

        res = self.session.post("https://help.instagram.com/ajax/help/contact/submit/page", data=payload, headers=report_headers, timeout=20)
        if res.status_code == 200:
            print_success(f"Report successful for: {username}")
            return True
        return False

    def report_video(self, video_url):
        form_id = "440963189380968"
        tokens = self._get_tokens("497253480400030")
        if not tokens: return False
        
        report_headers = {**self.headers, "X-FB-LSD": tokens["lsd"], "Content-Type": "application/x-www-form-urlencoded", "Origin": "https://help.instagram.com", "Referer": f"https://help.instagram.com/contact/{form_id}"}
        payload = {
            "jazoest": tokens["jazoest"], "lsd": tokens["lsd"], "Field419623844841592": video_url,
            "Field1476905342523314_iso2_country_code": "US", "Field1476905342523314": "United States",
            "support_form_id": form_id, "__a": "1", "__req": "1"
        }
        res = self.session.post("https://help.instagram.com/ajax/help/contact/submit/page", data=payload, headers=report_headers, timeout=20)
        return res.status_code == 200

def report_profile_attack(username, proxy):
    reporter = InstagramReporter(proxy)
    reporter.report_profile(username)

def report_video_attack(video_url, proxy):
    reporter = InstagramReporter(proxy)
    reporter.report_video(video_url)
