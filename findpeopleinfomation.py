import webbrowser
import sys
import time
import socket
import random
import os
import threading
import argparse
import importlib
from requests import get,exceptions
from os import system
from argparse import ArgumentParser

def main():
    while True:
        print("""
        ____   _____ _____ _   _ _______    
       / __ \ / ____|_   _| \ | |__   __|
      | |  | | (___   | | |  \| |  | |  
      | |  | |\___ \  | | | . ` |  | |   
      | |__| |____) |_| |_| |\  |  | |  
       \____/|_____/|_____|_| \_|  |_|     
                                                
        1. Name Search
        2. Phone Search/Phoneinfoga
        3. E-Mail Search
        4. License Plate Search 
        5. VIN Search
        6. Username
        7. exit
        
        """)
        ch = input("OSINT-X~>")
        if ch == '1':
            osintA()
        elif ch == '2':
            osintB()
        elif ch == '3':
            osintC()
        elif ch == '4':
            osintD()
        elif ch == '5':
            osintE()
        elif ch == '6':
            osintF()
        elif ch == 'exit' or 'quit' or 'Exit':
            exit()

def osintA():
    n = input("Enter Name (ex: michael-scott): ")
    s = input("Enter State Initials (ex: ny): ")
    c = input("Enter City (ex: scranton): ")
    webbrowser.open(f'https://www.fastpeoplesearch.com/name/{n}_{c}-{s}')
    webbrowser.open(f'https://www.searchpeoplefree.com/find/{n}/{s}/{c}')
    webbrowser.open(f'https://www.peoplesearchnow.com/person/{n}_{c}_{s}')

def osintB():
    print("1. Phoneinfoga")
    print("2. Web Scrape")
    print("3. go back")
    choices = input("which tool:")
    
    if choices == "1":
        print("Searching phone number info")
        phonenum2 = input("Phone number you would like to get info on include the country code 1 = USA: ")
        os.system(" phoneinfoga scan -n " + ( phonenum2 ))
        
    if choices == "2":
        p = input("Enter Phone Number (ex: 123-456-7890): ")
        webbrowser.open(f'https://www.fastpeoplesearch.com/{p}')
        webbrowser.open(f'https://www.searchpeoplefree.com/phone-lookup/{p}')
        webbrowser.open(f'https://www.peoplesearchnow.com/phone/{p}')
        webbrowser.open(f'https://www.whitepages.com/phone/1-{p}')
        webbrowser.open(f'https://www.thatsthem.com/phone/{p}')
        
    if choices == "3":
        main()
        
def osintC():
    em = input("Enter email: ")
    webbrowser.open(f'https://www.skymem.info/srch?q={em}&ss=home')
    webbrowser.open(f'https://www.melissa.com/v2/lookups/emailcheck/email/?email={em}&site=')

def osintD():
    plate = input("Enter license plate: ")
    s = input("Enter state: ")
    webbrowser.open(f'https://www.faxvin.com/license-plate-lookup/result?plate={plate}&state={s}')
    webbrowser.open(f'https://www.findbyplate.com/US/{s}/{plate}/')

def osintE():
    vin = input("Enter VIN: ")
    webbrowser.open(f'https://www.vehiclehistory.com/vin-report/{vin}')
    webbrowser.open(f'https://www.vindecoderz.com/EN/check-lookup/{vin}')
    
def osintF():
    print("Please enter the username you would like to search")
    u2 = input("The username you want to find: ")
    
    social = {
         "facebook":f"https://facebook.com/{u2}",
         "twitter":f"https://twitter.com/{u2}",
         "telegram":f"https://t.me/{u2}",
         "youtube":f"https://youtube.com/{u2}",
         "instagram":f"https://instagram.com/{u2}",
         "tiktok":f"https://www.tiktok.com/{u2}",
         "github":f"https://github.com/{u2}",
         "linkedin":f"https://www.linkedin.com/in/{u2}",
         "plus":f"https://plus.google.com/{u2}",
         "pinterest":f"https://pinterest.com/{u2}",
         "flickr":f"https://flickr.com/people/{u2}",
         "hashnode":f"https://hashnode.com/@{u2}",
         "twitter":f"https://twitter.com/{u2}",
         "medium":f"https://medium.com/@{u2}",
         "hackerone":f"https://hackerone.com/{u2}",
         "imgur":f"https://imgur.com/user/{u2}",
         "spotify":f"https://open.spotify.com/user/{u2}",
         "pastebin":f"https://pastebin.com/u/{u2}",
         "wattpad":f"https://wattpad.com/user/{u2}",
         "codecademy":f"https://codecademy.com/{u2}",
         "wikipedia":f"https://www.wikipedia.org/wiki/User:{u2}",
         "blogspot":f"https://{u2}.blogspot.com/",
         "tumblr":f"https://{u2}.tumblr.com/",
         "wordpress":f"https://{u2}.wordpress.com/",
         "steamcommunity":f"https://steamcommunity.com/id/{u2}",
         "zone-h":f"http://www.zone-h.org/archive/notifier={u2}"
    }

    print(f"Checking social media links for {u2}")
    print("#" * 126)
    print("# SOCIAL MEDIA   |        USER        | STATUS CODE | URL" + " " * 49 + " #")
    
    for platform, url in social.items():
        try:
            req = get(url)
            code = req.status_code
        except exceptions.TooManyRedirects:
            print("TooManyRedirects")
            break
        except exceptions.ConnectionError:
            print("\n\nConnectionError!\n\nCheck your internet connection!\n\n")
            break
        except exceptions.Timeout:
            continue
        
        user_status = (
            "| Found        " if code == 200
            else "| Not Found      " if code == 404
            else "| Undefined status code"
        )

        print(
            "#" + "-" * 124 + "#",
            f"# {platform: <16}{user_status}{code: <10}{url: <70} #"
        )

    print("#" * 126)
    print("\n")
    
if __name__ == "__main__":
    main()
