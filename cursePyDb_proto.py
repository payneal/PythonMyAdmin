import curses
import curses.panel
import curses.ascii
import locale
import pdb
import pprint
# general notes/comments ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
#
#   abbreviation key:
#       coords = coordinates
#       off = offset
#       org = origin (the upper left corner of a window is the origin)
#       par = parent
#       pnl = panel
#       rel = relative 
#       txt = text
#
#   curses "chtype":
#       curses attributes use "chtype", an int bit value that corresponds to a
#       a set of style properties:
#           unsigned <char value> | <color_pair> | <attr1> | <attr 2> | etc...
#       <attr> are constants defined in the curses libaray
#
#   ASCII codes: 
#       32 = SPACE
#       35 = #
#
# ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?


brChrSet = None
locCode = None
colors = None
cursePanels = []
panelCounter = 0
stdscr = None
styles = None

last_select_index = -1
selected_index = -1
  
# . . . . . . . . . . . . . . . . . M A I N . . . . . . . . . . . . . . . . . . 
def cursedPyDbApp(scr):
    global last_select_index
    global locCode
    global cursePanels
    global panelCounter
   
    global selected_index
    global stdscr

    locale.setlocale(locale.LC_ALL, '')
    locCode = locale.getpreferredencoding()

    stdscr = scr
    last_select_index = -1
    selected_index = -1
    
    init_color_pairs()
    init_style()
    init_panels()

    #pp = pprint.PrettyPrinter(indent=4)
    #debugstr1 = "styleobjects len: " + str(len(styleObjects)) + " "
    #debugstr1 +=  " cursePanels len " + str(len(cursePanels)) + " "
    #debugstr1 += "panelcounter " + str(panelCounter) + " "
    #stdscr.addstr(0, 0, debugstr1)
    #stdscr.addstr(1, 0, str(cursePanels[0].id))
    last_select_index = 0
    selected_index = 0
    cursePanels[selected_index].select_panel()

    for i in range (0, panelCounter):
        cursePanels[i].win.leaveok(1)
        cursePanels[i].win.noutrefresh()
    curses.doupdate()
    
    while True :
        #c = cursePanels[0].win.getch()
        c = cursePanels[selected_index].win.getch()
        if c == ord('q'):
            break
        elif c == ord('1'):
            selected_index = 0         
        elif c == ord('2'):
            selected_index = 1
        elif c == ord('3'):
            selected_index = 2
        else:       
            #for i in range(0, len(cursePanels)):
            #    cursePanels[i].updatePanel()
            #curses.doupdate()  
            continue
        if selected_index != last_select_index :
            if last_select_index != -1:
                cursePanels[last_select_index].deselect_panel()  
            cursePanels[selected_index].select_panel()
            last_select_index = selected_index 
            
        
        for j in range(0, len(cursePanels)):
            cursePanels[j].updatePanel()
        curses.doupdate()  
        #cursePanels[selected_index].select_panel()
        #cursePanels[selected_index].noutrefresh()

        # while True :
        #c = cursePanels[0].win.getch()
        #if c == ord('q'):
        #    break
        #elif c == ord('w'):
        #    selected_index = selected_index - 1
        #    if selected_index < 0 :
        #        selected_index = panelCounter - 1
        #elif c == ord('s'):
        #    selected_index = selected_index + 1
        #    if selected_index >= panelCounter :
        #        selected_index = 0
        #else:
        #    cursePanels[0].win.noutrefresh()
        #    curses.doupdate()  
        #    continue   
        #cursePanels[selected_index].select_panel()
        #cursePanels[selected_index].noutrefresh()
        #      
            
    #curses.napms(5000)  

# . . . . . . . . . . . . . . .  M A I N . E N D . . . . . . . . . . . . . . . 

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@                                                                            @
#@                      FUNCTION AND CLASS DEFINITIONS                        @
#@                                                                            @
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

#### class CursePanel #########################################################
##
##  purpose: main base object type used for display and program navigation   
##
##  __init__(self, args):   
##      args obj:  
##          CursePanel.id               int used for pnl identifier       
##          CursePanel.name             str name used for pnl identifier        
##          CursePanel.title            displayed title/header txt for pnl     
##          CursePanel.ppanel           parent panel of this panel
##          CursePanel.y                y screen coord offset from NW corner
##          CursePanel.x                x screen coord offset from NW corner                       
##          CursePanel.titlexy          yx scr                                 
##          CursePanel.focus            is panel focused             
##          CursePanel.vis              is panel visible                              
##          CursePanel.stylestr         key for styles[] for a style obj   
##          CursePanel.border           { "br_chrs", "br_attr", "br_clr" }
###############################################################################
class CursePanel(object):   
# x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x
#
#   CursePanel- 
#       initialization:                        
#           __init__
#
# x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x
    def __init__(self, **kwargs):
        global panelCounter
        global styles
        if kwargs == None:
            self.isinit = False
        else:
        # CursePanel.id ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self.id = panelCounter
            panelCounter += 1                              
        # CursePanel.name ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
            self.name = kwargs["name"]    
        # CursePanel.title ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
            self.title = kwargs["title"] 
        # CursePanel.ppanel ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self.ppanel = kwargs["ppanel"] 
        # CursePanel.xy ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self.height = kwargs["h"]
            self.width = kwargs["w"]
            self.y = kwargs["y"]
            self.x = kwargs["x"]
        # CursePanel.win ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self.win = curses.newwin(self.height, self.width, self.y, self.x)           
        # CursePanel.panel ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self.panel = curses.panel.new_panel(self.win)    
        # CursePanel.titlexy ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
            self.titlexy = kwargs["titlexy"]  
        # CursePanel.isfocused ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self.foc = kwargs["foc"]
        # CursePanel.isvisible ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self.vis = kwargs["vis"]                                
        # CursePanel.cur_style ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self.stylestr = kwargs["stylestr"]
            self.border = { 
                "chrs": list((styles[self.stylestr]).br_chrs), 
                "atr" : styles[self.stylestr].br_atr, 
                "clr" : styles[self.stylestr].br_clr }
        
            self.set_style(styles[self.stylestr])
            self.draw_title()
    
            if self.vis == False:                                     
                self.panel.hide()                                             

    def updatePanel(self):
        self.drawText()
        self.win.noutrefresh()

    def drawText(self):
        self.draw_title()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #       get_relxy   
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def get_relxy(self):                                                      
        return (self.ppanel.y - self.y, self.ppanel.x - self.x)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #       set_style                         
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def set_style(self, s_obj):                                                 
        self.set_bg(s_obj.bg_chr, s_obj.bg_atr, s_obj.bg_clr)                
        self.set_border(
            self.border["chrs"], self.border["atr"], self.border["clr"])

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #       set_bg
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def set_bg(self, bg_ch, bg_at, bg_cl):
        self.win.bkgdset(bg_ch | bg_at | bg_cl) 

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #       set_border
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def set_border(self, br_chs, br_at, br_cl):
        prebg = self.win.getbkgd()       
        #self.win.attroff(prebg)
        self.win.attron(br_at | br_cl)
        self.win.border(*br_chs)
        self.win.attroff(br_at | br_cl)
        #self.win.attron(prebg)
   
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #       draw_title
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -     
    def draw_title(self):
        self.win.addstr(
            self.titlexy[0], self.titlexy[1], self.title, curses.A_BOLD)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #       select_panel
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def select_panel(self, focus_bg=0, focus_br=0):
        global styles
        if focus_bg == 0:
            focus_bg = styles[self.stylestr].onwinfocus_bg
        if focus_br == 0:
            focus_br = styles[self.stylestr].onwinfocus_br

        self.set_bg(focus_bg["chr"], focus_bg["atr"], focus_bg["clr"])       
        self.set_border(focus_br["chrs"], focus_br["atr"], focus_br["clr"])

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #       deselect_panel
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def deselect_panel(self):
        global styles
        init_style = styles[self.stylestr]

        self.set_bg(init_style.bg_chr, init_style.bg_atr, init_style.bg_clr)       
        self.set_border(init_style.br_chrs,init_style.br_atr,init_style.br_clr)          

# . . . . E N D . . . C L A S S . . . D E F I N I T I O N . . . . . . . . . . .            


#### (class) ##### CurseStyle #################################################
##
##                                                                 
##
###############################################################################
class CurseStyle(object):
    def __init__(self, kwargs):
        self.bg_chr         = kwargs["bg_ch"]
        self.bg_atr         = kwargs["bg_at"]
        self.bg_clr         = kwargs["bg_cl"]
        self.br_chrs        = list(kwargs["br_chs"])
        self.br_atr         = kwargs["br_at"]
        self.br_clr         = kwargs["br_cl"]
        self.onwinfocus_br  = kwargs["wfocus_br"] 
        self.onwinfocus_bg  = kwargs["wfocus_bg"] 

#### (function) ###### init_style() ############################################
##
##                                                                   
##
###############################################################################
def init_style():
    global brChrSet
    global locCode
    global colors
    global styles
    
    # attrset->border?
    # attron->border?
    x = ord("x".encode(locCode))
    hsh = ord("#".encode(locCode))
    dsh = ord("-".encode(locCode))
    vln = ord("|".encode(locCode))
    sp = ord(" ".encode(locCode))
   
    brChrSet = {
        "all_hash" : [ hsh for i in range (0, 8) ],
        "all_space" : [ sp for i in range (0, 8) ],
        "all_x" : [ x for i in range (0, 8) ],
        "side_hash_top_dash" : [ hsh, hsh, dsh, dsh, hsh, hsh, hsh, hsh ],
        "w_s_hash_n_dash_e_vline" : [ hsh, vln, dsh, hsh, hsh, dsh, hsh, vln]}

    styles = {}
    styles["default"] = CurseStyle(
            {
                "bg_ch" : sp,
                "bg_at" : 0,
                "bg_cl" : colors["BLU"],
                "br_chs": list(brChrSet["all_space"]),
                "br_at" : curses.A_REVERSE,
                "br_cl" : colors["BLU"],
                "wfocus_bg" : { 
                    "chr": sp, 
                    "atr": 0, 
                    "clr": colors["BLU"] },
                "wfocus_br" : { 
                    "chrs": list(brChrSet["all_space"]), 
                    "atr": curses.A_REVERSE, 
                    "clr": colors["RED"] }
            })

    styles["style1"] = CurseStyle(
            {
                "bg_ch" : sp,
                "bg_at" : 0,
                "bg_cl" : colors["BLU"],
                "br_chs": list(brChrSet["w_s_hash_n_dash_e_vline"]),
                "br_at" : 0,
                "br_cl" : colors["BLU"],
                "wfocus_bg" : { 
                    "chr": sp, 
                    "atr": 0, 
                    "clr": colors["BLU"] },
                "wfocus_br" : { 
                    "chrs": list(brChrSet["w_s_hash_n_dash_e_vline"]), 
                    "atr": 0, 
                    "clr": colors["RED"] }
            })

#### function init_color_pairs() ###############################################
##
## purpose: set the curses.color_pair() collection to specific FG/BG colors                                                                  
##
################################################################################
def init_color_pairs():
    global colors
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)  # black / black
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)   # blue  / black
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # cyan  / black
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)  # green / black
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)# mgnta / black
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)    # red   / black
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK) # yllw  / black

    colors = {  "BLK": curses.color_pair(1), "BLU": curses.color_pair(2),
                "CYN": curses.color_pair(3), "GRN": curses.color_pair(4),
                "MGA": curses.color_pair(5), "RED": curses.color_pair(6),
                "YLW": curses.color_pair(7)}

   
#### function init_panels() ####################################################
##
## purpose: instantiate and initialize CursePanels                                                             
##
################################################################################
def init_panels():
    kwargs = [
                {
                    "id" : -1, 
                    "name" : "test_panel1",
                    "title" : "PNL1",
                    "ppanel" : None,
                    "h" : 4,"w" : 80,"y" : 0, "x" : 0,
                    "titlexy" : (0,2),
                    "foc" : False, "vis" : True,
                    "stylestr" : "default"
                },
                {
                    "id" : -1, 
                    "name" : "test_panel2",
                    "title" : "PNL2",
                    "ppanel" : None,
                    "h" : 4,"w" : 80,"y" : 4, "x" : 0,
                    "titlexy" : (0,2),
                    "foc" : False, "vis" : True,
                    "stylestr" : "default"
                },
                {
                    "id" : -1, 
                    "name" : "test_panel3",
                    "title" : "PNL3",
                    "ppanel" : None,
                    "h" : 4,"w" : 80,"y" : 8, "x" : 0,
                    "titlexy" : (0,2),
                    "foc" : False, "vis" : True,
                    "stylestr" : "default"
                }                
             ]
    for i in range (0, len(kwargs)):
        cursePanels.append(CursePanel(**kwargs[i]))     

#### function clampval() #######################################################
##
##
##
##
################################################################################
def clampval(minv, maxv, v):
    return max(minv, min(maxv, v))


#### MAIN ######################################################################
##
## purpose: curses wrapper called, which calls the function obj that executes                                                                    
##          the main application code      
##
################################################################################
if __name__ == "__main__":
    # wrapper initializes curses screen settings and 
    # restores original terminal screen settings on error/close
    # wrapper is passed and calls an object 
    # that contains the main application's code
    curses.wrapper(cursedPyDbApp)