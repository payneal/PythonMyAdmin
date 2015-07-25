import curses
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
        self.onselect["func"](*self.onselect["args"])
        return self.onselect["rstatus"]

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

