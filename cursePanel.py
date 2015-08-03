import copy
import curses
from curseTextbox import CurseTextbox
from curseItem import CurseItem

class CursePanel(object):
    """The CursePanel class is the central class of CursesDB. CursePanels serve
     as functional and visual containers for all other content. The CursePanel
    class wraps the curses library classes curses.window and curses.panel"""   
    def __init__(self, **kwargs):      
        self.globals                             = kwargs["globals"]  
        self.parent                                     = kwargs["parent"]
                             
        if "act_msg_map" in kwargs:    self.act_msg_map = kwargs["act_msg_map"]
        else:                          self.act_msg_map = None

        self.y                                          = kwargs["size"][0]
        self.x                                          = kwargs["size"][1]
        self.height                                     = kwargs["size"][2]
        self.width                                      = kwargs["size"][3]

        self.win          = curses.newwin(self.height, self.width, self.y, self.x)           
        
        self.style = kwargs["style"]

        if "title" in kwargs:        
            self.title                                  = kwargs["title"][0]
            self.title_y                                = kwargs["title"][1]    
            self.title_x                                = kwargs["title"][2]
        else:
            self.title                                  = "" 
            self.title_y                                = 0 
            self.title_x                                = 0
        
        if "textbox" in kwargs:            self.textbox = kwargs["textbox"]
        else:                              self.textbox = None     

        if "info" in kwargs:                  self.info = kwargs["info"]
        else:                                 self.info = None

        if "infotar" in kwargs:        self.infotar_str = kwargs["infotar"] 
        else:                          self.infotar_str = None

        self.infotar = None            
                              
        if "focusable" in kwargs:        self.focusable = kwargs["focusable"]
        else:                            self.focusable = False     

        self.items                  = {} # dict of item name : item object pairs
        self.item_indexes           = [] # list of item names
        self.item_count             = 0
       
        self.is_item_focused        = False
        self.focus_key              = ""
        self.focus_index            = -1
        self.focus_item             = None

        self.is_focused             = False
        self.changed                = False

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
                    
    def update(self):
        if self.changed == True:
            self.win.touchwin()
            self.win.noutrefresh()
            self.changed = False

    def checkInput(self, act_key):
        """ check if action triggers a response in panel or panel items """
        msg = None
        if act_key in self.act_msg_map:
            if act_key == "select":
                return self.select()
            else:             
                msg = copy.deepcopy(self.act_msg_map[act_key])

        self.readMessage(msg)
        return msg
        
    def readMessage(self, msg):
        if msg == None:                                                  return
        
        if msg["msg_status"] == "unread":
            if msg["recv_layer"] == "screen" or msg["recv_layer"] == "self":
                if msg["on_recv"] == "call_function":

                    func = getattr(self, msg["recv_act"])
                    if msg["recv_args"] == None:  
                        msg["ret_info"] = func()
                    else:        
                        msg["ret_info"] = func(*msg["recv_args"])

                    msg["msg_status"] = "read"

        return msg

    def showInfo(self):
        """ reset infotar and tell it to redraw textbox"""      
        if self.infotar != None:
            self.infotar.resetTextbox(self.info)
            self.infotar.drawTextbox()
        elif self.info != None:
            self.resetTextbox(self.info)
            self.drawTextbox()

    def hideInfo(self):
        """ reset infotar and tell it to redraw textbox"""      
        if self.infotar != None:
            self.infotar.resetTextbox()
            self.infotar.drawTextbox()
        elif self.info != None:
            self.resetTextbox()
            self.drawTextbox()
                          
    def select(self):
        """ tells focus item to activate its stored _on_select behavior"""
        if self.focus_item != None:
            return self.focus_item.select()

    def focus(self):
        """ sets panel focus, redraws panel, infotex to screen """
        self.is_focused = True
        self.draw()
        self.showInfo()

    def defocus(self):
        """ removes panel focus, redraws panel, hides infotex from screen """
        self.is_focused = False
        self.draw()
        self.hideInfo()

        if self.item_count > 0:
            self._defocusItem()

#/\/\/  PANEL DRAW FUNCTIONS  /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/

    def draw(self):
        """ draw panel and contents to screen and flag to be updated """    
        self.drawPanel()
        self.drawPanelContents()
        self.changed = True

    def drawPanel(self):
        """ draws panel background, border, and title to screen """
        if self.is_focused == False:
            bg_chtype   = self.style.bg_chtype
            br_chrs     = self.style.br_chrs
            br_atr      = self.style.br_atr
            br_clr      = self.style.br_clr
            ttl_atr     = self.style.ttl_atr
            ttl_clr     = self.style.ttl_clr
        else:
            bg_chtype   = self.style.fbg_chtype
            br_chrs     = self.style.fbr_chrs
            br_atr      = self.style.fbr_atr
            br_clr      = self.style.fbr_clr
            ttl_atr     = self.style.fttl_atr
            ttl_clr     = self.style.fttl_clr            

        self._setBg(bg_chtype)                
        self._setBorder(br_chrs, br_atr, br_clr)
        self.drawTitle()

    def drawPanelContents(self):
        """ draws panel items and textbox to screen"""
        for i in range(0, self.item_count):
            self.items[self.item_indexes[i]].draw()
        self.drawTextbox()

    def clearPanel(self):
        """ clears everything inside panel from screen """
        self.win.move(0,0)
        self.win.clrtobot()
        self.changed = True

    def drawTitle(self):
        """ draws panel title to screen """
        if self.title == "" or self.title == None:                       return

        ttl_atr = self.style.ttl_atr
        ttl_clr = self.style.ttl_clr
        self.win.attron(ttl_atr | ttl_clr)
        self.win.addstr(self.title_y, self.title_x,self.title, ttl_atr|ttl_clr)
        self.win.attroff(ttl_atr | ttl_clr)

    def _setBg(self, bg_chtype=0):
        """ sets panel background color and attributes """
        if bg_chtype == 0:                    bg_chtype = self.style.bg_chtype
        self.win.bkgd(bg_chtype)

    def _setBorder(self, br_chs=[], br_at=0, br_cl=0):
        """ draws panel border (all inner cells adjacet to window edge) """
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
                                                                
#/\/\/\ ITEM FUNCTIONS  \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
             
    def prevItem(self):
        """ defocus current item in focus indices and focus item before it"""
        if self.item_count == 0:                                         return
          
        prev_focus_index = self.focus_index 
        while True:
            if self.focus_index < 0:                       self.focus_index = 0
            else:                                         self.focus_index -= 1    

            if self.focus_index == prev_focus_index:                     return                                     
            elif self.focus_index == -1: 
                self.focus_index = self.item_count - 1
            
            item_key = self.item_indexes[self.focus_index]
            if self.items[item_key].focusable == True:                    break

        self.changeFocusItem(item_key)

    def nextItem(self):
        """ defocus current item in focus indices and focus item after it"""
        if self.item_count == 0:                                         return
          
        prev_focus_index = self.focus_index 
        while True:
            if self.focus_index < 0:                       self.focus_index = 0
            else:                                         self.focus_index += 1

            if self.focus_index == prev_focus_index:                     return
            elif self.focus_index == self.item_count:      self.focus_index = 0
            
            item_key = self.item_indexes[self.focus_index]
            if self.items[item_key].focusable == True:                    break

        self.changeFocusItem(item_key)
        
    def changeFocusItem(self, new_key):
        """ switches focus from current focused item to new item """
        self._defocusItem()
        self._focusItem(new_key)

    def _focusItem(self, item_key):
        """ apply focus to panel child item """
        self.is_item_focused     = True
        self.focus_key           = item_key
        self.focus_index         = self.item_indexes.index(item_key)
        self.focus_item          = self.items[item_key]
        self.focus_item.focus()
        
    def _defocusItem(self):
        """ remove focus from panel child item """
        if self.focus_item != None:
            self.focus_item.defocus()  
            self.is_item_focused = False
            self.focus_key       = ""
            self.focus_index     = -1
            self.focus_item      = None
                     
#/\/  TEXTBOX FUNCTIONS  /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

    def turnPage(self, direction, target):
        """ turns textbox page and redraws textbox"""
        if target == "self":
            if self.textbox != None:
                self.textbox.turnPage(direction)
                self.drawTextbox()
        elif target == "infotar":
            if self.infotar != None:
                self.infotar.turnPage(direction, "self")

    def drawTextbox(self):
        """ draws textbox data to physical screen """
        if self.textbox != None:                        self.textbox.drawText()

    def resetTextbox(self, text=""):
        """ resets textbox data to text or empty string """
        if self.textbox != None:                   self.textbox.resetText(text)

    def clearTextbox(self):
        """ clears textbox text from physical screen """
        if self.textbox != None:                       self.textbox.clearText()