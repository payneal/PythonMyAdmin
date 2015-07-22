import curses
import curses.panel
import curseTextbox

class CursePanel(object):
    """The CursePanel class is the central class of CursesDB. CursePanels serve
     as functional and visual containers for all other content. The CursePanel
    class wraps the curses library classes curses.window and curses.panel"""   
    def __init__(self, **kwargs):
        if kwargs == None:
            self.isinit = False
        else:
            self.id = kwargs["id"]                           
            self.name = kwargs["name"]          
             
            self.height = kwargs["h"]
            self.width = kwargs["w"]
            self.y = kwargs["y"]
            self.x = kwargs["x"]

            self.win = curses.newwin(self.height, self.width, self.y, self.x)           
            self.panel = curses.panel.new_panel(self.win)  
              
            self.titleyx = kwargs["titleyx"]
            self.title = kwargs["title"]
            
            #### TEXTBOX PARENT SET HERE
            #if kwargs["textbox"] != None:
            #    kwargs["textbox"]["parent"] = self
            #    self.textbox = curseTextbox.CurseTextbox(kwargs["textbox"])
            #else:
            #    self.textbox = None
            self.textbox = kwargs["textbox"]

            self.style = kwargs["style"]
            self.dftstyle = kwargs["dftstyle"]            
              
            self.focusable = kwargs["focusable"]     
            self.isfocused = False
            
            #self.isvisible = False
                
            #self.onload()
    
    #       update
    def update(self, force_refresh=False):
        self.set_style(self.isfocused)
        self.draw_text()
        if force_refresh == True:
            self.win.refresh()
        else:
            self.win.noutrefresh()            

    #
    def load(self, kwargs):
        self.onload(**kwargs)

    #       onload
    def onload(self, **kwargs):
        self.ppanel = kwargs["ppanel"]
        self.infotext = kwargs["infotext"]
        self.infotexttar = kwargs["infotexttar"]

    #       focus
    def focus(self):
        self.isfocused = True
        self.onfocus()

    #       defocus
    def defocus(self):
        self.isfocused = False
        self.ondefocus()

    #       onfocus
    def onfocus(self):
        self.select_panel()
        self.showinfotxt()

    #       ondefocus
    def ondefocus(self):
        self.deselect_panel()
        if self.infotexttar != None:
            self.infotexttar.reset_text()
            self.infotexttar.update(True)
        
                                                          
    #################################################
    #       showinfotxt        
    def showinfotxt(self):
        if self.infotexttar != None:
            if len(self.infotext) != 0:
                self.infotexttar.reset_text(self.infotext)
                self.infotexttar.draw_text()

    #       getinput
    def check_input(self, inputc):
        if self.infotexttar != None:
            if inputc == str(ord("w")):
                self.infotexttar.textbox.turnpage("prev")
            if inputc == str(ord("s")):
                self.infotexttar.textbox.turnpage("next")
            self.infotexttar.update(True)

    #       select_panel
    def select_panel(self):
        self.set_style(True)

    #       deselect_panel
    def deselect_panel(self):
        self.set_style() 

    #################################################

    #       set_style
    def set_style(self, focus=False, s_obj=0):
        try:
            if s_obj == 0:
                s_obj = self.style
        except:
            s_obj = self.dftstyle
        
        if focus == False:
            bg_chtype = s_obj.bg_chtype
            br_chrs = s_obj.br_chrs
            br_atr = s_obj.br_atr
            br_clr = s_obj.br_clr
            ttl_atr = s_obj.ttl_atr
            ttl_clr = s_obj.ttl_clr
        else:
            bg_chtype = s_obj.fbg_chtype
            br_chrs = s_obj.fbr_chrs
            br_atr = s_obj.fbr_atr
            br_clr = s_obj.fbr_clr
            ttl_atr = s_obj.fttl_atr
            ttl_clr = s_obj.fttl_clr            

        self.set_bg(bg_chtype)                
        self.set_border(br_chrs, br_atr, br_clr)
        self.draw_title(ttl_atr, ttl_clr)

    #       set_bg
    def set_bg(self, bg_chtype=0):
        try:
            if bg_chtype == 0:
                bg_chtype = self.style.bg_chtype
        except:
            bg_chtype = 32

        #self.win.bkgdset(bg_chtype)
        self.win.bkgd(bg_chtype)

    #       set_border
    def set_border(self, br_chs=[], br_at=0, br_cl=0):
        try:           
            if len(br_chs) == 0:
                br_chs = self.style.br_chrs
                br_at = self.style.br_atr
                br_cl = self.style.br_clr
            elif br_chs[0] == -1:
                return
            self.win.attron(br_at | br_cl)
            self.win.border(*br_chs)        
            self.win.attroff(br_at | br_cl)
        except:
            self.win.border(0)
    
    #       draw_title                 
    def draw_title(self, ttl_atr=0, ttl_clr=0):
        if len(self.title) == 0:
            return
        try:
            y = self.titleyx[0]
            x = self.titleyx[1]
            txt = self.title
            if ttl_atr == 0:
                ttl_atr = self.style.ttl_atr
            if ttl_clr == 0:
                ttl_clr = self.style.ttl_clr
        except:
            y = 0
            x = 0
            txt = "DFT"
            ttl_atr = 0
            ttl_clr = curses.color_pairs(0)

        self.win.attron(ttl_atr | ttl_clr)
        self.win.addstr(y, x, txt, ttl_atr | ttl_clr)
        self.win.attroff(ttl_atr | ttl_clr)
        
    def draw_text(self):
        if self.textbox != None:
            self.textbox.drawtext()

    def reset_text(self, text=""):
        if self.textbox != None:
            self.textbox.resettext(text)

    def clear_text(self):
        if self.textbox != None:
            self.textbox.cleartext()

    #       get_relxy
    def get_relxy(self):                                                      
        return (self.ppanel.y - self.y, self.ppanel.x - self.x)

      
# . . . . E N D . . . C L A S S . . . D E F I N I T I O N . . . . . . . . . . . 



