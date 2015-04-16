#! /usr/bin/env python

import os, time, sys, string, random, pygame, pygame.font, pygame.mixer, json
from pygame.locals import *
from pprint import pprint

class Challenge_Selector:
  def __init__(self, consoles, challenges):
    self.__dict__.update(config)
    pygame.init()
    self.screen = pygame.display.set_mode((1024,768), HWSURFACE|DOUBLEBUF|FULLSCREEN)
    self.tinyfont = pygame.font.SysFont("Monospace", 16)
    self.lilfont = pygame.font.SysFont("Monospace", 15)
    self.medfont = pygame.font.SysFont("Monospace", 20)
    self.bigfont = pygame.font.SysFont("Monospace", 28)

    self.box = pygame.surface.Surface((640,50))
    self.box.fill((50,50,50))

    # Positional constants
    self.X_MARGIN = 12
    self.Y_BANNER_PADDING = 2
    
    # Create banner surface
    self.banner = pygame.image.load( self.image_folder + "core/M12_Challenges_Banner.jpg").convert_alpha()
    self.banner_rect = self.banner.get_rect()
    self.banner_rect.center = ((512, 115))

    # Create challenge list surfaces
    self.tabbak = pygame.Surface((1000, 32), HWSURFACE)
    self.tabbak.fill((200, 152, 88))
    
    self.tabs = []    
    for i in self.consoles:
      self.tabs.append(pygame.image.load(i.image).convert_alpha())
    
    self.tabsEn = []
    for i in self.consoles:
      self.tabsEn.append(pygame.image.load(i.enimage).convert_alpha())
    
    # Create difficulty surfaces
    self.normDiff = self.bigfont.render("NORMAL", 0, (255, 255, 255))
    self.hardDiff = self.bigfont.render("HARD", 0, (255, 255, 255))
    self.expertDiff = self.bigfont.render("EXPERT", 0, (255, 255, 255))
    self.unfairDiff = self.bigfont.render("UNFAIR", 0, (255, 255, 255))
    
    # Create instruction surfaces
    self.instructbak = pygame.Surface((self.screen.get_width(), 30))
    self.instructbak.fill((128, 128, 128))
    
    self.instruct = self.tinyfont.render("UP or DOWN to select a game | LEFT or RIGHT to change tabs | ENTER or a button to play", 0, (255,255,255), (128, 128, 128))
    self.instruct_rect = self.instruct.get_rect()
    self.instruct_rect.center = ((self.screen.get_width()/2, self.screen.get_height() - 20))
    
  def get_challenge(self):
    pygame.event.set_blocked(MOUSEMOTION)
    pygame.display.set_caption('MAGFEST12 Challenges: ZeldAdventure Time')
    pygame.mouse.set_visible(0)
    
    while True:
      self.screen.fill((0,0,0))

      # Add challenges booth banner
      self.screen.blit(self.banner, self.banner_rect)
      
      offsetX = self.X_MARGIN
      for i in range(0, len(self.tabs)):
        if i == self.whichTab:
          self.screen.blit(self.tabsEn[i], (offsetX, self.banner.get_height() + self.Y_BANNER_PADDING))
        else:
          self.screen.blit(self.tabs[i], (offsetX, self.banner.get_height() + self.Y_BANNER_PADDING))
        
        offsetX += 2 + self.tabs[i].get_width()
        
      # Add games from selected tab list
      offsetY = 40
      count = 0
      
      # Fill 13 veritcal text boxes with games from current list
      x = -6
      count = 0
      while(1):
        i = self.whichRom[self.whichTab] + x
        if (i >= 0) and (i < len(self.tabList[self.whichTab])):
          if x == 0:
            fontColor = ((255, 255, 255))
          else:
            fontColor = ((160 - abs(x)*10), (160 - abs(x)*10), (160 - abs(x)*10))
        
          text = self.lilfont.render(self.tabList[self.whichTab][i]["readableName"], 0, fontColor)
          self.screen.blit(text, (self.X_MARGIN, (self.banner.get_height() + self.Y_BANNER_PADDING + self.tabbak.get_height() + self.Y_BANNER_PADDING) + offsetY))
          offsetY += 30
          count += 1
          
        x += 1
        
        if (count >= 13) or (i >= len(self.tabList[self.whichTab])):
          break;

      # Create screen shot container
      self.screen_container = pygame.Surface((self.screen.get_width() - 437, 450))
      if self.tablist[self.whichTab][self.whichRom[self.whichTab]]["difficulty"] == "HARD":
        self.screen_container.fill((105, 105, 255))
      elif self.tablist[self.whichTab][self.whichRom[self.whichTab]]["difficulty"] == "EXPERT":
        self.screen_container.fill((255, 97, 97))
      elif self.tablist[self.whichTab][self.whichRom[self.whichTab]]["difficulty"] == "UNFAIR":
        self.screen_container.fill((255, 97, 255))
      else:
        self.screen_container.fill((100, 204, 100))
      self.screen.blit(self.screen_container, (425, (self.banner.get_height() + self.Y_BANNER_PADDING + tabbak.get_height() + self.Y_BANNER_PADDING + 20)))

      # Add screenshot for selected game
      gamePic = pygame.image.load( self.image_folder + self.tablist[self.whichTab][self.whichRom[self.whichTab]]["system"] + "/" + self.tablist[self.whichTab][self.whichRom[self.whichTab]]["imageFile"]).convert_alpha()
      gamePicborder = pygame.Surface((gamePic.get_width() + 4, gamePic.get_height() + 4))
      gamePicborder.fill((0, 0, 0))
      self.screen.blit(gamePicborder, (425 + (self.screen_container.get_width() / 2) - (gamePic.get_width() / 2), (self.banner.get_height() + self.Y_BANNER_PADDING + tabbak.get_height() + self.Y_BANNER_PADDING + 25)))
      self.screen.blit(gamePic, (425 + (self.screen_container.get_width() / 2) - (gamePic.get_width() / 2) + 2, (self.banner.get_height() + self.Y_BANNER_PADDING + tabbak.get_height() + self.Y_BANNER_PADDING + 25 + 2)))
      
      # Add challenge difficulty
      pygame.draw.line(self.screen, (255, 255, 255), (450, (self.banner.get_height() + self.Y_BANNER_PADDING + tabbak.get_height() + self.Y_BANNER_PADDING + 260)), (986, (self.banner.get_height() + self.Y_BANNER_PADDING + tabbak.get_height() + self.Y_BANNER_PADDING + 260)), 2)
      if self.tablist[self.whichTab][self.whichRom[self.whichTab]]["difficulty"] == "HARD":
        self.screen.blit(hardDiff, ((425 + (self.screen_container.get_width() / 2) - (hardDiff.get_width() / 2)), (self.banner.get_height() + self.Y_BANNER_PADDING + tabbak.get_height() + self.Y_BANNER_PADDING + 265)))
      elif self.tablist[self.whichTab][self.whichRom[self.whichTab]]["difficulty"] == "EXPERT":
        self.screen.blit(expertDiff, ((425 + (self.screen_container.get_width() / 2) - (expertDiff.get_width() / 2)), (self.banner.get_height() + self.Y_BANNER_PADDING + tabbak.get_height() + self.Y_BANNER_PADDING + 265)))
      elif self.tablist[self.whichTab][self.whichRom[self.whichTab]]["difficulty"] == "UNFAIR":
        self.screen.blit(unfairDiff, ((425 + (self.screen_container.get_width() / 2) - (unfairDiff.get_width() / 2)), (self.banner.get_height() + self.Y_BANNER_PADDING + tabbak.get_height() + self.Y_BANNER_PADDING + 265)))
      else:
        self.screen.blit(normDiff, ((425 + (self.screen_container.get_width() / 2) - (normDiff.get_width() / 2)), (self.banner.get_height() + self.Y_BANNER_PADDING + tabbak.get_height() + self.Y_BANNER_PADDING + 265)))
      pygame.draw.line(self.screen, (255, 255, 255), (450, (self.banner.get_height() + self.Y_BANNER_PADDING + tabbak.get_height() + self.Y_BANNER_PADDING + 300)), (986, (self.banner.get_height() + self.Y_BANNER_PADDING + tabbak.get_height() + self.Y_BANNER_PADDING + 300)), 2)

      # Add challenge descriptions
      wholeDesc = self.tablist[self.whichTab][self.whichRom[self.whichTab]]["description"]
      descLines = wholeDesc.split("NEWLINE")
      
      offsetX = 425 + (self.screen_container.get_width() / 2)
      offsetY = (self.banner.get_height() + self.Y_BANNER_PADDING + tabbak.get_height() + self.Y_BANNER_PADDING + 325)
      for i in descLines:
        line = lilfont.render(i, 0, (255, 255, 255))
        self.screen.blit(line, (offsetX - (line.get_width() / 2), offsetY))
        offsetY += 25
      
      # Add instructions
      self.screen.blit(instructbak, (0, self.screen.get_height() - 30))
      self.screen.blit(instruct, instruct_rect)

      # Refresh self.screen
      pygame.display.flip()

      # Wait for input
      event = pygame.event.wait()
      curRom = self.tablist[self.whichTab][self.whichRom[self.whichTab]]
      if event.type == KEYDOWN:
        if event.key == K_UP:
          if self.whichRom[self.whichTab] > 0:
            self.whichRom[self.whichTab] -= 1
        elif event.key == K_DOWN:
          if self.whichRom[self.whichTab] < (len(self.tablist[self.whichTab]) - 1):
            self.whichRom[self.whichTab] += 1
        elif event.key == K_RIGHT:
          if self.whichTab < (len(self.tablist) - 1):
            self.whichTab += 1
        elif event.key == K_LEFT:
          if self.whichTab > 0:
            self.whichTab -= 1
        elif event.key == K_RETURN:          
          pygame.display.quit()
          return curRom
