import copy
import curses

class CurseScreen(object):
    """description of class"""
    def __init__(self, **kwargs):
        self.global_storage     = kwargs["global_storage" ]
        self.screen_storage     = {}
        self.user_strip_str     = kwargs["user_strip"]

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

        if "default_focus_key" in kwargs: 
              self.default_focus_key = kwargs["default_focus_key"]
        else: self.default_focus_key = ""

        self.is_active          = False
        self.update_screen      = False
        
    def checkInput(self, input):
        """ checks if input triggers action in screen or its focused panel """
        if self.is_active != True: return
        if input not in self.key_action_map: return
        
        msg = None
        act_key = self.key_action_map[input]
       
        if act_key in self.act_msg_map: 
            msg = copy.deepcopy(self.act_msg_map[act_key])
        elif self.focus_panel != None: #
            msg = self.focus_panel.checkInput(act_key)

        self.readMessage(msg)
        return msg
             
    def updateScreen(self): self.updatePanels()

    def readMessage(self, msg):
        if msg == None: return
        
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

    #/\ SCREEN FUNCTIONS /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\        
 
    def showScreen(self):
        """ activates screen, its default focus panel, and updates all panels"""
        self.is_active = True

        if hasattr(self, "_on_load"):
            if self._on_load["action"] == "call_function":
                func = getattr(self, _on_load["action_name"])
                func(*_on_load["action_args"])

        self.setUserStripInfo()
        self.loadPanels()    
        self.drawPanels()
        self.focusPanel(self.default_focus_key) #
        self.updatePanels()
                  
    def hideScreen(self):
        self.is_active = False      
        for panel_key in self.panels:       
            self.panels[panel_key].clearPanel()

    def setUserStripInfo(self):
        """ shows user info (name, etc...) in infostrip at top of page"""
        if "log_name" in self.global_storage:
            name = copy.copy(self.global_storage["log_name"])
            pw = copy.copy(self.global_storage["log_pw"])
            self.user_strip.title = " USERNAME: "+name.ljust(20)+\
                "PASSWORD: "+pw.ljust(20) 

    def drawUserStripInfo(self):                 self.user_strip.refreshPanel()
         
    #/\ PANEL FUNCTIONS  /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

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
        for panel in self.panels:
            if item_name in panel.items:
                return panel.items[item_name]

    def focusPanel(self, panel_key):
        """ apply focus to screen child panel """
        if panel_key not in self.panels: return

        self.focus_panel = self.panels[panel_key]
        self.focus_panel.focus()     
        self.focus_index = self.panel_indexes.index(panel_key)
        self.focus_key = panel_key
        self.is_panel_focused = True

    def defocusPanel(self, panel_key):
        """ remove focus from screen child panel """
        if panel_key not in self.panels: return 
                                
        self.focus_panel.defocus()
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
