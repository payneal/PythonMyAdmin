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
        self.win = curses.newwin(self.yx[0], self.yx[1], 0, 0)

        self.usestyle = kwargs["usestyle"]
        self.bg_ch = kwargs["style"].bg_chr
        self.bg_atr = kwargs["style"].bg_atr
        self.bg_clr = kwargs["style"].bg_clr

        self.isactive = False
        
    def update(self, input_i):

        # try to black out
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

        if self.isactive == True:
            status = self.checkInput(input_i) # <-------------------- GET status
            self.updatePanels()
            return status # <------------------------------------ RETURN status

    def updatePanels(self, force_refresh=False):
        for p in range(0, len(self.panels)):
            self.panels[p].update(force_refresh)
        
    def checkInput(self, input_i):       
        status = None
        if input_i == ord("u"):
            return status

        input_s = str(input_i)
        # check input key against screen keymap                   
        if input_s in self.inputkeys:
            status = self.keymap(self.inputkeys[input_s]) # <- GET stat scr
            if status != None:
                if   status      == "ext":
                    return status # <------------ RETURN status from screen cmd
                elif status[0:3] == "scr":
                    return status # <------------ RETURN status from screen cmd
        #else:
        #    return status

        # check input against panel input dictionaries
        if self.findex >= 0:
            return self.panels[self.findex].check_input(
                self.inputkeys[input_s]) # <-stat fm itm
            #return self.panels[self.findex].check_input(inputc) # <-stat fm itm

    def keymap(self, action):
        if   action == "prev" or action == "back":
            self.prevPanel()
        elif action == "next" or action == "forward":
            self.nextPanel()
        elif action == "quit":
            return self.quit()
        elif action == "prevscr":
            self.hideScreen(self.prevscr)
            return "scr="+self.prevscr.name

    def prevPanel(self):
        if self.canpanelchange != True:
            return

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
        if self.canpanelchange != True:
            return
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
        #for p in range(0, len(self.panels)):
        #    self.panels[p].panel.show() 
        self.updatePanels()

    def quit(self):
        return "ext"