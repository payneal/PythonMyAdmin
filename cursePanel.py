import copy
import curses
from curseTextbox import CurseTextbox
from curseItem import CurseItem

class CursePanel(object):
    """The CursePanel class is the central class of CursesDB. CursePanels serve
     as functional and visual containers for all other content. The CursePanel
    class wraps the curses library classes curses.window and curses.panel"""   
    def __init__(self, **kwargs):      
        self.global_storage                         = kwargs["global_storage" ]
        self.panel_storage                          = {}  
        self.parent_screen                          = kwargs["parent"]
                             
        if "act_msg_map" in kwargs:    self.act_msg_map = kwargs["act_msg_map"]
        else:                          self.act_msg_map = None

        self.y                                      = kwargs["size"][0]
        self.x                                      = kwargs["size"][1]
        self.height                                 = kwargs["size"][2]
        self.width                                  = kwargs["size"][3]
        
        # viewport y/x: viewport origin within pad
        # screen y/x/h/w: panel dimension on screen
        # refresh(viewport_y,viewport_x,screen_y, screen_x, screen_h, screen_w)
        if "is_pad" in kwargs:

            self.is_pad=True

            self.p_height = kwargs["psize"][0]
            self.p_width  = kwargs["psize"][1]

            self.win   = curses.newpad(self.p_height, self.p_width)

            self.s_y_max = self.y + self.height
            self.s_x_max = self.x + self.width      

            self.vp_y = 0;
            self.vp_x = 0;
            self.vp_y_max = self.p_height-self.height
            self.vp_x_max = self.p_width-self.width

            self.col_count = -1         #
            self.row_count = -1         #
            self.col_max_widths = None  #
            self.row_max_length = -1    #
            self.cols_per_win = -1

            self.cur_index = -1
            
            self.p_y_buff = 0
            self.p_x_buff = 0

            if "_inner_list" in kwargs:
                self._inner_list = kwargs["_inner_list"]
                #self.row_count = len(self._inner_list)

            self.sel_list_indices = []                       
        else:
            self.is_pad=False
            self.win   = curses.newwin(self.height, self.width, self.y, self.x)           
        
        self.style = kwargs["style"]

        if "title" in kwargs:        
            self.title                              = kwargs["title"][0]
            self.title_y                            = kwargs["title"][1]    
            self.title_x                            = kwargs["title"][2]
            if "title_args" in kwargs:
                self.title_args = kwargs["title_args"]
        else:
            self.title                              = "" 
            self.title_y                            = 0 
            self.title_x                            = 0
        
        if "textbox" in kwargs:      self.textbox = kwargs["textbox"]
        else:                        self.textbox = None     

        if "info" in kwargs:         self.info = kwargs["info"]
        else:                        self.info = None

        if "infotar" in kwargs:      self.infotar_str = kwargs["infotar"] 
        else:                        self.infotar_str = None
        self.infotar = None            
                              
        if "focusable" in kwargs:    self.focusable = kwargs["focusable"]
        else:                        self.focusable = False     

        if "is_sec_focus" in kwargs: self.is_sec_focus = kwargs["is_sec_focus"]
        else:                        self.is_sec_focus = False

        if "_inner_text" in kwargs:  self._inner_text = kwargs["_inner_text"]

        if "_default_focus_item_key" in kwargs:
            self._default_focus_item_key = kwargs["_default_focus_item_key"]

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
            if self.is_pad == False:
                self.win.noutrefresh()
            else:
                self.win.noutrefresh(self.vp_y, self.vp_x, 
                    self.y, self.x, self.height+self.y, self.width+self.x-2)
            self.changed = False

    def checkInput(self, act_key, aux_info=None):
        """ check if action triggers a response in panel or panel items """
        msg = None
        if act_key in self.act_msg_map:
            if act_key == "select":         msg = self.select()
            else:    msg = copy.deepcopy(self.act_msg_map[act_key])
       
        return self.readMessage(msg)
        
    def readMessage(self, msg):
        if msg == None:     return
        
        if msg["msg_status"] == "unread":
            if msg["recv_layer"] == "panel" or msg["recv_layer"] == "self":
                if msg["on_recv"] == "call_function":

                    func = getattr(self, msg["recv_act"])
                    if msg["recv_args"] == None:       msg["ret_info"] = func()
                    else:             msg["ret_info"] = func(*msg["recv_args"])

                    msg["msg_status"] = "read"
        return msg


    def reset(self):
        if hasattr(self, "_inner_list"):
            self._inner_list = None
            self.clearPanel()

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
                          
    def setInnerText(self, y, x, text):
        if not hasattr(self, "_inner_text"):
            setattr(self, "_inner_text", [])
            self._inner_text.append((y,x,text))
        else: self._inner_text.append((y, x, text))

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
        if self.focus_item != None:             return self.focus_item.select()

    def focus(self):
        """ sets panel focus, redraws panel, infotex to screen """
        self.is_focused = True
        if hasattr(self, "_default_focus_item_key"):
            if self.focus_item == None:
                self.changeFocusItem(self._default_focus_item_key)
        self.draw()
        self.showInfo()

    def defocus(self, keep_i_focus=False):
        """ removes panel focus, redraws panel, hides infotex from screen """
        self.is_focused = False
        self.draw()
        self.hideInfo()

        if self.item_count > 0:
            if keep_i_focus == False: self.defocusItem()

        if self.is_pad == True:
            if keep_i_focus == False:
                if self._inner_list != None:
                    if keep_i_focus != True:
                        self.clearList()
                        self.cur_index = -1
                        self.vp_y = 0
                        self.vp_x = 0

    def refreshPanel(self):
        self.draw()
        if self.is_pad == False: self.win.refresh()
        else:
            self.win.refresh(self.vp_y, self.vp_x, 
                self.y, self.x, self.height+self.y, self.width+self.x-2)

#/\/\/  PAD FUNCTIONS  \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/

    # used to give a panel a new results list
    def loadList(self, string_list=None):      
        if string_list == None:     s_list = self._inner_list
        else:                       s_list = string_list

        #self.col_hdrs
        
        self.col_count = len(s_list[0]) 
        self.row_count = len(s_list)
        self.col_max_widths = [0 for x in range(self.col_count)]
        self.row_max_length = 0

        row_total_length = 0

        # get longest total row length
        # get widest column width for each column
        for row in range(0,  self.row_count):
            for col in range(0, self.col_count):
                col_width = len(s_list[row][col]) + 2
                row_total_length += col_width 
                if col_width > self.col_max_widths[col]:
                    self.col_max_widths[col] = col_width
       
        # make all entries in same column equal length
        for row in range(0,  self.row_count):
            for col in range(0, self.col_count):        
                s_list[row][col] = s_list[row][col].center(
                    self.col_max_widths[col])
        
        # get total length of a list row
        for col in range(0, self.col_count):
            self.row_max_length += self.col_max_widths[col]

        self.cur_index = 1
        self.refreshPanel()
         
    def prevListItem(self, defocus_prev=True):
        if self.cur_index > 1:
            self.cur_index -= 1
            self.scrollUp()

    def nextListItem(self, defocus_prev=True):
        if self.cur_index < self.row_count - 1:
            self.cur_index += 1
            self.scrollDown()

    def scrollLeft(self):
        if self.is_pad == True:
            if self.vp_x > 0:
                self.vp_x -= 1
                self.refreshPanel()

    def scrollRight(self):
        if self.is_pad == True:
            if self.vp_x < (self.row_max_length -self.width)+ 1:
                self.vp_x += 1
                self.refreshPanel()

    def scrollUp(self):
        if self.is_pad == True:
            if self.p_y_buff > self.height:
                self.vp_y -= 1
                self.p_y_buff -= 1
            elif self.p_y_buff > 0: self.p_y_buff -= 1
            self.refreshPanel()

    def scrollDown(self):
        if self.is_pad == True:
            if self.p_y_buff < self.height: self.p_y_buff += 1
            elif self.p_y_buff + self.vp_y < self.p_height:  
                self.p_y_buff += 1
                self.vp_y += 1
            self.refreshPanel()

    def clearList(self):
        for l in range(0, len(self._inner_list)):
            self.win.hline(l,0,32,self.width - 1)
        self._inner_list = None

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
        if self.is_pad: self.drawInnerList()
        else:           self.drawTitle()
        self.drawInnerText()

    def drawPanelContents(self):
        """ draws panel items and textbox to screen"""
        self.drawItems()
        self.drawTextbox()

    def clearPanel(self):
        """ clears everything inside panel from screen """
        self.defocus(True)       
        self.win.move(0,0)
        self.win.clrtobot()
        self.changed = True
        
    def drawTitle(self):
        """ draws panel title to screen """
        if self.title == "" or self.title == None:      return

        ttl_atr = self.style.ttl_atr
        ttl_clr = self.style.ttl_clr
        try:
            self.win.attron(ttl_atr | ttl_clr)
            self.win.addstr(self.title_y, self.title_x,self.title, 
                ttl_atr|ttl_clr)
            self.win.attroff(ttl_atr | ttl_clr)
        except:            self.win.attroff(ttl_atr | ttl_clr)

        # INNER TEXT IS A LIST OF TUPLES!!!
    def drawInnerText(self):
        """ draws hidden field _inner_text if set"""
        #     "_inner_text"   : [ (4, 21, "--------------------"),
        #                         (5, 21, "--------------------")]
        # inner_text: 
        #   [<inner text line >,<<line t,ycoord>,<linet,xcoord>,<line t,text>>]
        #   [ line#, [y,x,text] ]
        if hasattr(self, "_inner_text"):
            txt_atr = self.style.txt_atr
            txt_clr = self.style.txt_clr
            try:
                for t in range (0, len(self._inner_text)):
                    self.win.addstr(
                        self._inner_text[t][0], 
                        self._inner_text[t][1],
                        self._inner_text[t][2], 
                        txt_atr | txt_clr)
            except: pass

    def drawInnerList(self):
        if self.row_count <= 0:     return

        # draw visible entries
        for row in range(0, self.row_count): # counter for number of lines to draw
            self.win.hline(row, 0, 32, self.width)      # clear line
             
            if row == 0: 
                self.win.attron(curses.A_BOLD | curses.color_pair(3))  
            elif row == self.cur_index:
                self.win.attron(self.style.ftxt_atr | self.style.ftxt_clr)   
                    
            x = 0
            for col in range(0, self.col_count):           
                self.win.addstr(row, x, self._inner_list[row][col])
                cell_len = len( self._inner_list[row][col])     
                x += cell_len     
                
            if row == 0:
                self.win.attroff(curses.A_BOLD | curses.color_pair(3)) 
            elif row == self.cur_index:
                self.win.attroff(self.style.ftxt_atr | self.style.ftxt_clr)

        # draw "more" arrows if content goes off screen
        if self.vp_x + self.width < self.row_max_length:
            if self.row_count < self.height: line_height = self.row_count
            else:                            line_height = self.height
            self.win.attron(curses.A_BOLD | curses.color_pair(5))   
            self.win.vline(self.vp_y + 1, self.vp_x + self.width - 3,
                ord("-"), line_height - 1)
            self.win.vline(self.vp_y + 1, self.vp_x + self.width - 2, 
                ord(">"),line_height - 1)
            self.win.attroff(curses.A_BOLD | curses.color_pair(5))   

        # draw pad title, which has to be handled different due to the
        # moving viewport

        # y = -1, x = -1, title=="" --> pad title that hasn't be initiated
        # y = -1, x =  0, title=="" --> pad title that has been initiated
        # y =  0, x  = 0, title=="" --> not a pad title, shouldn't see this!
        #if self.title_y == -1:
        #    if self.title_x == -1:
        #        # initialize title, store in title args so it won't trigger
        #        # drawing in normal title function
        #        temp = self.title_args[0]
        #        for i in range(0, self.title_args[1]):
        #            temp = temp.replace("!", 
        #                globals[self.title_args[1][i]], 1)
        #        self.title_args[0] = copy.copy(temp)

        #    ttl_atr = self.style.ttl_atr
        #    ttl_clr = self.style.ttl_clr
        #    try:
        #        self.win.attron(ttl_atr | ttl_clr)
        #        self.win.addstr(self.vp_y, self.vp_x, self.title_args[0],
        #            ttl_atr|ttl_clr)
        #        self.win.attroff(ttl_atr | ttl_clr)
        #    except:            self.win.attroff(ttl_atr | ttl_clr)        

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

    def prevItem(self):
        """ defocus current item, focus previous item in focus indices"""
        if self.item_count == 0:    return
               
        prev_focus_index = self.focus_index 
        while True:
            if self.focus_index < 0:    self.focus_index = 0
            else:                       self.focus_index -= 1    

            if self.focus_index == prev_focus_index:    return                                     
            elif self.focus_index == -1: 
                self.focus_index = self.item_count - 1
            
            item_key = self.item_indexes[self.focus_index]
            if self.items[item_key].is_active == True:
                if self.items[item_key].focusable == True:  break
        
        self.changeFocusItem(item_key)

    def nextItem(self):
        """ defocus current item, focus next item in focus indices"""
        if self.item_count == 0:    return
         
        prev_focus_index = self.focus_index 
        while True:
            if self.focus_index < 0:    self.focus_index = 0
            else:                       self.focus_index += 1

            if self.focus_index == prev_focus_index:    return
            elif self.focus_index == self.item_count:      
                self.focus_index = 0
            
            item_key = self.item_indexes[self.focus_index]
            if self.items[item_key].is_active == True:
                if self.items[item_key].focusable == True:  break
       
        self.changeFocusItem(item_key)
        
    def changeFocusItem(self, new_key):
        """ switches focus from current focused item to new item """
        self.defocusItem()
        self.focusItem(new_key)

    def focusItem(self, item_key):
        """ apply focus to panel child item """
        self.is_item_focused     = True
        self.focus_key           = item_key
        self.focus_index         = self.item_indexes.index(item_key)
        self.focus_item          = self.items[item_key]
        self.focus_item.focus()
        
    def defocusItem(self):
        """ remove focus from panel child item """
        if self.focus_item != None:
            self.focus_item.defocus()  
            self.is_item_focused = False
            self.focus_key       = ""
            self.focus_index     = -1
            self.focus_item      = None

    def selectItem(self, item_key=None):
        i_key = None
        if item_key == None:
            if self.focus_item != None:     i_key = self.focus_key
        elif item_key in self.items:    i_key = item_key
        if i_key == None:    return
        item = self.items[i_key]
        return item.select()
                     
#/\/  TEXTBOX FUNCTIONS  /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

    def loadTextbox(self):
        if self.textbox != None:        self.textbox.load()

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