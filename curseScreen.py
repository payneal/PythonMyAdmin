import copy
import curses

class CurseScreen(object):
    """description of class"""
    def __init__(self, **kwargs):
        self.global_storage     = kwargs["global_storage" ]
        self.screen_storage     = {}
        self.user_strip_str     = kwargs["user_strip"]
        self.ftr_strip_str      = kwargs["ftr_strip"]
        self.screens            = kwargs["screens"]

        self.key_action_map     = kwargs["key_action_map"]
        self.act_msg_map        = kwargs["act_msg_map"]
        self.can_panel_change   = kwargs["can_panel_change"]

        self.style              = kwargs["style"]

        self.panels             = {}    # dictionary of cursePanels
        self.panel_indexes      = []    # list of panel keys in intended order
        self.panel_count        = 0     # number of panaels

        self.is_panel_focused   = False # is a panel focused on the screen now
        self.focus_key          = ""    # key for current focused panel
        self.focus_index        = -1    # focus panel key index in panel_indexes
        self.focus_panel        = None  # current focused panel

        self.fpanel_key_stack   = []
        self.fpanel_stack_top   = None
        self.fpnl_stk_ht        = 0

        if "default_focus_key" in kwargs: 
              self.default_focus_key = kwargs["default_focus_key"]
        else: self.default_focus_key = ""

        if "_on_load" in kwargs:
            self._on_load = kwargs["_on_load"]
            self._loaded  = False
            if "_load_once" in kwargs:
                self._load_once = kwargs["_load_once"]

        self.is_active          = False
        self.update_screen      = False
        
    def checkInput(self, input):
        """ checks if input triggers action in screen or its focused panel """
        if self.is_active != True: return
        if input not in self.key_action_map:   
            #self.global_storage['log_name'] = chr(int(input))+" HOTKEY_"+chr(int(input))
            #self.setUserStripInfo()
            #self.drawUserStripInfo()            
            #return
            act_key = "HOTKEY_"+chr(int(input))
        else:                       act_key = self.key_action_map[input]
        #if "other" not in self.key_action_map: return 
        
        msg = None   
        if act_key in self.act_msg_map: 
            msg = copy.deepcopy(self.act_msg_map[act_key])
        elif self.focus_panel != None: #
            msg = self.focus_panel.checkInput(act_key, input)
    
        return self.readMessage(msg)
             
    def updateScreen(self):                                 self.updatePanels()

    def readMessage(self, msg):
        if msg == None: return
        
        if msg["msg_status"] == "unread":
            if msg["recv_layer"] == "screen" or msg["recv_layer"] == "self":
                if msg["on_recv"] == "call_function":

                    func = getattr(self, msg["recv_act"])
                    if msg["recv_args"] == None:       msg["ret_info"] = func()
                    else:             msg["ret_info"] = func(*msg["recv_args"])

                    msg["msg_status"] = "read"
                    if "replace_msg" in msg:
                        if msg["ret_info"] != None:
                            msg_new = copy.deepcopy(msg["ret_info"])
                            msg = msg_new
        return msg

    #/\ SCREEN FUNCTIONS /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\        
 
    def showScreen(self):
        """ activates screen, its default focus panel, and updates all panels"""
        self.is_active = True

        if hasattr(self, "_on_load"):
            skip_load = False
            if hasattr(self, "_load_once"):
                if self._load_once == True and self._loaded == True:
                    skip_load = True 

            if not skip_load:
                self._loaded = True
                if self._on_load["action"] == "call_function":
                    func = getattr(self, self._on_load["action_name"])
                    func(self._on_load["action_args"])

        self.setUserStripInfo()
        self.loadPanels()
        self.openNestedPanel(self.default_focus_key)            
        self.drawPanels()
        #self.openNestedPanel(self.default_focus_key)
        #self.focusPanel(self.default_focus_key) #
        self.updatePanels()
                  
    def hideScreen(self):
        self.is_active = False      
        for panel_key in self.panels:       
            self.panels[panel_key].clearPanel()

    def reset(self):
        if hasattr(self, "_on_load"):
            self._loaded = False
        for p_key in self.panels:
            self.panels[p_key].reset()

    def setUserStripInfo(self):
        """ shows user info (name, etc...) in infostrip at top of page"""
        name = ""
        pw = ""
        lang = ""
        try:        self.user_strip.win.hline(0,0,32,80)
        except:     pass
        if "log_name" in self.global_storage:
            name = copy.copy(self.global_storage["log_name"])
        if "log_pw" in self.global_storage:
            #pw = copy.copy(self.global_storage["log_pw"])
            pass
        if "log_lang" in self.global_storage:
            lang = copy.copy(self.global_storage["log_lang"])                   
            
        self.user_strip.title = ""+\
            " USERNAME: " + name[0:20].ljust(24) +\
            "CURSESDB".ljust(24) + "QLANG: "+lang[0:10]

    def drawUserStripInfo(self):                 self.user_strip.refreshPanel()
         
    #/\ PANEL FUNCTIONS  /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

    """ HOW SCREEN INTERPERETS AND APPLIES USER INPUT 
    
    navigation input:
    1. User input window from CursesDB gives Screen raw input (converted to
        string type)
    2. Screen checks if key pressed is in its key-action map
        2A. If it is, it gets an action key/string value using that key
            2Ai.  Screen checks if action key is in its action-message map
                2Aia. If it is, it generates a message from its action-
                    message map using the action key
                    2Aia.1. The Screen's response is on one of three levels:
                        "screen", "panel" and "item" level responses
                        screen: changescreen (via message to main)
                        panel:

                2Aib. If it isn't the action key goes to the focus panel
    2-----------< The screen action-message map is the 2nd arbiter >
        2B. If it isn't, the Screen returns control back to DB without
             taking any action. Thus:
    1---< The screen key-action map is the 1st arbiter in the input path >
    """

    def loadPanels(self):
        """ calls all panel load functions"""
        for i in range(0, self.panel_count):
            self.panels[self.panel_indexes[i]].load()

    def drawPanels(self):
        """ draws all panels to screen """
        for i in range(0, self.panel_count):
            self.panels[self.panel_indexes[i]].draw()

    def updatePanels(self): 
        """ flags changed panels to be redrawn to screen by curses.doupdate """
        for i in range(0, self.panel_count):
            self.panels[self.panel_indexes[i]].update()

    def getPanelByName(self, panel_name):
        """ returns panel if it's in the screen's panel collection """
        if panel_name in self.panels: return self.panels[panel_name]

    def getItemByName(self, item_name):
        for panel_key in self.panels:
            panel = self.panels[panel_key]
            if item_name in panel.items:
                return panel.items[item_name]

    #def getTextboxByName(self, textbox_name):
    #    for panel in self.panels:
    #        if item_name in panel.items:
    #            return panel.items[item_name] 

    def openNestedPanel(self, p_key):   
        if p_key != None:
            self.focusPanel(self.pushFPanel(p_key))

    def closeNestedPanel(self, keep_i_focus=False):
        old_top_key = self.popFPanel()
        if old_top_key != None:
            self.defocusPanel(old_top_key, keep_i_focus)
            self.focusPanel(self.fpanelStackTopKey())

    def pushFPanel(self, panel_key):
        """ pushes panel KEY to stack"""
        self.fpanel_key_stack.append(panel_key)
        self.fpnl_stk_ht += 1
        self.fpanel_stack_top = self.panels[panel_key]
        return panel_key #self.fpanel_stack_top

    def fpanelStackTop(self): 
        """ returns top focus panel """
        return self.panels[self.fpanel_key_stack[self.fpnl_stk_ht]]

    def fpanelStackTopKey(self): return self.fpanel_key_stack[self.fpnl_stk_ht-1]

    def popFPanel(self, reset=False):
        """ removes top focus panel and returns its KEY"""
        if self.fpnl_stk_ht > 1:       
            if reset == True:
                pass
                #top_fpanel.reset()...

            old_top_key = self.fpanelStackTopKey()
            self.fpanel_key_stack.pop()
            self.fpnl_stk_ht -= 1
            self.fpanel_stack_top = self.panels[self.fpanelStackTopKey()]
            return old_top_key
        else: return None

    def focusPanel(self, panel_key):
        """ apply focus to screen child panel """
        if panel_key not in self.panels: return

        self.focus_panel = self.panels[panel_key]
        self.focus_panel.focus()     
        self.focus_index = self.panel_indexes.index(panel_key)
        self.focus_key = panel_key
        self.is_panel_focused = True

    def defocusPanel(self, panel_key=None, keep_i_focus=False):
        """ remove focus from screen child panel """
        if panel_key not in self.panels: return 
        if panel_key != None:        fpanel = self.panels[panel_key]
        else:                              fpanel = self.focus_panel
        if fpanel != None:
            fpanel.defocus(keep_i_focus)
            self.focus_panel = None     
            self.focus_index = -1
            self.focus_key = ""
            self.is_panel_focused = False

    def prevPanel(self):
        """ defocus current panel in focus indices and focus panel after it"""
        if self.can_panel_change != True: return

        prev_focus_index = self.focus_index
        prev_focus_key   = self.focus_key
        while True:
            if self.focus_index < 0: 
                self.focus_index = 0
            else: 
                self.focus_index -= 1    
            
            if   self.focus_index == prev_focus_index: return # @ start again                                      
            elif self.focus_index == -1:
                self.focus_index  = self.panel_count - 1
            
            new_focus_key = self.panel_indexes[self.focus_index]
            if self.panels[new_focus_key].focusable == True:              
                break

        if prev_focus_index >= 0:   
            self.defocusPanel(prev_focus_key)
        self.focusPanel(new_focus_key)

    def nextPanel(self):
        """ defocus current panel in focus indices and focus panel after it"""
        if self.can_panel_change != True: return

        prev_focus_index = self.focus_index
        prev_focus_key   = self.focus_key
        while True:
            if self.focus_index < 0: 
                self.focus_index = 0
            else:                      
                self.focus_index += 1    

            if self.focus_index   == prev_focus_index: return # @ start again                                    
            elif self.focus_index == self.panel_count: 
                self.focus_index = 0
            
            new_focus_key = self.panel_indexes[self.focus_index]
            if self.panels[new_focus_key].focusable == True: break


        if prev_focus_index >= 0:             
            self.defocusPanel(prev_focus_key)
        self.focusPanel(new_focus_key)

    def scrollPanelLeft(self):
        if self.focus_key == None or self.focus_key == "":      return

        pri_fpanel = self.panels[self.focus_key]
        # does 1' panel focus item have a 2' focus panel?
        if hasattr(pri_fpanel.focus_item, "_focus_key"):
            sec_fpanel = self.panels[pri_fpanel.focus_item._focus_key]
            # if 2' focus panel of 1' panel focus item has is selected:
            if sec_fpanel.focus_item.is_selected == True:
                # check if it has a 3' focus panel
                if  hasattr(sec_fpanel.focus_item, "_focus_key"):
                    ter_fpanel = self.panels[sec_fpanel.focus_item._focus_key]
                    return      ter_focus_panel.scrollLeft()
            return      sec_fpanel.scrollLeft()
        return      pri_fpanel.scrollLeft()

    #/\ ITEM FUNCTIONS  /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/

    def prevSecondaryItem(self):
        """ switches focus to previous item in a panel
        
        target_pnl_key = the secondary panel that focus is being changed in
            if this is None, then the item focus in the screen's focused
            panel is changed
        prereq_item_key = item key in primary panel that must be focused
            in order to change the index of the secondary panel 

        """
        if self.focus_key == None or self.focus_key == "":      return

        focus_panel = self.panels[self.focus_key]
        if hasattr(focus_panel.focus_item, "_focus_key"):            
            self.panels[focus_panel.focus_item._focus_key].prevItem()

    def nextsecondaryItem(self):
        if self.focus_key == None or self.focus_key == "":      return

        focus_panel = self.panels[self.focus_key]
        # does ths focus panel have a focus panel?
        if hasattr(focus_panel.focus_item, "_focus_key"):
            sec_focus_panel = self.panels[focus_panel.focus_item._focus_key]
            #setting up selection for tertiary focus
            if sec_focus_panel.focus_item.is_selected == True:         pass 
            else:                                 sec_focus_panel.nextItem()

    def selectItem(self):
        if self.focus_key == None or self.focus_key == "":      return

        focus_panel = self.panels[self.focus_key]
        if hasattr(focus_panel.focus_item, "_focus_key"):            
            self.panels[focus_panel.focus_item._focus_key].selectItem()
        else:                             self.focus_panel.selectItem()

    def directItemSelect(self, item_key):
        item = self.getItemByName(item_key)
        #self.global_storage['log_name'] = item_key
        #self.setUserStripInfo()
        #self.drawUserStripInfo()
        msg = item.select()
        return msg

