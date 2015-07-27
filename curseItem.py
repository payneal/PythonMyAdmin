import curses
import curses.ascii
import copy
#from cursePanel import CursePanel

class CurseItem(object):
    """description of class"""
    def __init__(self, **kwargs):
        self.parent                 = kwargs["parent"]

        self.lindex                 = kwargs["lindex"]
        self.y                      = kwargs["y"] # RELATIVE TO PARENT WIN
        self.x                      = kwargs["x"] # RELATIVE TO PARENT WIN

        self.listheight             = kwargs["listheight"]
        self.listwidth              = kwargs["listwidth"]   
        
               
        self.lbltext                = kwargs["lbltext"]

        self.infotext               = kwargs["infotext"]
        self.infotexttar            = kwargs["infotexttar"]

        self.focusable              = kwargs["focusable"]     
        self.isfocused              = False

        self.onselect               = kwargs["onselect"]

        self.style                  = kwargs["style"]

    ###########################################################################

    #       update
    def update(self):
        self.set_style(self.isfocused)

    def load(self, kwargs):
        pass

    def onload(self, **kwargs):
        pass

    def focus(self):
        self.isfocused = True
        self.onfocus()

    def onfocus(self):
        self.showinfotxt()
        
    def defocus(self):
        self.isfocused = False
        self.ondefocus()

    def ondefocus(self):
        if self.infotexttar != None:
            self.infotexttar.reset_textbox()
            self.infotexttar.update(True)

    # onselect = { func: function(), kwargs: { argkey:argval...}
    def select(self):
        status = ""
        info = ""
        if self.onselect["func_type"] == "other":
            self.onselect["func"](*self.onselect["args"])
            status = self.onselect["rinfo"]
        elif self.onselect["func_type"] == "self":
            if self.onselect["func"] == "get_user_string":
                info = "$" + self.get_usrstr(*self.onselect["args"])
                status = status + info
        return status

    ###########################################################################

    #       showinfotxt        
    def showinfotxt(self):
        if self.infotexttar != None:
            if len(self.infotext) != 0:
                self.infotexttar.reset_textbox(self.infotext)
                self.infotexttar.draw_textbox()

    def changeinfotxt(self, text):
        if self.infotexttar != None:
            self.infotext = copy.copy(text)
            self.showinfotxt()

    # http://stackoverflow.com/questions/5977395/ncurses-and-esc-alt-keys
    def get_usrstr(self, format, min=1, max=0, echo=False, 
                   y=0, x=0, pw=False ):     
        incount = 0
        xpos = x
        status = "UNDF"
        outstr = ""
        if max == 0:
            max = self.parent.win.getmaxyx()[1] - x
        
        prepos = self.parent.win.getyx()
        if echo== True:
            self.parent.win.move(y,x)

        while incount < max:

            input_i = self.parent.win.getch()
            
            if input_i == ord("\n"):                   # RETURN
                if incount > mn:
                    status = "GOOD"
                else:
                    status = "SHRT"
                break
            elif input_i == 27:                           # ESCAPE
                self.parent.win.nodelay(True)
                n = self.parent.win.getch()
                self.parent.win.noodelay(False)
                if n == -1:
                    status = "CNCL"
                    break
            elif input_i == curses.KEY_BACKSPACE:            # BACKSPACE                
                if incount > 0:
                    xpos -= 1
                    self.parent.win.delch(y, xpos)
                    incount -= 1
            elif input_i == curses.KEY_DC:                   # DELETE
                self.parent.win.delch(y, xpos)
                if incount > 0:
                    incount -= 1
            else:                                      # OTHER
                status = self.validate(format, input_i)
                if status == "GOOD":
                    outstr = outstr + chr(input_i)
                else:
                    status = "FAIL"
                    break

                incount += 1
                xpos += 1
                if echo == True:
                    self.parent.win.move(y, xpos)
                    if pw == True:
                        self.parent.win.addch(y, xpos, ord("#"))
                    else:
                        self.parent.win.addch(y, xpos, input_i)

            if echo == True:
                self.parent.win.move(y, xpos)
              
        return status+":"+outstr
           
    # format string: [alpha][digit][whitespace][punctuation][other]
    def validate(self, format, input_i):
        if curses.ascii.isalpha(input_i) != int(format[0]):
            return "ERR_ALPHA"
        if curses.ascii.isdigit(input_i) != int(format[1]):
            return "ERR_DIGIT"
        if curses.ascii.isspace(input_i) != int(format[2]):
            return "ERR_WSPACE"
        if curses.ascii.ispunct(input_i) != int(format[3]):
            return "ERR_PUNCT"
        else:
            return "OK"

    ###########################################################################

    def set_style(self, focus=False, s_obj=0):
        try:
            if s_obj == 0:
                s_obj = self.style
        except:
            s_obj = self.dftstyle
        
        if focus == False:
            txt_atr = s_obj.txt_atr
            txt_clr = s_obj.txt_clr
            txt_bg_clr = s_obj.txt_bg_clr
        else:
            txt_atr = s_obj.ftxt_atr
            txt_clr = s_obj.ftxt_clr   
            txt_bg_clr = s_obj.ftxt_bg_clr
           
        txt_atrclr = txt_atr | txt_clr

        self.parent.win.attron(txt_bg_clr)
        self.parent.win.hline(self.y, self.x, 32, self.listwidth)
        self.parent.win.attroff(txt_bg_clr)

        self.parent.win.addstr(self.y, self.x, self.lbltext, txt_atrclr)

    def hide_list(self):
        pass

