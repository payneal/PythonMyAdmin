import curses

class CurseScreen(object):
    """description of class"""
    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.panels = kwargs["panels"]
        self.inputkeys = kwargs["inputkeys"]
        self.findex = kwargs["findex"]  # findex is index of focused panel
      
        self.canpanelchange = kwargs["canpanelchange"]
        self.prevscr = None

        self.stdscr = kwargs["stdscr"]
        self.yx = self.stdscr.getmaxyx()

        self.inputwin = kwargs["inputwin"]
        self.win = curses.newwin(self.yx[0], self.yx[1], 0, 0)

        self.usestyle = kwargs["usestyle"]
        self.bg_ch = kwargs["style"].bg_chr
        self.bg_atr = kwargs["style"].bg_atr
        self.bg_clr = kwargs["style"].bg_clr

        self.isactive = False
        
    def update(self, input_i):

        # try to black out $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $  
        if self.usestyle == True:
            ch  = self.bg_ch
            atr = self.bg_atr
            clr = self.bg_clr
        else:
            ch  = 35
            atr = 0
            clr = curses.color_pair(1)

        self.win.attron(clr | atr)
        for l in range (0, self.yx[0]):
            self.win.hline(l, 0, ch, self.yx[1])
        self.win.attroff(clr | atr)
        self.win.refresh()
        # try to black out $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $  

        if self.isactive == True:
            status = self.checkInput(input_i) # <----------------- CHECK INPUT
            self.updatePanels()
            return status

    def updatePanels(self, force_refresh=False):
        for p in range(0, len(self.panels)):
            self.panels[p].update(force_refresh)
        
 
    def checkInput(self, input_i): # < < < < < < < < < < < < < < < < < < < < < 
        status = None
        if input_i == ord("u"):
            return status

        input_s = str(input_i)
        if input_s in self.inputkeys:
            actionstr = self.inputkeys[input_s]
        else:
            actionstr = "undefined"

        if actionstr != "undefined":
            # check for screen actions < < < < < < < < < < < < < < < < < < < < 
            status = self.screen_actions(actionstr) 
            if status != None:
                return status
            # if no screen actions, check for panel actions  < < < < < < < < < 
            if self.findex >= 0:
                status = self.panels[self.findex].check_input(actionstr)
        return status


    def screen_actions(self, action):
        if   action == "prev" or action == "back":
            self.prevPanel()
        elif action == "next" or action == "fwrd":
            self.nextPanel()
        elif action == "quit":
            return "exit"
        elif action == "pscr":
            self.hideScreen(self.prevscr)
            return "schg="+str(self.prevscr.id)

    def prevPanel(self):
        if self.canpanelchange != True:
            return

        prev_index = self.findex

        # findex = -2 : no focusable indices on screen
        # findex = -1 : focusable indices on screen, but no current focus
        while True:
            self.findex -= 1     
           
            if self.findex == prev_index:          # back @ start       
                return                             
            elif self.findex == -3:                # (-2 - 1) = -3  
                return                                   
            elif self.findex == -2:                # (-1 - 1) = -2   
                self.findex = 0                             
            elif self.findex == -1:                # was @first index, wrap
                self.findex = len(self.panels) - 1  

            if self.panels[self.findex].focusable == True:
                break               # quit looking if focusable panel found

        if prev_index >= 0:
            self.panels[prev_index].defocus()
        self.panels[self.findex].focus()

    def nextPanel(self):
        if self.canpanelchange != True:
            return

        prev_index = self.findex

        # findex = -2 : no focusable indices on screen
        # findex = -1 : focusable indices on screen, but no current focus
        while True:
            self.findex += 1     

            if self.findex == prev_index:           # back @ start 
                return                              
            elif self.findex == -1:                 # (-2 + 1) = -1
                return                              
            elif self.findex == len(self.panels):   # was @last index, wrap
                self.findex = 0                     

            if self.panels[self.findex].focusable == True:
                break               # quit looking if focusable panel found

        if prev_index >= 0:
            self.panels[prev_index].defocus()
        self.panels[self.findex].focus()


    def hideScreen(self, next_screen=None):
        self.isactive = False
        
        for p in range(0, len(self.panels)):
            self.panels[p].clear_panel()

        self.win.move(0,0)
        self.win.clrtobot()


        # try to black out 
        self.win.attron(curses.color_pair(1))
        for l in range (0, 22):
            self.win.hline(l, 0, 32, 80)
        self.win.attroff(curses.color_pair(1))

        if next_screen != None:
            next_screen.showScreen(self)

    def showScreen(self, prev_scr=None):
        self.isactive = True
        self.prevscr = prev_scr
        self.updatePanels()                         # updatePanels()