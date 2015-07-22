import curses

class CurseScreen(object):
    """description of class"""
    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.panels = kwargs["panels"]
        self.inkeys = kwargs["inkeys"]
        self.findex = kwargs["findex"]
      
        self.isactive = False
        
    def update(self, inputc):
        if self.isactive == True:
            status = self.checkInput(inputc)
            self.updatePanels()
            return status#self.checkInput(inputc)     

    def updatePanels(self):
        for p in range(0, len(self.panels)):
            self.panels[p].update()
        
    def checkInput(self, inputc):       
        status = None                    
        if inputc in self.inkeys:
            status = self.keymap(self.inkeys[str(inputc)])
            if status == "exit":
                return status
        if self.findex >= 0:
            self.panels[self.findex].check_input(inputc)

    def keymap(self, action):
        if action == "prev":
            self.prevPanel()
        elif action == "next":
            self.nextPanel()
        elif action == "quit":
            return self.quit()

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
            self.panels[p].win.erase() # .clear()?
        if next_screen != None:
            next_screen.showScreen()

    def showScreen(self):
        self.isactive = True
        self.updatePanels()
        #for p in range(0, len(self.panels)):
        #    self.panels[p].update()#refresh() # was refresh

    def quit(self):
        return "exit"