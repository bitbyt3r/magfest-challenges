#!/usr/bin/python2

import os
from subprocess import Popen
import threading
import Challenge_Selector2 as Challenge_Selector
import json
import configReader
import Challenge
import Console
import time
import shutil

HOME = "/home/mark"
EVROUTER_RC = HOME+"/.evrouterrc"

KEYCODES = {  "select":"minus underscore minus underscore",
              "start":"equal plus equal plus",
              "left":"Left NoSymbol Left",
              "right":"Right NoSymbol Right",
              "up":"Up NoSymbol Up",
              "down":"Down NoSymbol Down",
              "L":"bracketleft braceleft bracketleft braceleft",
              "R":"bracketright braceright bracketright braceright",
              "x":"x X x X",
              "y":"y Y y Y",
              "a":"a A a A",
              "b":"b B b B" }

os.system("xmodmap -pke > "+HOME+"/.Xmodmap.orig")

with open("./roms.conf", "r") as romconf:
  roms_conf = json.loads(romconf.read())
challenges = [Challenge.Challenge(x) for x in roms_conf]

consoles_conf, global_conf = configReader.getConf("./consoles.conf")
consoles = [Console.Console(x) for x in consoles_conf]
for i in consoles:
  for j in challenges:
    if i.section == j.system:
      i.challenges.append(j)
      j.console = i
  i.selected = i.challenges[0]

challenge_selector = Challenge_Selector.Challenge_Selector(consoles, global_conf)

while(1):
    # Get the game from the menu
    console, challenge = challenge_selector.get_challenge()
    print("Selected console", console.name)
    print("Selected challenge", challenge.readableName)
    
    # Generate the evrouter file
    with open(EVROUTER_RC, "w") as evrouter_config:
      evrouter_config.write(challenge.generate_evrouter())
    
    # Launch key rebinding
    if os.path.isfile("/tmp/.evrouter:0.0"):
      os.system("evrouter -q")
      os.system("rm -f /tmp/.evrouter:0.0")
    os.system('evrouter -c ~/.evrouterrc /dev/input/*')
    
    # Lauch Xmodmap
    newmodmap = ""
    with open(HOME+"/.Xmodmap.orig", "r") as origmodmap:
      for line in origmodmap.readlines():
        for key in challenge.disabledKeys:
          if not key in line:
            newmodmap += line
    with open(HOME+"/.Xmodmap", "w") as newmodmapfile:
      newmodmapfile.write(newmodmap)
    os.system("xmodmap "+HOME+"/.Xmodmap")
    
    # Copy Save file
    if not os.path.isdir(console.save_destination):
      os.makedirs(console.save_destination)
    shutil.copy(challenge.save_path, console.save_destination)
    
    # Copy Config file
    if os.path.isdir(console.config_destination):
      os.rmdir(console.config_destination)
    shutil.copytree(console.config_source, console.config_destination)
    
    # Print a helpful message
    Popen(['sleep 4 ; notify-send "' + console.notify_text + '"'], shell=True)
    
    # Launch the game
    print("Launching "+challenge.readableName)
    print('Command: '+challenge.launch_cmd())
    os.system(challenge.launch_cmd())
    
    # kill key rebinding  
    os.system("evrouter -q")
    
    # Repair Xmodmap
    os.system("xmodmap "+HOME+"/.Xmodmap.orig")
    