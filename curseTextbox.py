﻿import math
import textwrap
import curses
import cursePanel

class CurseTextbox(object):
    """description of class"""
    def __init__(self, **kwargs):
        self.height = kwargs["h"]
        self.width = kwargs["w"]
        self.y = kwargs["y"]
        self.x = kwargs["x"]                

        #self.parindex = kwargs["parindex"]
        #self.parent = kwargs["parent"]
        #self.basetext = kwargs["basetext"]
        self.linetext = []

        self.totalheight = 0
        self.pageheight = 0
        self.pages = 0
        self.currentpg = 0
        self.index = 0
        self.morecontent = False

        self.style = kwargs["style"]

        #self.onload( kwargs["panels"] )

    def load(self, parent, basetext=""):
        self.onload(parent, basetext)

    #       onload
    def onload(self, parent, basetext):
        self.parent = parent
        #self.basetext = basetext
        self.resettext(basetext)#self.basetext)

    def resettext(self, text):
        self.index = 0
        self.currentpg = 0
        self.cleartext()
        self.basetext = text
        if self.basetext != "":
            self.texttolines(self.basetext)
            self.setpages()
            self.turnpage("prev")

    #       
    def texttolines(self, text):             
        self.linetext = textwrap.wrap(text, int(self.width))

    #
    def setpages(self):
        self.totalheight = len(self.linetext)
        self.pages = self.totalheight / self.height
        if self.totalheight % self.height != 0:
            self.pages += 1
        if self.pages > 1:
            self.morecontent = True
     
    #
    def turnpage(self, direction):
        if direction == "next":         
            if self.index + self.height < self.totalheight :
                self.index += self.height
                self.currentpg += 1
            if self.currentpg + 1 == self.pages:
                self.morecontent = False
            else:
                self.morecontent = True
        elif direction == "prev":
            if self.index - self.height >= 0:
                self.index -= self.height
                self.currentpg -= 1
            if self.pages > 1:
                self.morecontent = True

    #
    def drawtext(self):
        self.cleartext()
        txt_atrclr = self.style.txt_atr | self.style.txt_clr
        bg_chtype = self.parent.win.getbkgd()
        self.parent.win.attron(txt_atrclr)
        for l in range(0, self.height):
            # clear lines past last line if we're on last page
            if l + self.index >= len(self.linetext):
                break
            # draw line
            self.parent.win.addstr(self.y + l, self.x, 
                self.linetext[self.index + l], txt_atrclr)
                 
        if self.morecontent == True:
            self.parent.win.addstr(
                self.y + self.height, self.x, "(MORE...)", txt_atrclr)
        self.parent.win.attroff(txt_atrclr)      
        
    def cleartext(self):
        bg_chtype = self.parent.win.getbkgd()
        self.parent.win.refresh()
        for l in range(0, self.height):
            self.parent.win.hline(self.y + l, self.x, bg_chtype, self.width)