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
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import subprocess

numverify_api_key = 'apikey'
twilio_account_sid = 'apikey'
twilio_auth_token = 'apikey'
client = Client(twilio_account_sid, twilio_auth_token)

def main():
    while True:
        print("""
        ____   _____ _____ _   _ _______    
       / __ \ / ____|_   _| \ | |__   __|
      | |  | | (___   | | |  \| |  | |  
      | |  | |\___ \  | | | . ` |  | |   
      | |__| |____) |_| |_| |\  |  | |  
       \____/|_____/|_____|_| \_|  |_|     
        
        Made by BJW333
                                                
        1. Name Search
        2. Phone Search/Phoneinfoga
        3. E-Mail Search
        4. License Plate Search 
        5. VIN Search
        6. Username
        7. exit
        
        """)
        ch = input("OSINT: ")
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
    print('Please first enter the phone number to be searched')
    phone_number = input("Input phone number with country code: ")
    print("")
    print('What type of tool would you like to use')
    print("1. Phone number info")
    print("2. Web Scrape for info")
    print("3. go back")
    choices = input("Which tool:")
    
    

    def get_phone_info(phone_number):
        info = {}
    
    # NumVerify API for basic info
        try:
            numverify_response = requests.get(f"http://apilayer.net/api/validate?access_key={numverify_api_key}&number={phone_number}&country_code=&format=1")
            numverify_response.raise_for_status()  # Raises stored HTTPError, if one occurred.
            numverify_data = numverify_response.json()
            info['country'] = numverify_data.get('country_name')
            info['location'] = numverify_data.get('location')
            info['carrier'] = numverify_data.get('carrier')
            info['line_type'] = numverify_data.get('line_type')
        except Exception as e:
            print(f"Error fetching from NumVerify: {e}")
    
    # Twilio API for detailed info
        try:
            twilio_client = Client(twilio_account_sid, twilio_auth_token)
            twilio_response = twilio_client.lookups \
                .v1 \
                .phone_numbers(phone_number) \
                .fetch(type=['carrier', 'caller-name'])
            info['twilio_carrier'] = twilio_response.carrier.get('name')
            info['twilio_caller_name'] = twilio_response.caller_name.get('caller_name')
            info['country_code'] = twilio_response.country_code
            info['national_format'] = twilio_response.national_format
            info['line_type'] = twilio_response.carrier.get('type')

        except Exception as e:
            print(f"Error fetching from Twilio: {e}")
        
    
        try:
            info['web_search_results'] = web_scrape_search(phone_number)
        except Exception as e:
            print(f"Error during web scraping: {e}")
    

        return info


    
    def web_scrape_search(phone_number):
    # DuckDuckGo's HTML results (note: URL structure could change)
        url = f"https://html.duckduckgo.com/html/?q={phone_number}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensure we notice bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find and return the first few summaries (this is a simplified approach)
        summaries = soup.find_all('a', class_='result__a', limit=30)
        results = [summary.get_text() for summary in summaries]
        return results
    
    def run_phoneinfoga(phone_number):
        try:
                # Execute PhoneInfoga scan command
            result = os.system(" phoneinfoga scan -n " + ( phone_number ))
            # Extract output
            return result
        except subprocess.CalledProcessError as e:
        # Handle error if PhoneInfoga command fails
            print(f"PhoneInfoga command failed with error: {e}")
        return None

    def summarize_info(phone_info, phone_number):
        print("Summary of Phone Number Information")
        print("===========================================")
        print(f"Country: {phone_info.get('country', 'N/A')}")
        print(f"Country Code: {phone_info.get('country_code', 'N/A')}")
        print(f"National Format: {phone_info.get('national_format', 'N/A')}")
        print(f"Location: {phone_info.get('location', 'N/A')}")
        print(f"Carrier: {phone_info.get('carrier', 'N/A')}")
        print(f"Line Type: {phone_info.get('line_type', 'N/A')}")
        print(f"Twilio Carrier: {phone_info.get('twilio_carrier', 'N/A')}")
        print(f"Twilio Caller Name: {phone_info.get('twilio_caller_name', 'N/A')}")
        print("===========================================")
        time.sleep(3)
        phoneinfoga_output = run_phoneinfoga(phone_number)
        if phoneinfoga_output:
            print("PhoneInfoga Output:")
            print(phoneinfoga_output)

        
        if phone_info.get('web_search_results'):
            print("===========================================")
            print("Web Search Results:")
            for result in phone_info['web_search_results']:
               print(result)
        else:
            print("===========================================")
            print("No web search results found.")
            print("===========================================")


    if choices == "1":
        phone_numbertwilio = client.lookups.v2.phone_numbers(phone_number).fetch()
        print(phone_numbertwilio.phone_number)
        phone_info = get_phone_info(phone_number)
        summarize_info(phone_info, phone_number)

    if choices == "2":
        print("Looking on the web for information regarding that Phone Number")
        p = phone_number
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
