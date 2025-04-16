#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import logging
import requests
import subprocess
import webbrowser  
from bs4 import BeautifulSoup
from pathlib import Path
import random
import phonenumbers
from phonenumbers import carrier
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions

#get the directory of the current script
script_dir = Path(__file__).resolve().parent
print("Script directory:", script_dir)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class email_info:  # Placeholder class for future email functionality
    def email_search(em):
        webbrowser.open(f'https://www.skymem.info/srch?q={em}&ss=srch')
        #webbrowser.open(f'https://www.melissa.com/v2/lookups/emailcheck/email/?email={em}&site=')



class license_plate_info:
    # These functions open lookup URLs for license plates and VINs.
    @staticmethod
    def license_plate_search(plate, state):
        webbrowser.open(f'https://www.faxvin.com/license-plate-lookup/result?plate={plate}&state={state}')
        webbrowser.open(f'https://www.findbyplate.com/US/{state}/{plate}/')

    @staticmethod
    def vin_search(vin):
        webbrowser.open(f'https://www.vehiclehistory.com/vin-report/{vin}')
        webbrowser.open(f'https://www.vindecoderz.com/EN/check-lookup/{vin}')



class name_info:  # Placeholder class for future name functionality
    def name_search(n, s, c):
        webbrowser.open(f'https://www.fastpeoplesearch.com/name/{n}_{c}-{s}') #might wanna remove this 
        webbrowser.open(f'https://www.searchpeoplefree.com/find/{n}/{s}/{c}')
        webbrowser.open(f'https://www.peoplesearchnow.com/person/{n}_{c}_{s}')



class username_info:  
    def username_search(username):
        print("Choose a option to use to search about a username")
        print("1. Scrape info about username from websites")
        print("2. Use whatsmyname.app to find information about a username")
        usernamesearchoptionchoice = input("What option would you like to use:")

        if usernamesearchoptionchoice == '1':
            social_media_platforms = {
            "facebook": f"https://facebook.com/{username}",
            "twitter": f"https://twitter.com/{username}",
            "telegram": f"https://t.me/{username}",
            "youtube": f"https://youtube.com/{username}",
            "instagram": f"https://instagram.com/{username}",
            "tiktok": f"https://www.tiktok.com/{username}",
            "github": f"https://github.com/{username}",
            "linkedin": f"https://www.linkedin.com/in/{username}",
            "pinterest": f"https://pinterest.com/{username}",
            "flickr": f"https://flickr.com/people/{username}",
            "hashnode": f"https://hashnode.com/@{username}",
            "medium": f"https://medium.com/@{username}",
            "hackerone": f"https://hackerone.com/{username}",
            "imgur": f"https://imgur.com/user/{username}",
            "spotify": f"https://open.spotify.com/user/{username}",
            "pastebin": f"https://pastebin.com/u/{username}",
            "wattpad": f"https://wattpad.com/user/{username}",
            "codecademy": f"https://codecademy.com/{username}",
            "wikipedia": f"https://www.wikipedia.org/wiki/User:{username}",
            "blogspot": f"https://{username}.blogspot.com/",
            "tumblr": f"https://{username}.tumblr.com/",
            "wordpress": f"https://{username}.wordpress.com/",
            "steamcommunity": f"https://steamcommunity.com/id/{username}",
            "zone-h": f"http://www.zone-h.org/archive/notifier={username}"
            }

            print(f"Checking social media links for {username}")
            print("#" * 126)
            print("# SOCIAL MEDIA   |        USER        | STATUS CODE | URL" + " " * 49 + " #")
            
            for platform, url in social_media_platforms.items():
                try:
                    req = requests.get(url)
                    code = req.status_code
                except requests.exceptions.TooManyRedirects:
                    print("TooManyRedirects")
                    break
                except requests.exceptions.ConnectionError:
                    print("\n\nConnectionError!\n\nCheck your internet connection!\n\n")
                    break
                except requests.exceptions.Timeout:
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
        
        if usernamesearchoptionchoice == '2':
            print("Opening whatsmyname.app")
            print("Just type in the name you want to search in the app")
            webbrowser.open(f'https://whatsmyname.app/?q={username}')




class phone_number_info:
    # Load user agents once as a class variable
    try:
        with open(script_dir / "useragents.txt", "r") as file:
            user_agents = [line.strip() for line in file if line.strip()]
    except Exception as e:
        logging.error("Failed to load user agents: %s", e)
        user_agents = []

    # ------------------------------------------------
    # COUNTRY CODES (from country.json)
    # ------------------------------------------------
    @staticmethod
    def load_country_codes(filepath=script_dir / 'country.json'):
        """
        Loads country codes from a JSON file and returns them as a dictionary.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                codes = json.load(f)
            return codes
        except Exception as e:
            print("Error loading country codes:", e)
            return {}

    @staticmethod
    def get_country_code(country, codes):
        """
        Retrieves the country code for a given country name from the dictionary.
        """
        print(f"Getting country code for: {country}")
        return codes.get(country)

    # ------------------------------------------------
    # REQUESTS MODULE (Synchronous HTTP request wrapper)
    # ------------------------------------------------
    @staticmethod
    def make_request(url, method="GET", **kwargs):
        """
        A generic HTTP request wrapper.
        """
        logging.info("Making a %s request to URL: %s", method, url)
        try:
            if method.upper() == "GET":
                response = requests.get(url, **kwargs)
            elif method.upper() == "POST":
                response = requests.post(url, **kwargs)
            else:
                raise ValueError("Unsupported method")
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error("HTTP request error: %s", e)
            return None

    # ------------------------------------------------
    # ANNUAIRE MODULE (annuaire_lookup from annuaire.py)
    # ------------------------------------------------
    @staticmethod
    def annuaire_lookup(p_n, output=False, file=None):
        browser = input("What's your browser? Chrome or Firefox? (c/f): ")
        if browser.lower() == 'c':
            options = Options()
            try:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                print("Driver setup completed\n")
            except Exception as e:
                print("Error while driver setup:", e)
                return
        elif browser.lower() == 'f':
            options = FirefoxOptions()
            try:
                driver = webdriver.Firefox(options=options)
                print("Driver setup completed\n")
            except Exception as e:
                print("Error while driver setup:", e)
                return
        else:
            print("Invalid browser option.")
            return

        driver.get("https://www.pagesjaunes.fr/annuaireinverse")
        print("You have 10 seconds to accept any pop-ups or notices.")
        time.sleep(10)

        try:
            # Using explicit waits instead of fixed sleeps:
            wait = WebDriverWait(driver, 10)
            input_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="quoiqui"]'))
            )
            input_element.send_keys(p_n)
            # Try to locate a clickable button within the form.
            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="form_motor_pagesjaunes"]//button'))
            )
            button.click()
        except Exception as e:
            print("Error while performing search:", e)
            driver.quit()
            return

        success = 0 if output else None

        try:
            pn = p_n.replace("+", "")
            result = driver.find_element(By.XPATH, '//*[@id="SEL-nbresultat"]')
            try:
                count = int(result.text.strip())
            except Exception:
                count = 0
            plural = "s" if count > 1 else ""
            print(f"\n{result.text} result{plural} found in PageBlanche")
            print(f"Link => https://www.pagesjaunes.fr/annuaireinverse/recherche?quoiqui={pn}&univers=annuaireinverse&idOu=")
            if output and file:
                with open(file, 'w') as output_file:
                    output_file.write(f"[>] {result.text} result{plural} found in PageBlanche\n[=] Link => https://www.pagesjaunes.fr/annuaireinverse/recherche?quoiqui={pn}&univers=annuaireinverse&idOu=")
                success += 1
        except Exception:
            print("\nNo result found in PageBlanche")
            if output and file:
                with open(file, 'w') as output_file:
                    output_file.write("[-] No result found in PageBlanche")
                success += 1

        driver.quit()

        if output:
            print(f"\nOutput saved ({success})")


    # ------------------------------------------------
    # FREE LOOKUP MODULE (free_lookup from free_lookup.py)
    # ------------------------------------------------
    @staticmethod
    def free_lookup(phone_number, useragents_file=script_dir / "useragents.txt"):
        # Read user agents from file and prepare headers.
        try:
            with open(useragents_file, 'r') as file:
                agents = [line.strip() for line in file if line.strip()]
        except Exception as e:
            print("Error reading user agents:", e)
            agents = phone_number_info.user_agents

        if not agents:
            agents = ["Mozilla/5.0"]  # Fallback default

        headers = {'user-agent': random.choice(agents)}
        url = f"https://free-lookup.net/{phone_number}"
        response = phone_number_info.make_request(url, headers=headers)
        if response is None:
            print("Error: No response from Free Lookup service.")
            return
        html = BeautifulSoup(response.text, "html.parser")
        try:
            divs = html.find("ul", class_="report-summary__list").find_all("div")
        except AttributeError:
            print("Error parsing Free Lookup response.")
            return
        info_dict = {
            key.get_text(strip=True): (value.get_text(strip=True) or "Not found")
            for key, value in zip(divs[::2], divs[1::2])
        }
        print("\n[> ] Free-lookup")
        for key, value in info_dict.items():
            if value != "Not found":
                print(f"  ├── {key}: {value}")

    # ------------------------------------------------
    # LOOKUP MODULE (lookup from lookup.py)
    # ------------------------------------------------
    @staticmethod
    def lookup(phone_number):
        """
        Performs the basic lookup on the phone number (parsing, validation,
        operator and country code identification).
        """
        print()
        try:
            # If phone number does not start with '+' assume US as default.
            if not phone_number.startswith("+"):
                parsed = phonenumbers.parse(phone_number, "US")
            else:
                parsed = phonenumbers.parse(phone_number)
        except Exception as e:
            print("Error parsing phone number:", e)
            return

        operator_name = carrier.name_for_number(parsed, "fr")
        line_type = phonenumbers.number_type(parsed)

        if line_type == phonenumbers.PhoneNumberType.FIXED_LINE:
            line_info = "Line type: Fixed"
        elif line_type == phonenumbers.PhoneNumberType.MOBILE:
            line_info = "Line type: Mobile"
        else:
            line_info = "Line not found"

        possible = phonenumbers.is_possible_number(parsed)
        valid = phonenumbers.is_valid_number(parsed)
        
        # Use the load_country_codes method for consistency.
        country_data = phone_number_info.load_country_codes()

        matched_countries = []
        for country in country_data.keys():
            code = phone_number_info.get_country_code(country, country_data)
            if phone_number.startswith(code):
                matched_countries.append(country)
                # The break condition retained from your original code.
                if len(matched_countries) >= 153:
                    break

        print(f"Phone number: {phone_number}")
        print(f"Possible: {'✔️' if possible else '❌'}")
        print(f"Valid: {'✔️' if valid else '❌'}")
        print()

        if operator_name:
            print(f"Operator: {operator_name}")
        else:
            print("Operator: Not found")

        try:
            location_str = ", ".join(matched_countries)
            print("Possible location: " + location_str)
        except Exception:
            print("Location: Not found")

        print(line_info)

    # ------------------------------------------------
    # SPAM MODULE (spamcalls from spam.py)
    # ------------------------------------------------
    @staticmethod
    def spamcalls(p_n):
        print("\n[> ] Spamcalls")
        # Note: The service may return 410 Gone if the endpoint has been removed.
        url = f"https://spamcalls.net/en/num/{p_n}"
        headers = {'user-agent': random.choice(phone_number_info.user_agents) if phone_number_info.user_agents else "Mozilla/5.0"}
        response = phone_number_info.make_request(url, headers=headers)
        if response and response.status_code == 200:
            print("  └── ! Spammer")
        else:
            print("  └── > Not spammer")

    # ------------------------------------------------
    # CLI MODULE (orchestrates all phone number info functions)
    # ------------------------------------------------
    @staticmethod
    def call_all_of_phonenuminfo(phone_number):
        """
        Call all functions related to phone number information.
        """
        print("\n[> ] Phone Number Information")
        phone_number_info.lookup(phone_number)
        phone_number_info.free_lookup(phone_number.replace("+", ""))
        phone_number_info.annuaire_lookup(phone_number)
        phone_number_info.spamcalls(phone_number)
        print("\n[> ] All functions executed successfully.")


# ------------------------------
# CLI Placeholder Functions
# ------------------------------
def osint_name_search():
    n = input("Enter Name (ex: michael-scott): ")
    s = input("Enter State Initials (ex: ny): ")
    c = input("Enter City (ex: scranton): ")
    name_info.name_search(n, s, c)


def osint_email_search():
    em = input("Enter email: ")
    email_info.email_search(em)


def osint_license_plate_search():
    # Optionally, call the license_plate_info methods.
    plate = input("Enter license plate: ")
    state = input("Enter state: ")
    license_plate_info.license_plate_search(plate, state)


def osint_vin_search():
    # Optionally, call the license_plate_info methods.
    vin = input("Enter VIN: ")
    license_plate_info.vin_search(vin)


def osint_username_search():
    username = input("Enter username: ")    
    username_info.username_search(username)


def osint_phone_search():
    phone = input("Enter phone number: ")
    phone_number_info.call_all_of_phonenuminfo(phone)


# ------------------------------
# MAIN METHOD and Menu
# ------------------------------
def print_menu():
    print("""
      ____   _____ _____ _   _ _______    
     / __ \ / ____|_   _| \ | |__   __|
    | |  | | (___   | | |  \| |  | |  
    | |  | |\___ \  | | | . ` |  | |   
    | |__| |____) |_| |_| |\  |  | |  
     \____/|_____/|_____|_| \_|  |_|     

     _______  __  .__   __.  _______  .______    _______   ______   .______    __       _______  __  .__   __.  _______   ______   
    |   ____||  | |  \ |  | |       \ |   _  \  |   ____| /  __  \  |   _  \  |  |     |   ____||  | |  \ |  | |   ____| /  __  \  
    |  |__   |  | |   \|  | |  .--.  ||  |_)  | |  |__   |  |  |  | |  |_)  | |  |     |  |__   |  | |   \|  | |  |__   |  |  |  | 
    |   __|  |  | |  . `  | |  |  |  ||   ___/  |   __|  |  |  |  | |   ___/  |  |     |   __|  |  | |  . `  | |   __|  |  |  |  | 
    |  |     |  | |  |\   | |  '--'  ||  |      |  |____ |  `--'  | |  |      |  `----.|  |____ |  | |  |\   | |  |     |  `--'  | 
    |__|     |__| |__| \__| |_______/ | _|      |_______| \______/  | _|      |_______||_______||__| |__| \__| |__|      \______/  
                                                                                                                                                                                                                                         
        Made by BJW333
                                                
        1. Name Search
        2. Phone Number Search
        3. E-Mail Search
        4. License Plate Search 
        5. VIN Search
        6. Username Search
        7. Exit
        """)


def main():
    while True:
        print_menu()
        choice = input("OSINT: ").strip()
        if choice == '1':
            osint_name_search()
        elif choice == '2':
            osint_phone_search()
        elif choice == '3':
            osint_email_search()
        elif choice == '4':
            osint_license_plate_search()
        elif choice == '5':
            osint_vin_search()
        elif choice == '6':
            osint_username_search()
        elif choice == '7' or choice.lower() in ['exit', 'quit']:
            sys.exit()
        else:
            print("Invalid option. Please try again.")


# ------------------------------
# Main Entry Point
# ------------------------------
if __name__ == "__main__":
    main()