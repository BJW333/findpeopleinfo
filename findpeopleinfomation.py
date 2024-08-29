import webbrowser
import os
import time
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import subprocess

# API keys and Twilio client setup
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
        6. Username Search
        7. Exit
        
        """)
        ch = input("OSINT: ")
        if ch == '1':
            osint_name_search()
        elif ch == '2':
            osint_phone_search()
        elif ch == '3':
            osint_email_search()
        elif ch == '4':
            osint_license_plate_search()
        elif ch == '5':
            osint_vin_search()
        elif ch == '6':
            osint_username_search()
        elif ch == '7':
            exit()
        elif ch.lower() in ['exit', 'quit']:
            exit()

def osint_name_search():
    n = input("Enter Name (ex: michael-scott): ")
    s = input("Enter State Initials (ex: ny): ")
    c = input("Enter City (ex: scranton): ")
    webbrowser.open(f'https://www.fastpeoplesearch.com/name/{n}_{c}-{s}')
    webbrowser.open(f'https://www.searchpeoplefree.com/find/{n}/{s}/{c}')
    webbrowser.open(f'https://www.peoplesearchnow.com/person/{n}_{c}_{s}')

def osint_phone_search():
    phone_number = input("Input phone number with country code: ")
    print("What type of tool would you like to use")
    print("1. Phone number info")
    print("2. Web Scrape for info")
    print("3. Go back")
    choice = input("Which tool: ")
    
    if choice == "1":
        phone_info = get_phone_info(phone_number)
        summarize_phone_info(phone_info, phone_number)
    elif choice == "2":
        web_scrape_phone_number(phone_number)
    elif choice == "3":
        main()

def get_phone_info(phone_number):
    info = {}
    try:
        # NumVerify API for basic info
        numverify_response = requests.get(f"http://apilayer.net/api/validate?access_key={numverify_api_key}&number={phone_number}&country_code=&format=1")
        numverify_response.raise_for_status()
        numverify_data = numverify_response.json()
        info['country'] = numverify_data.get('country_name')
        info['location'] = numverify_data.get('location')
        info['carrier'] = numverify_data.get('carrier')
        info['line_type'] = numverify_data.get('line_type')
    except Exception as e:
        print(f"Error fetching from NumVerify: {e}")
    
    try:
        # Twilio API for detailed info
        twilio_response = client.lookups.v1.phone_numbers(phone_number).fetch(type=['carrier', 'caller-name'])
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
    url = f"https://html.duckduckgo.com/html/?q={phone_number}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    summaries = soup.find_all('a', class_='result__a', limit=30)
    return [summary.get_text() for summary in summaries]

def run_phoneinfoga(phone_number):
    try:
        result = os.system(f"phoneinfoga scan -n {phone_number}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"PhoneInfoga command failed with error: {e}")
    return None

def summarize_phone_info(phone_info, phone_number):
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

def web_scrape_phone_number(phone_number):
    print("Looking on the web for information regarding that Phone Number")
    webbrowser.open(f'https://www.fastpeoplesearch.com/{phone_number}')
    webbrowser.open(f'https://www.searchpeoplefree.com/phone-lookup/{phone_number}')
    webbrowser.open(f'https://www.peoplesearchnow.com/phone/{phone_number}')
    webbrowser.open(f'https://www.whitepages.com/phone/1-{phone_number}')
    webbrowser.open(f'https://www.thatsthem.com/phone/{phone_number}')

def osint_email_search():
    em = input("Enter email: ")
    webbrowser.open(f'https://www.skymem.info/srch?q={em}&ss=home')
    webbrowser.open(f'https://www.melissa.com/v2/lookups/emailcheck/email/?email={em}&site=')

def osint_license_plate_search():
    plate = input("Enter license plate: ")
    state = input("Enter state: ")
    webbrowser.open(f'https://www.faxvin.com/license-plate-lookup/result?plate={plate}&state={state}')
    webbrowser.open(f'https://www.findbyplate.com/US/{state}/{plate}/')

def osint_vin_search():
    vin = input("Enter VIN: ")
    webbrowser.open(f'https://www.vehiclehistory.com/vin-report/{vin}')
    webbrowser.open(f'https://www.vindecoderz.com/EN/check-lookup/{vin}')

def osint_username_search():
    print("Choose a option to use to search about a username")
    print("1. Scrape info about username from websites")
    print("2. Use whatsmyname.app to find information about a username")
    usernamesearchoptionchoice = input("What option would you like to use:")

    if usernamesearchoptionchoice == '1':
        username = input("The username you want to find: ")
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
        webbrowser.open('https://whatsmyname.app')
    
    
if __name__ == "__main__":
    main()
