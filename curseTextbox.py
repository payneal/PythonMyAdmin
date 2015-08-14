import copy
import curses
import math
import textwrap
import string

class CurseTextbox(object):
    """description of class"""
    def __init__(self, **kwargs):
        self.parent                 = kwargs["parent"]

        self.y                      = kwargs["size"][0]
        self.x                      = kwargs["size"][1]
        self.height                 = kwargs["size"][2]
        self.width                  = kwargs["size"][3]

        if "base_text" in kwargs:   self.base_text = kwargs["base_text"]
        else:                       self.base_text = ""
        
        self.line_text              = []

        self.total_height           = 0
        self.page_height            = 0
        self.pages                  = 0
        self.current_pg             = 0
        self.index                  = 0
        self.more_content           = False

        self.style                  = kwargs["style"]

        if "center" in kwargs:      self.center = kwargs["center"]
        else:                       self.center = False

        self.resetText()

    def load(self):
        if hasattr(self, "_on_load"):
            if self._on_load["action"] == "call_function":
                func = getattr(self, _on_load["action_name"])
                func(*_on_load["action_args"])

    def refresh(self, new_text=None):
        if new_text != None: self.resetText(new_text)
        self.drawText()
        self.parent.win.refresh()

    def drawText(self):
        """ draws textbox text to screen """
        txt_atrclr =          self.style.txt_atr | self.style.txt_clr

        self.parent.win.attron(txt_atrclr)
        self.clearText()       
        for l in range(0, self.height):
            if l + self.index >= len(self.line_text):           break
            self.parent.win.addstr(
                self.y + l,
                self.x, 
                self.line_text[self.index + l], 
                txt_atrclr)
        if self.more_content == True:
            self.parent.win.addstr(
                self.y + self.height, 
                self.x, 
                "(MORE...)", 
                txt_atrclr)
        self.parent.win.attroff(txt_atrclr)

        self.parent.changed = True

    def clearText(self):
        """ removes text from textbox on screen """
        bg_chtype = self.parent.win.getbkgd()
        for l in range(0, self.height):
            self.parent.win.hline(self.y + l, self.x, bg_chtype, self.width)

    def resetText(self, text=None):
        """ resets textbox data to base text or passed text"""
        if text == None:    text = self.base_text
        else:               self.base_text = copy.copy(text)

        self.index          = 0
        self.current_pg     = 0
        
        self.textToLines()
        self.setPages()
        self.turnPage("prev")
      
    def textToLines(self):
        if self.center == True:
            self.line_text = textwrap.wrap(self.base_text, self.width)
            for l in range (0, len(self.line_text)):
                self.line_text[l] = textwrap.dedent(
                        self.line_text[l]).center(self.width," ")
        else:
            wr = textwrap.TextWrapper(
                    width=self.width, 
                    replace_whitespace=False,
                    drop_whitespace=False)
            self.line_text = wr.wrap(self.base_text)    

    def setPages(self):
        self.total_height = len(self.line_text)
        self.pages        = self.total_height / self.height

        if self.total_height % self.height != 0 :               self.pages += 1
        if self.pages > 1 :                            self.more_content = True
     
    def turnPage(self, direction):
        if direction == "next":         
            if self.index + self.height < self.total_height :
                self.index += self.height
                self.current_pg += 1
            if self.current_pg + 1 == self.pages:      self.more_content = False
            else:                                       self.more_content = True
        elif direction == "prev":
            if self.index - self.height >= 0:
                self.index -= self.height
                self.current_pg -= 1
            if self.pages > 1:                          self.more_content = True