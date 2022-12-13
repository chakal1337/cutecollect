#!/usr/bin/python3
import sys
import requests
import argparse
import random
import string
import threading
import time
import urllib.parse
from bs4 import BeautifulSoup
import json

tlock = threading.Lock()

links_collected = []
threads = 10
extra = ""
bruteforce = 0
tor = 0
randomize = 0
debug = 0

parser = argparse.ArgumentParser()
parser.add_argument('keywords')
parser.add_argument('-t', '--threads')
parser.add_argument('-f', '--footprints-file')
parser.add_argument('-e', '--extra-word')
parser.add_argument('-b', '--bruteforce', action="store_true")
parser.add_argument('-r', '--randomize', action="store_true")
parser.add_argument('-z', '--tor', action="store_true")
args = parser.parse_args()

if args.tor:
 tor = 1

if args.randomize:
 randomize = 1

if args.bruteforce:
 bruteforce = 1

if args.threads:
 threads = int(args.threads)

if args.extra_word:
 extra = args.extra_word

footprints = [""]
if args.footprints_file:
 with open(args.footprints_file, "rb") as file:
  footprints.extend(file.read().decode().splitlines())

keywords = []
try:
 with open(args.keywords, "rb") as file:
  keywords = file.read().decode().splitlines()
except:
 keywords = [args.keywords]

def scrape(key_data):
 global links_collected
 data = {"q":key_data, "b":""}
 proxies = {}
 if tor == 1:
  proxies["http"] = "socks5h://127.0.0.1:9050"
  proxies["https"] = "socks5h://127.0.0.1:9050"
 headers = {
  "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
  "Content-Type":"application/x-www-form-urlencoded"
 }
 r = requests.post(url="https://html.duckduckgo.com/html/", data=data, headers=headers, proxies=proxies)
 soup = BeautifulSoup(r.text, "html.parser")
 for lnk in soup.find_all("a",{"class":"result__a"}):
  link = lnk.get("href")
  if link in links_collected: continue
  if not link.startswith("http"): continue
  with tlock: links_collected.append(link)
  if link and not link.startswith("https://duckduckgo.com"):
   print(link)

def _start():
 global keywords
 while len(keywords):
  with tlock: keyword = keywords.pop(0)
  for footprint in footprints:
   rep_arr = [""]
   if randomize == 1: rep_arr[0] = random.choice(string.ascii_lowercase)
   if bruteforce == 1: rep_arr = string.ascii_lowercase
   for brute in rep_arr:
    try:
     scrape("{} {} {} {}".format(keyword, footprint, extra, brute))
    except Exception as error:
     if debug == 1: print(error)

def main():
 for i in range(threads):
  t=threading.Thread(target=_start)
  t.start()

if __name__ == "__main__":
 main()
