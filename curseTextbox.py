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


#def getUserString(item, valid_in_format, input_panel, minlen, maxlen, 
#        echo_input, cursor_yx_pos, password):


#    input_count = 0

#    cur_y = cursor_yx_pos[0]
#    cur_x = cursor_yx_pos[1]
    
#    outstr = ""

#    input_win = input_panel.win
#    input_scr = input_panel.parent

#    cursor_start_pos = input_win.getyx()
#    cursor_start_ch = input_win.inch(cur_y, cur_x)

#    # if no max length given, default to size of input window
#    if maxlen == 0:
#        maxlen = input_win.getmaxyx()[1] - cur_x

#    if echo_input == True:
#        input_win.move(cur_y, cur_x)

#    # DEBUG %%%%%
#    input_scr.panels[0].title=""
#    for r in range (0, max+1):       
#        self.parent.parent.panels[0].win.delch(
#            self.parent.parent.panels[0].titleyx[0],
#            self.parent.parent.panels[0].titleyx[1])
#    # DEBUG %%%%%


#    target.focus()
#    self.parent.parent.updatePanels()
#    curses.doupdate()   
#    while incount < max:               
#        input_i = self.parent.win.getch()
            
#        if input_i == ord("\n"):                   # RETURN
#            if incount >= min:
#                status = "GOOD"
#            else:
#                status = "SHRT"
#            incount = max
#        elif input_i == 27:                        # ESCAPE
#            self.parent.win.nodelay(True)
#            n = self.parent.win.getch()
#            #n = self.parent.parent.inputwin.getch()
#            self.parent.win.nodelay(False)
#            if n == -1:
#                status = "CNCL"
#        elif input_i == curses.KEY_BACKSPACE:      # BACKSPACE                
#            if incount > 0:
#                xpos -= 1
#                target.win.delch(y, xpos)
#                incount -= 1
#            continue
#        elif input_i == curses.KEY_DC:             # DELETE
#            target.win.delch(y, xpos)
#            if incount > 0:
#                incount -= 1
#            continue
#        else:                                      # OTHER
#            status = self.validate(ok_format, input_i)
                
#            # DEBUG %%%%%
#            self.parent.parent.panels[0].title = copy.copy(status)##
#            # DEBUG %%%%%
                
#            if status == "GOOD":
#                outstr = outstr + chr(input_i)
#            else:
#                status = "FAIL"
#                break

#            if echo == True:               
#                if pw == True:
#                    target.win.addch(y, xpos, ord("#"))
#                else:
#                    target.win.addch(y, xpos, input_i)
#            incount += 1
#            xpos += 1

#        if echo == True:
#            target.win.move(y, xpos)
#        self.parent.parent.updatePanels()
#        curses.doupdate()              

#    target.win.hline(y,x, prech, max + 1)
#    target.defocus()
        
#    return status+":"+outstr