class Console:
  def __init__(self, config):
    self.__dict__.update(config)
    self.challenges = []