#!/usr/bin/python

from __future__ import division
import pygame

pygame.init()

class Row:
  def __init__(self, elements, mode="even", padding=5, xmargin=0, ymargin=0, proportion=1, hard=False, height=-1, width=-1):
    self.proportion = proportion
    self.elements = elements
    self.mode = mode
    self.padding = padding
    self.xmargin = xmargin
    self.ymargin = ymargin
    self.hard = hard
    self.height = height
    self.width = width
    
  def draw(self, tl, br, screen):
    hardWidth = 0
    softElements = 0
    for i in self.elements:
      if i.hard:
        if i.width >= 0:
          hardWidth += i.width
      else:
        softElements += 1
    self.height = br[1] - tl[1]
    self.width = br[0] - tl[0]
    top = tl[1]+self.padding+self.ymargin
    bottom = br[1]-self.padding-self.ymargin
    fillWidth = self.width - self.xmargin*2 - hardWidth
    
    if self.mode == "even":
      elementWidth = fillWidth / softElements
      Xoffset = self.xmargin
      for i in range(len(self.elements)):
        left = tl[0]+Xoffset+self.padding
        if self.elements[i].hard:
          right = left+self.elements[i].width-self.padding
          Xoffset += self.elements[i].width
        else:
          right = left+elementWidth-self.padding
          Xoffset += elementWidth
        self.elements[i].draw((left, top), (right, bottom), screen)
        
    if self.mode == "proportional":
      Xoffset = self.xmargin
      for i in range(len(self.elements)):
        left = tl[0]+Xoffset+self.padding
        if self.elements[i].hard:
          right = left+self.elements[i].width-self.padding
          Xoffset += self.elements[i].width
        else:
          elementWidth = fillWidth * self.elements[i].proportion
          right = left+elementWidth-self.padding
          Xoffset += elementWidth
        self.elements[i].draw((left, top), (right, bottom), screen)
        
class Column:
  def __init__(self, elements, mode="even", padding=5, xmargin=0, ymargin=0, proportion=1, hard=False, height=-1, width=-1):
    self.proportion = proportion
    self.elements = elements
    self.mode = mode
    self.padding = padding
    self.xmargin = xmargin
    self.ymargin = ymargin
    self.hard = hard
    self.height = height
    self.width = width
    
  def draw(self, tl, br, screen):
    hardHeight = 0
    softElements = 0
    for i in self.elements:
      if i.hard:
        if i.height >= 0:
          hardHeight += i.height
      else:
        softElements += 1
    self.height = br[1] - tl[1]
    self.width = br[0] - tl[0]
    left = tl[0]+self.padding+self.xmargin
    right = br[0]-self.padding-self.xmargin
    fillHeight = self.height - self.ymargin*2 - hardHeight
    
    if self.mode == "even":
      elementHeight = fillHeight / len(self.elements)
      Yoffset = self.ymargin+self.padding
      for i in range(len(self.elements)):
        top = tl[1]+Yoffset+self.padding
        if self.elements[i].hard:
          bottom = top+self.elements[i].height-self.padding
          Yoffset += self.elements[i].height
        else:
          bottom = top+elementHeight-self.padding
          Yoffset += elementHeight
        self.elements[i].draw((left, top), (right, bottom), screen)
        
    if self.mode == "proportional":
      Yoffset = self.xmargin
      for i in range(len(self.elements)):
        top = tl[1]+Yoffset+self.padding
        if self.elements[i].hard:
          bottom = top+self.elements[i].height-self.padding
          Yoffset += self.elements[i].height
        else:
          elementHeight = fillHeight * self.elements[i].proportion
          bottom = top+elementHeight-self.padding
          Yoffset += elementHeight
        self.elements[i].draw((left, top), (right, bottom), screen)
     
class BoxStack:
  def __init__(self, content, proportion=1, padding=0, hard=False, height=-1, width=-1):
    self.content = content
    self.proportion = proportion
    self.padding = padding
    self.hard = hard
    self.height = height
    self.width = width
  
  def draw(self, tl, br, screen):
    surface = pygame.Surface((br[0]-tl[0], br[1]-tl[1]))
    for i in self.content:
      i.draw((0,0), (br[0]-tl[0], br[1]-tl[1]), surface)
    screen.blit(surface, tl)

class Box:
  def __init__(self, content, proportion=1, xpadding=0, ypadding=0, xposition="left", yposition="top", color=(255,255,255), padding=0, hard=False, height=-1, width=-1):
    self.proportion = proportion
    self.xpadding = xpadding
    self.ypadding = ypadding
    if padding:
      self.xpadding=padding
      self.ypadding=padding
    self.padding = padding
    self.content = content
    self.xposition = xposition
    self.yposition = yposition
    self.color = color
    self.hard = hard
    self.height = height
    self.width = width
    
  def draw(self, tl, br, screen):
    if self.content['type'] == 'image':
      rect = pygame.image.load(self.content['path']).convert_alpha()
      if self.height > 0:
        width = int(rect.get_width()/(rect.get_height()/self.height))
        rect = pygame.transform.smoothscale(rect, (width, self.height))
      elif self.width > 0:
        height = int(rect.get_height()/(rect.get_width()/self.width))
        rect = pygame.transform.smoothscale(rect, (self.width, height))
      elif self.width > 0 and self.height > 0:
        rect = pygame.transform.smoothscale(rect, (self.width, self.height))
    elif self.content['type'] == 'text':
      rect = self.content['font'].render(self.content['text'], 0, self.color)
    elif self.content['type'] == 'rectangle':
      rect = pygame.Surface((br[0]-tl[0]-self.xpadding, br[1]-tl[1]-self.ypadding))
      rect.fill(self.color)
    elif self.content['type'] == 'rect':
      rect = self.content['rect']
    elif self.content['type'] == 'circle':
      r = self.content['radius']
      rect = pygame.Surface((r*2, r*2))
      pygame.draw.circle(rect, self.color, (r, r), r)
      
    if self.xposition == "left":
      x = tl[0]
    elif self.xposition == "center":
      x = br[0]-(((br[0]-tl[0])-rect.get_width())/2+rect.get_width())
    elif self.xposition == "right":
      x = br[0]-rect.get_width()
      
    if self.yposition == "top":
      y = tl[1]
    elif self.yposition == "center":
      y = br[1]-(((br[1]-tl[1])-rect.get_height())/2+rect.get_height())
    elif self.yposition == "bottom":
      y = br[1]-rect.get_height()
    screen.blit(rect, (x,y))