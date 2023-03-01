# development halted, repl project terminated and progress was lost
<a name="readme-top"></a>
<br />
<div align="center">
  <a href="https://github.com/cloudcant/pyCNC/">
    <img src="https://user-images.githubusercontent.com/66269103/220436048-cf5c617b-3f09-40f7-bc10-dd055e60b520.png" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">Fcnc</h3>

  <p align="center">
    A command and controlserver writen in python3 using the Flask module. <a href="https://replit.com/@cloudcant/fcnc">Live Demo</a>
    <br />
  </p>
</div>
 <br />
 
![the gamer](https://user-images.githubusercontent.com/66269103/221206842-92389c30-819f-4c96-ba9b-e920551eee1d.png)

## Getting Started

This is developed and tested on unix so for best luck run this on a repl or a unix enviorment

### Prerequisites

To run the flask server you need to install the flask module: 
  ```sh
  pip3/pip install flask
  ```

### Installation


1. Clone the repo
   ```sh
   git clone https://github.com/cloudcant/fcnc.git
   ```
2. Set server settings in ```main.py``` (for repl deployment keep settings the same)

    ![image](https://user-images.githubusercontent.com/66269103/220188881-6eec179c-4ee9-4041-9679-30da36a05abd.png)

4. start the cnc server
   ```sh
   python3 main.py 
   ```
5. All done! :)

## Usage

usage here


<!-- ROADMAP -->
## Roadmap

- [X] Login Page
  - [ ] User
  - [X] Pass
  - [X] Encryption
  - [X] Sessions
  
- [x] Panel
  - [X] sending commands
  - [X] toggle bots button
  - [X] auto scroll output
  - [X] better style in general
  - [X] command type dropdown
  - [ ] authenticated command setting
  - [ ] seperate dos inputs
  - [ ] users
  - [ ] bot output 
  
- [X] Bot
  - [X] Encryption of commands
  - [X] Better encryption of commands (fernet)
  - [X] RCE
  - [ ] Denial of service
    - [ ] diffrent methods
  - [ ] bot outputs
  
- [ ] Telnet connection

## Acknowledgments

This was made for fun. I am not responsable for whatever you may do with this project.

