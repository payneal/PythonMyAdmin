import copy
import curses
import math
import textwrap
import string

class CurseTextbox(object):
    """description of class"""
    def __init__(self, **kwargs):
        self.height = kwargs["h"]
        self.width = kwargs["w"]
        self.y = kwargs["y"]        #   Y RELATIVE TO PARENT WINDOW
        self.x = kwargs["x"]        #   X RELATIVE TO PARENT WINDOW

        self.linetext = []
        
        self.totalheight = 0
        self.pageheight = 0
        self.pages = 0
        self.currentpg = 0
        self.index = 0
        self.morecontent = False

        self.style = kwargs["style"]

    #
    def update(self, refresh=False):
        self.drawtext()
        if refresh == True:
            self.parent.win.refresh()

    def load(self, parent, basetext="", centertxt=False):
        self.onload(parent, basetext, centertxt)

    #       onload
    def onload(self, parent, basetext, centertxt):
        self.parent = parent
        self.defaulttext = copy.copy(basetext)
        self.centertext = centertxt
        self.resettext(basetext)

    def resettext(self, text):
        self.index = 0
        self.currentpg = 0
        self.cleartext()
        self.basetext = text
        if text == "":
            self.basetext = self.defaulttext
        #if self.basetext != "":
        self.texttolines(self.basetext)
        self.setpages()
        self.turnpage("prev")

    #       
    def texttolines(self, text):  
     
        if self.centertext == True:
            self.linetext = textwrap.wrap(text, self.width)
            for l in range (0, len(self.linetext)):
                self.linetext[l] = textwrap.dedent(
                    self.linetext[l]).center(self.width," ")
        else:
            wr = textwrap.TextWrapper(
                width=self.width,
                replace_whitespace=False,
                drop_whitespace=False)
            self.linetext = wr.wrap(text)    
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
        txt_atrclr = self.style.txt_atr | self.style.txt_clr
        self.parent.win.attron(txt_atrclr)
        self.cleartext()       

        for l in range(0, self.height):
            if l + self.index >= len(self.linetext):
                break

            self.parent.win.addstr(self.y + l, self.x, 
                self.linetext[self.index + l], txt_atrclr)

            # draw line
            #ln = copy.copy(self.linetext[self.index + l])
            #if self.centertext == True:
            #    ln.center(self.width)
            #self.parent.win.addstr(self.y + l, self.x, 
            #    ln, txt_atrclr)
            #ln = None
                 
        if self.morecontent == True:
            self.parent.win.addstr(
                self.y + self.height, self.x, "(MORE...)", txt_atrclr)

        self.parent.win.attroff(txt_atrclr)      
        
    def cleartext(self):
        bg_chtype = self.parent.win.getbkgd()
        #self.parent.win.refresh()
        for l in range(0, self.height):
            self.parent.win.hline(self.y + l, self.x, 32, self.width)
            #self.parent.win.hline(self.y + l, self.x, bg_chtype, self.width)