class Challenge:
  def __init__(self, config):
    self.__dict__.update(config)
    self.image_path = "./images/"+self.system+"/"+self.imageFile
    self.rom_path = "./roms/"+self.system+"/"+self.romFile
    self.save_path = "./saves/"+self.system+"/"+self.saveFile
    self.description = self.description.split("NEWLINE")
    self.console = None
  
  def generate_evrouter(self):
    string = ""
    string += 'Window ""\n'
    string += self.console.evrouter_load + "\n"
    string += self.console.evrouter_kill + "\n"
    string += self.console.evrouter_exit + "\n"
    return string
  
  def launch_cmd(self):
    cmd = self.console.command + " "
    cmd += " ".join(self.console.arguments)
    cmd += " "+self.rom_path
    return cmd
  
  def __repr__(self):
    return self.readableName