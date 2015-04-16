import pygame
from Gui import Box, Column, Row, BoxStack
import time
import os

class Challenge_Selector:
  def __init__(self, consoles, config):
    self.consoles = consoles
    self.config = config
    self.selectedconsole = 0
    pygame.init()
    for i in self.consoles:
      i.index = 0
    
  def get_challenge(self):
    self.screen = pygame.display.set_mode((0,0), pygame.RESIZABLE)
    self.width = self.screen.get_width()
    self.height = self.screen.get_height()
    self.draw()
    speak = False
    refresh = True
    while True:
      if refresh:
        self.draw()
        refresh=False
      for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
          refresh=True
          self.width, self.height = event.size
        if event.type == pygame.KEYDOWN:
          refresh = True
          speak = True
          if event.key == pygame.K_UP:
            self.consoles[self.selectedconsole].index -= 1
            if self.consoles[self.selectedconsole].index < 0:
              self.consoles[self.selectedconsole].index = 0
          elif event.key == pygame.K_DOWN:
            self.consoles[self.selectedconsole].index += 1
            if self.consoles[self.selectedconsole].index >= len(self.consoles[self.selectedconsole].challenges):
              self.consoles[self.selectedconsole].index = len(self.consoles[self.selectedconsole].challenges) - 1
          elif event.key == pygame.K_RIGHT:
            self.selectedconsole += 1
            if self.selectedconsole >= len(self.consoles):
              self.selectedconsole = len(self.consoles) - 1
          elif event.key == pygame.K_LEFT:
            self.selectedconsole -= 1
            if self.selectedconsole < 0:
              self.selectedconsole = 0
          elif event.key == pygame.K_RETURN: 
            pygame.display.quit()
            return self.consoles[self.selectedconsole], self.consoles[self.selectedconsole].challenges[self.consoles[self.selectedconsole].index]
      self.screen.fill((0,0,0))
  def draw(self):
    wideBox = Box({'type':'rectangle'}, yposition='center', color=(0,0,255), ypadding=16)
    tallBox = Box({'type':'rectangle'}, xposition='center', color=(0,0,255), xpadding=16)
    c1 = Box({'type':'circle', 'radius':8}, yposition='top', xposition='left', color=(0,0,255))
    c2 = Box({'type':'circle', 'radius':8}, yposition='top', xposition='right', color=(0,0,255))
    c3 = Box({'type':'circle', 'radius':8}, yposition='bottom', xposition='left', color=(0,0,255))
    c4 = Box({'type':'circle', 'radius':8}, yposition='bottom', xposition='right', color=(0,0,255))
    blueBox = BoxStack([c1, c2, c3, c4, tallBox, wideBox])
    for i in self.consoles:
      consoleFont = pygame.font.SysFont("Monospace", 20)
      label = Box({'type':'text', 'text':i.name, 'font':consoleFont}, yposition='center', xposition="center", padding=5)
      if i == self.consoles[self.selectedconsole]:
        consoleFont = pygame.font.SysFont("Monospace", 22)
        label = Box({'type':'text', 'text':i.name, 'font':consoleFont}, yposition='center', xposition="center", padding=5, color=(255,0,0))
      i.tab = BoxStack([blueBox, label])
      
    listFont = pygame.font.SysFont("Monospace", 16)
    difficultyFont = pygame.font.SysFont("Monospace", 24)
    descriptionFont = pygame.font.SysFont("Monospace", 18)
    for i in self.consoles[self.selectedconsole].challenges:
      if i == self.consoles[self.selectedconsole].challenges[self.consoles[self.selectedconsole].index]:
        i.listItem = Box({'type':'text', 'text':i.readableName, 'font':listFont}, yposition='center', xposition='left', padding=5, color=(255,255,0))
      else:
        i.listItem = Box({'type':'text', 'text':i.readableName, 'font':listFont}, yposition='center', xposition='left', padding=5, color=(255,255,255))
      i.image = Box({'type':'image', 'path':i.image_path}, yposition='center', xposition='center', hard=True, height=360, width=480)
      i.difficultyBox = Box({'type':'text', 'text':i.difficulty, 'font':difficultyFont}, xposition='center')
      descriptionLines = []
      for j in i.description:
        descriptionLines.append(Box({'type':'text', 'text':j, 'font':descriptionFont}, hard=True, height=25))
      i.descriptionBox = Column(descriptionLines)
    
    banner = Box({'type':'image', 'path':self.config['banner_path']}, xposition='center', height=224, hard=True)
    tabrow = Row([x.tab for x in self.consoles], hard=True, height=50, padding=5)
    challengeList = Column([x.listItem for x in self.consoles[self.selectedconsole].challenges])
    challengeListBox = BoxStack([blueBox, challengeList])
    curr = self.consoles[self.selectedconsole].challenges[self.consoles[self.selectedconsole].index]
    info = Column([curr.image, curr.difficultyBox, curr.descriptionBox])
    infoBox = BoxStack([blueBox, info])
    bottomRow = Row([challengeListBox, infoBox])
    
    page = Column([banner, tabrow, bottomRow], mode='proportional', padding=0)
  
    page.draw((0,0), (self.width, self.height), self.screen)
    pygame.display.flip()