import ConfigParser
import os
import re

def getConf(configFile):
  images = {}
  config = ConfigParser.ConfigParser()
  if not(os.path.isfile(configFile)):
    sys.exit("The config file "+configFile+" is not a file. That is unfortunate.")
  if config.read(configFile):
    sections = {}
    for i in config.sections():
      sections[i] = config.items(i)
  else:
    sys.exit("Config File is not valid.")
  if "main" in sections.keys():
    options = {}
    for i in sections["main"]:
      options[i[0]] = i[1]
  else:
    options = None
    print "No global options found. Strange. I might explode."
  for i in sections.keys():
    if not i == "main":
      images[i] = {}
      for j in sections[i]:
        images[i][j[0]] = j[1]
      if not "section" in images[i].keys():
        images[i]["section"] = i
  if options:
    options = replaceKeys(options, {})
  images = [replaceKeys(images[x], options) for x in images]
  return images, options
  
def replaceKeys(image, main):
  if main:
    for i in main.keys():
      if not i in image.keys():
        image[i] = main[i]
  madeProgress = True
  keysWithSubs = remainingSubs(image)
  while keysWithSubs and madeProgress:
    madeProgress = False
    for j in keysWithSubs.keys():
      if not any(map(lambda x: x in keysWithSubs.keys(), keysWithSubs[j])):
        for k in keysWithSubs[j]:
          if k in image.keys():
            image[j] = re.sub("<"+k+">", image[k], image[j])
            madeProgress = True
    keysWithSubs = remainingSubs(image)
  return image

def remainingSubs(image):
  keysWithSubs = {}
  for i in image.keys():
    if re.findall(".*<(.+?)>.*", image[i]):
      keysWithSubs[i] = re.findall(".*<(.+?)>.*", image[i])
  return keysWithSubs