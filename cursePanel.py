import curses
import curses.panel
from curseTextbox import CurseTextbox
from curseItem import CurseItem

class CursePanel(object):
    """The CursePanel class is the central class of CursesDB. CursePanels serve
     as functional and visual containers for all other content. The CursePanel
    class wraps the curses library classes curses.window and curses.panel"""   
    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]          
             
        #self.parent = None                      # set in separate load function

        self.height = kwargs["h"]
        self.width = kwargs["w"]
        self.y = kwargs["y"]
        self.x = kwargs["x"]

        self.win = curses.newwin(self.height, self.width, self.y, self.x)           
        self.panel = curses.panel.new_panel(self.win)  
              
        self.titleyx = kwargs["titleyx"]
        self.title = kwargs["title"]
            
        self.textbox = kwargs["textbox"]    
                            
        #self.infotext = None                   # set in separate load function
        #self.infotexttar = None                # set in separate load function

        self.style = kwargs["style"]
        self.dftstyle = kwargs["dftstyle"]   

        self.focusable = kwargs["focusable"]     
        self.isfocused = False

        #self.items = None                      # set in separate load function
        self.findex = -2                        # set in separate load function

    ###########################################################################

    #       update
    def update(self, force_refresh=False):
        self.set_style(self.isfocused)
        self.update_textbox()
        self.update_items()
        if force_refresh == True:
            self.win.refresh()
        else:
            self.win.noutrefresh()     
            
    def update_items(self):
        item_count = len(self.items)
        for i in range(0, item_count):
            self.items[i].update()

    ###########################################################################                   

    #
    def load(self, kwargs):
        self.onload(**kwargs)

    def onload(self, **kwargs):
        self.parent = kwargs["parent"]
        self.infotext = kwargs["infotext"]
        self.infotexttar = kwargs["infotexttar"]

    def load_items(self, item_list):
        item_count = len(item_list)
        self.items = []                                    # items list created
        for i in range(0, item_count):
            self.items.append(CurseItem(**item_list[i]))
        #self.findex = -2                                   # findex var created

    def clear_panel(self):
        #self.win.immedok(True)
        #self.win.clearok(1)
        self.panel.hide()
        self.win.erase()
        
        #self.win.attron(curses.color_pair(1))
        #for l in range (0, 22):
        #    self.stdscr.hline(l, 0, 32, 80)
        #if len(self.items) > 0:
        #    for i in range (0, len(self.items)):
        #        sel
        #self.win.attroff(curses.color_pair(1))

        #if len(self.items) > 0:
        #    pass#for i in range (0, len(self.items)):
        #self.win.refresh()
        #self.win.immedok(False)


    ###########################################################################

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
            self.infotexttar.reset_textbox()
            self.infotexttar.update(True)
        if len(self.items) > 0:
            if self.findex >= 0:
                self.items[self.findex].defocus()
                self.items[self.findex].infotexttar.reset_textbox()
                self.findex = -2
                                   
    ###########################################################################

    #       showinfotxt        
    def showinfotxt(self):
        if self.infotexttar != None:
            if len(self.infotext) != 0:
                self.infotexttar.reset_textbox(self.infotext)
                self.infotexttar.draw_textbox()

    #       getinput
    def check_input(self, inputc):

        #
        #       textbox page prev/next: w/s
        #   
        if self.infotexttar != None:
            if inputc == str(ord("w")):
                self.infotexttar.textbox.turnpage("prev")
            elif inputc == str(ord("s")):
                self.infotexttar.textbox.turnpage("next")
            self.infotexttar.update(True)

        #
        #       item list prev/next/select: q/e/space
        #
        items_len = len(self.items)
        status = "none"
        if items_len > 0:
            prev_findex = self.findex
            if inputc == str(ord("q")):      
                self.prevItem(prev_findex, items_len)
            elif inputc == str(ord("e")):
                self.nextItem(prev_findex, items_len)
            elif inputc == str(ord(" ")):
                if self.findex >= 0:
                    status = self.items[self.findex].select()

            if prev_findex != self.findex:
                self.items[prev_findex].defocus()
                self.items[self.findex].focus() 
            self.update_items()
        return status


    def nextItem(self, prev_findex, items_len):
        # self.findex < 0 means no previous item was focused
        while True:
            if self.findex < 0:
                self.findex = 0
            else:
                self.findex += 1

            if self.findex == prev_findex:
                return                                      # back @ start
            elif self.findex == items_len:
                self.findex = 0
            
            if self.items[self.findex].focusable == True:
                break;

    def prevItem(self, prev_findex, items_len):
        while True:
            if self.findex < 0:
                self.findex = 0
            else:
                self.findex -= 1    

            if self.findex == prev_findex:
                return                                      # back @ start
            elif self.findex == -1:
                self.findex = items_len - 1
            
            if self.items[self.findex].focusable == True:
                break;

    #       select_panel
    def select_panel(self):
        self.set_style(True)

    #       deselect_panel
    def deselect_panel(self):
        self.set_style()

    ###########################################################################

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
        
    #       update_textbox
    def update_textbox(self, refresh=False):
        if self.textbox != None:
            self.textbox.update(refresh)

    #       draw_textbox
    def draw_textbox(self):
        if self.textbox != None:
            self.textbox.drawtext()

    #       reset_textbox
    def reset_textbox(self, text=""):
        if self.textbox != None:
            self.textbox.resettext(text)

    #       clear_textbox
    def clear_textbox(self):
        if self.textbox != None:
            self.textbox.cleartext()

    ###########################################################################

    #       get_relxy
    def get_relxy(self):                                                      
        return (self.ppanel.y - self.y, self.ppanel.x - self.x)
     
# . . . . E N D . . . C L A S S . . . D E F I N I T I O N . . . . . . . . . . . 



