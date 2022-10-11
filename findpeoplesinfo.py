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
parser = ArgumentParser()
parser.add_argument("username",type=str,nargs='?')
args = parser.parse_args()
r = "\033[31m"
g = "\033[32m"
y = "\033[33m"
b='\33[36m'
p = "\033[35m"


from importlib import import_module
SocialAnalyzer = import_module("social-analyzer").SocialAnalyzer(silent=True)
results = SocialAnalyzer.run_as_object(username = "", websites="youtube pinterest tumblr", metadata=True, extract=True, silent=False)

print("")
print("")
print("Welcome to people finder")
print("")
print("Made by BJW333")
print("")
print("Start [1]")
print("Quit [99]")

starttool = input('Your choice here: ')
if starttool == "1":
    print('Starting Tool')
    time.sleep(2)

print("Please enter the username you would like to search")
u2 = input("The username you want to find: ")

#def scanner(u2)
social={
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
print(f"\n{p}starting:\n")
spece=" "*20
print(f"{g}#"*126)
print(f"{g}# {r}SOCIAL MEDIA   {g}|        {r}USER {g}        | {r}STATUS CODE{g} | {r}                   URL   {g}      {spece}                   #")
for i,j in social.items():
  try:
   req = get(j)
   code=req.status_code
  except exceptions.TooManyRedirects:
   print("TooManyRedirects")
   break
  except exceptions.ConnectionError:
   print("\n\nConnectionError!\n\ncheck your internet connection!\n\n")
   break
  except exceptions.Timeout: 
   continue
  print(f"{g}#"+f"{p}-"*124+f"{g}#")
  if code==200:
   user=f"{g}|{y}        Found        "
  elif code==404:
   user=f"{g}|{r}      Not Found      "
  else:
   user=f"{g}|{b}undefined status code"
   j="none"
  media=f"{g}# {y}"+i+" "*(15-len(i))
  code=f"{g}|     {y}"+str(code)+" "*5
  url=f"{g}|{y} "+j+" "*(70-len(j))+f"{g}#"
  print(media+user+code+url)
print("#"*126)
print(f"{y}{g}\n")
if starttool == "99":
        time.sleep(1)
        print("Shuting Down")
        exit()



#os.system("social-analyzer --username " + ( username1 ) + " --metadata --top 50")
#time.sleep(10)



print("Want to find some elses phone number info: ")
print("""Start finding someone again
To phone number searcher [1]
Quit [99] """)

startagain = input('Your choice here: ')
    
if startagain == "1":
    print("Would you like to search a phone number")
    phonenum2 = input("Phone number you would like to get info on include the country code 1 = USA: ")
    os.system("./phoneinfoga scan -n " + ( phonenum2 ))
    
if startagain == "99":
        time.sleep(1)
        print("Shuting Down")
        exit()


