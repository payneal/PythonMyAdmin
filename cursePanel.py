﻿import copy
import curses
from curseTextbox import CurseTextbox
from curseItem import CurseItem

class CursePanel(object):
    """The CursePanel class is the central class of CursesDB. CursePanels serve
     as functional and visual containers for all other content. The CursePanel
    class wraps the curses library classes curses.window and curses.panel"""   
    def __init__(self, **kwargs):      
        self.global_storage                             = kwargs["global_storage" ]
        self.panel_storage                              = {}  
        self.parent_screen                              = kwargs["parent"]
                             
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

        if "_inner_text" in kwargs:     self._inner_text = kwargs["_inner_text"]
        if "_secondary_focus" in kwargs:
            self._sec_foc_key        = kwargs["_secondary_focus"]
            self._sec_foc_prereq_key = kwargs["_secondary_focus_prereq"]

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
                          
    def load(self):
        """ executes custom behavior, then does so for items and text boxes"""
        if hasattr(self, "_on_load"):
            # to call a function on load:
            #   "action"        = "call_function"
            #   "action_args"   = packed list of arguments for above function
            # to draw text to screen on load:
            #   "action"        = "draw_text"
            #   "action_args"   = "list of 4-tuples- each list provides a
            #       4-tuple for addstr (y, x, character drawn, character attr)
            #       and uses one tuple per addstr call
            if self._on_load["action"] == "call_function":
                func = getattr(self, _on_load["action_name"])
                func(*_on_load["action_args"])

        self.loadItems()
        self.loadTextbox()

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

    def refreshPanel(self):
        self.draw()
        self.win.refresh()

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
        self.drawInnerText()

    def drawPanelContents(self):
        """ draws panel items and textbox to screen"""
        self.drawItems()
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

    def drawInnerText(self):
        """ draws hidden field _inner_text if set"""
        #     "_inner_text"   : [ (4, 21, "--------------------"),
        #                         (5, 21, "--------------------")]
        if hasattr(self, "_inner_text"):
            txt_atr = self.style.txt_atr
            txt_clr = self.style.txt_clr
            for t in range (0, len(self._inner_text)):
                self.win.addstr(self._inner_text[t][0], self._inner_text[t][1],
                                self._inner_text[t][2], txt_atr | txt_clr)

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
     
    def loadItems(self):
        for i in range(0, self.item_count):
            self.items[self.item_indexes[i]].load()
        
    def drawItems(self):
        for i in range(0, self.item_count):
            self.items[self.item_indexes[i]].draw()

    def getItemByName(self, item_name):
            if item_name in self.items:
                return self.items[item_name]

    def prevItem(self, target_key=None):
        """ defocus current item in focus indices and focus item before it"""
        if target_key == None:  target = self

        if target.item_count == 0:                                       return
               
        prev_focus_index = target.focus_index 
        while True:
            if target.focus_index < 0:                   target.focus_index = 0
            else:                                       target.focus_index -= 1    

            if target.focus_index == prev_focus_index:                   return                                     
            elif target.focus_index == -1: 
                target.focus_index = target.item_count - 1
            
            item_key = target.item_indexes[target.focus_index]
            if target.items[item_key].is_active == True:
                if target.items[item_key].focusable == True:              break

        # if this panels has a secondary focus and we're changing item
        # indices, if the next index isn't the prereq item for that
        # secondary panel, defocus the secondary panel
        if hasattr(target, "_sec_foc_key"):
            sec_panel = self.parent_screen.getPanelByName(target._sec_foc_key)
            if target._sec_foc_prereq_key == item_key:
                 sec_panel.focus()
            else:
                sec_panel.defocus()
        self.changeFocusItem(item_key)

    def nextItem(self, target_key=None):
        """ defocus current item in focus indices and focus item after it"""
        if target_key == None:   target = self

        if target.item_count == 0:                                       return
         
        prev_focus_index = target.focus_index 
        while True:
            if target.focus_index < 0:                   target.focus_index = 0
            else:                                       target.focus_index += 1

            if target.focus_index == prev_focus_index:                   return
            elif target.focus_index == target.item_count:      
                target.focus_index = 0
            
            item_key = self.item_indexes[target.focus_index]
            if target.items[item_key].is_active == True:
                if target.items[item_key].focusable == True:              break
       
        # if this panels has a secondary focus and we're changing item
        # indices, if the next index isn't the prereq item for that
        # secondary panel, defocus the secondary panel
        if hasattr(target, "_sec_foc_key"):
            sec_panel = self.parent_screen.getPanelByName(target._sec_foc_key)
            if target._sec_foc_prereq_key == item_key:
                 sec_panel.focus()
            else:
                sec_panel.defocus()
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

    def loadTextbox(self):
        if self.textbox != None:                            self.textbox.load()

    def drawTextbox(self):
        """ draws textbox data to physical screen """
        if self.textbox != None:                        self.textbox.drawText()

    def resetTextbox(self, text=""):
        """ resets textbox data to text or empty string """
        if self.textbox != None:                   self.textbox.resetText(text)

    def clearTextbox(self):
        """ clears textbox text from physical screen """
        if self.textbox != None:                       self.textbox.clearText()

    def turnPage(self, direction, target):
        """ turns textbox page and redraws textbox"""
        if target == "self":
            if self.textbox != None:
                self.textbox.turnPage(direction)
                self.drawTextbox()
        elif target == "infotar":
            if self.infotar != None:
                self.infotar.turnPage(direction, "self")