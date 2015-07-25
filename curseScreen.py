import curses

class CurseScreen(object):
    """description of class"""
    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.panels = kwargs["panels"]
        self.inputkeys = kwargs["inputkeys"]
        self.findex = kwargs["findex"]  # findex is index of focused panel
      
        self.prevscr = None
        self.stdscr = kwargs["stdscr"]
        self.win = curses.newwin(22, 80, 0, 0)
        self.isactive = False
        
    def update(self, inputc):
        self.win.attron(curses.color_pair(1))
        for l in range (0, 22):
            self.stdscr.hline(l, 0, 32, 80)
        self.win.attroff(curses.color_pair(1))

        if self.isactive == True:
            status = self.checkInput(inputc) # <-------------------- get status
            self.updatePanels()
            return status # <------------------------------------ RETURN status

    def updatePanels(self, force_refresh=False):
        for p in range(0, len(self.panels)):
            self.panels[p].update(force_refresh)
        
    def checkInput(self, inputc):       
        status = None                    
        if inputc in self.inputkeys:
            status = self.keymap(self.inputkeys[str(inputc)]) # <-stat from scr
            if status != None:
                if status == "ext":
                    return status # <------------ RETURN status from screen cmd
                elif status[0:3] == "scr":
                    return status # <------------ RETURN status from screen cmd
        if self.findex >= 0:
            return self.panels[self.findex].check_input(inputc) # <-stat fm itm

    def keymap(self, action):
        if action == "prev":
            self.prevPanel()
        elif action == "next":
            self.nextPanel()
        elif action == "quit":
            return self.quit()
        elif action == "prevscr":
            self.hideScreen(self.prevscr)
            return "scr="+self.prevscr.name

    def prevPanel(self):
        prev_index = self.findex

        # findex = -2 : no focusable indices on screen
        # findex = -1 : focusable indices on screen, but no current focus
        while True:
            self.findex -= 1     
           
            if self.findex == prev_index:                
                return                             # back @ start 
            elif self.findex == -3:               
                return                             # (-2 - 1) = -3        
            elif self.findex == -2:                
                self.findex = 0                    # (-1 - 1) = -2            
            elif self.findex == -1:                
                self.findex = len(self.panels) - 1 # was @first index, wrap 

            if self.panels[self.findex].focusable == True:
                break               # quit looking if focusable panel found

        if prev_index >= 0:
            self.panels[prev_index].defocus()
        self.panels[self.findex].focus()

    def nextPanel(self):
        prev_index = self.findex
        # findex = -2 : no focusable indices on screen
        # findex = -1 : focusable indices on screen, but no current focus
        while True:
            self.findex += 1     

            if self.findex == prev_index:
                return                              # back @ start 
            elif self.findex == -1:
                return                              # (-2 + 1) = -1
            elif self.findex == len(self.panels):
                self.findex = 0                     # was @last index, wrap

            if self.panels[self.findex].focusable == True:
                break               # quit looking if focusable panel found

        if prev_index >= 0:
            self.panels[prev_index].defocus()
        self.panels[self.findex].focus()

    def hideScreen(self, next_screen=None):
        self.isactive = False
        
        for p in range(0, len(self.panels)):
            self.panels[p].clear_panel()
            #self.panels[p].panel.hide() # .clear()? -> win.erase()
        #self.stdscr.clear()
        #self.stdscr.refresh()
        #curses.doupdate()
        self.win.attron(curses.color_pair(1))
        for l in range (0, 22):
            self.win.hline(l, 0, 32, 80)
        self.win.attroff(curses.color_pair(1))

        if next_screen != None:
            next_screen.showScreen(self)

    def showScreen(self, prev_scr=None):
        self.isactive = True
        self.prevscr = prev_scr
        for p in range(0, len(self.panels)):
            self.panels[p].panel.show() 
        self.updatePanels()

    def quit(self):
        return "ext"