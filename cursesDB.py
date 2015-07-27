import copy
#import curses.panel
import curses
import curses.ascii

import locale
import textwrap

from cursePanel import CursePanel
import curseStyle
from curseTextbox import CurseTextbox
from curseScreen import CurseScreen
import asciiart

scr1_Panels = []
scr2_Panels = []
scr3_Panels = []

curseScreens = {}
inputKeys = {}
inputWin = None

stdscr = None
screenKey = None

accountName = "BUGS"
  
teststr1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "\
          "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut "\
          "enim ad minim veniam, quis nostrud exercitation ullamco laboris "\
          "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in "\
          "reprehenderit in voluptate velit esse cillum dolore eu fugiat "\
          "nulla pariatur. Excepteur sint occaecat cupidatat non proident, "\
          "sunt in culpa qui officia deserunt mollit anim id est laborum."

teststr2 = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem "\
           "accusantium doloremque laudantium, totam rem aperiam, eaque ipsa "\
           "quae ab illo inventore veritatis et quasi architecto beatae "\
           "vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia "\
           "voluptas sit aspernatur aut odit aut fugit, sed quia "\
           "consequuntur magni dolores eos qui ratione voluptatem sequi "\
           "nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor "\
           "sit amet, consectetur, adipisci velit, sed quia non numquam eius "\
           "modi tempora incidunt ut labore et dolore magnam aliquam quaerat "\
           "voluptatem. Ut enim ad minima veniam, quis nostrum "\
           "exercitationem ullam corporis suscipit laboriosam, nisi ut "\
           "aliquid ex ea commodi consequatur? Quis autem vel eum iure "\
           "reprehenderit qui in ea voluptate velit esse quam nihil "\
           "molestiae consequatur, vel illum qui dolorem eum fugiat quo "\
           "voluptas nulla pariatur?"

instructstr = "(Shift + Tab) / (Tab) = <-/+ selected panel>... "\
"arrow keys(up/down) = <-/+ panel content item selection> ... "\
"arrow keys(left/right)... <-/+ textbox page> ... "\
# (Shift + Tab) / (Tab) = < -/+ selected panel >... arrow keys(up/down) = < -/+ panel content item selection > ... arrow keys(left/right)... < -/+ textbox page > ...
# 164

# . . . . . . . . . . . . . . . . . M A I N . . . . . . . . . . . . . . . . . . 
def cursedPyDbApp(scr):
    global curseScreens       # dictionary of curseScreens
    global screenKey          # key to active screen in screen dictionary

    global stdscr             # set panel vars dependant on other panel/screen
                              #     curses library initialization
    global inputWin           # inputWin gets user keyboard input and forwards
                              #     to active screen

    stdscr = scr               
    stdscr.refresh()            

    curses.curs_set(0)

    curseStyle.init_color_pairs()   # setup curses.color_pair() values
    curseStyle.init_style()         # setup curseStyles for use with UI objects

    init_keys()               # setup input key -> cmd dictionary, screen level
    init_panels()             # instantiate & init panels, textboxes, items
    init_screens()            # instantiate and initialize screen

    load_panels()             # load panel,item vars that ref other panel/item
    load_textboxes()          # assign textbox parents and basetext
    load_screens()            # assign panels to screens

    inputWin = curses.newwin(1,1,22,80) # input win is tucked away in LR corner
    inputWin.keypad(1) 

    screenKey = "scr1"
    curseScreens[screenKey].showScreen()
    curses.doupdate()

    # MAIN PROGRAM LOOP
    while True:
        #1      get user input
        input_i = inputWin.getch() 
        #2      give input to screen, get status codes from panels/items
        status = curseScreens[screenKey].update(input_i)
        #3      update physical screen with virtual screen
        curses.doupdate()

        #4      check for returned status codes
        if status != None:

            #4A     status code
            stat_code = status[0:3]
            #4B     status code value
            stat_val  = status[4:]

            # command:      exit program
            if stat_code == "ext":
                break
            # command:      change screen to stat_val (origin: item)
            elif stat_code == "key":
                screenKey = stat_val
                curses.ungetch(ord("u"))
                #curses.doupdate()
            # command:      change screen to stat_val (origin: curse screen)
            elif stat_code == "scr":
                screenKey = stat_val
                curses.ungetch(ord("u"))
            # command: get username
            elif stat_code == "fnc":
                if stat_val[0:8] == "SETACCNT":
                    field = stat_val[9:13]
                    fetch_status = stat_val[14:18] 
                    if fetch_status == "GOOD":
                        content = stat_val[19:]
                    else:
                        content = "empty"
                    setaccount(fetch_status, field, content)
                  
            #                            14
            #                          13 |   18
            #         0       7 8 9  12 | | 17 |19
            #         |       | | |   | | |  | | |
            # "[fnc]=[func_code]:[field]:[stat]:[content]

# . . . . . . . . . . . . . . .  M A I N . E N D . . . . . . . . . . . . . . . 
def setaccount(fetch_status, field, field_content):
    global accountName
    accountName = field_content
    scr3_Panels[0].title= accountName
    

def init_keys():
    global inputKeys
    inputKeys[str(ord("a"))]            = "prev"
    inputKeys[str(ord("d"))]            = "next"
    inputKeys[str(ord(" "))]            = "select"
    inputKeys[str(ord("\n"))]           = "return"
    inputKeys[str(ord("x"))]            = "quit"
    inputKeys[str(ord("z"))]            = "prevscr"

    inputKeys[str(curses.KEY_BTAB)]     = "back"
    inputKeys[str(ord("\t"))]           = "forward"
    inputKeys[str(curses.KEY_LEFT)]     = "left"
    inputKeys[str(curses.KEY_RIGHT)]    = "right"
    inputKeys[str(curses.KEY_UP)]       = "up"
    inputKeys[str(curses.KEY_DOWN)]     = "down"

##############################################     1      #####################
############################################# INIT PANELS  ####################
##############################################            ##################### 
def init_panels():
    global scr1_Panels
    global scr2_Panels
    global scr3_Panels
    global stdscr
    global titlestr

    ###########################################################################
    ##
    ##      #### #### ####   #### #### #   #    #          INIT PANELS
    ##      #    #    #   #  #    #    ##  #   ##          
    ##      #### #    ####   #### #### # # #    #
    ##         # #    #   #  #    #    #  ##    #
    ##      #### #### #    # #### #### #   #   ###
    ##
    ##      panel scr1-0 : user strip  
    ##      panel scr1-1 : title panel                     FOCUS ITEMS
    ##      panel scr1-2 : title_infobox panel             TXTBOX  
    ##
    ###########################################################################

    ##      panel scr1-0 : user strip                      FOCUS
    scr1_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "user_strip",
        "h"             : 1,
        "w"             : 80,
        "y"             : 0, 
        "x"             : 0,
        "titleyx"       : (0,0),
        "title"         : "",
        "textbox"       : None,
        "style"         : curseStyle.panelStyles["user_strip"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : False})) 
    ##      panel scr1-1 : title panel                     FOCUS ITEMS TXTBOX
    scr1_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "title panel",
        "h"             : 22, 
        "w"             : 80, 
        "y"             : 1,  
        "x"             : 0, 
        "textbox"       : CurseTextbox(**{
            "y": 3,  
            "x": 9, 
            "h": 10, 
            "w": 63,
            "style": curseStyle.panelStyles["title_panel"]}),
        "titleyx"       : (1,0),
        "title"         : "",
        "style"         : curseStyle.panelStyles["title_panel"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : True}))
    ##      panel scr1-2 : title_infobox panel             TXTBOX
    scr1_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "title_infobox",
        "h"             : 1, 
        "w"             : 78,
        "y"             : 21, 
        "x"             : 1,
        "textbox"       : CurseTextbox(**{
            "y": 0, "x": 0, "h": 1, "w": 78,
            "style": curseStyle.panelStyles["infobox2"]}),
        "titleyx"       : (0,0),
        "title"         : "",
        "style"         : curseStyle.panelStyles["infobox2"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : False}))

    ###########################################################################
    ##
    ##    #### #### ####   #### #### #   #     ##          INIT PANELS
    ##    #    #    #   #  #    #    ##  #    #  #
    ##    #### #    ####   #### #### # # #      #
    ##       # #    #   #  #    #    #  ##     #
    ##    #### #### #    # #### #### #   #    ####
    ##
    ##      panel scr2-0 : user strip  
    ##      panel scr2-1 : infobox panel 1                 
    ##      panel scr2-2 : left middle panel    
    ##      panel scr2-3 : right middle panel          
    ##      panel scr2-4 : infobox 2 panel       
    ##      panel scr2-5 : input strip   
    ##
    ###########################################################################

    ##      panel scr2-0 : user_strip                      FOCUS
    scr2_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "user_strip",
        "h"             : 1,
        "w"             : 80,
        "y"             : 0, 
        "x"             : 0,
        "titleyx"       : (0,0),
        "title"         : "",
        "textbox"       : None,
        "style"         : curseStyle.panelStyles["user_strip"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : True})) 
    ##      panel scr2-1: infobox panel 1                  TXTBOX
    scr2_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "infobox1",
        "h"             : 5,
        "w"             : 80,
        "y"             : 1, 
        "x"             : 0,
        "textbox"       : CurseTextbox(**{"y": 1, "x": 4, "h": 3, "w": 72,
            "style" : curseStyle.panelStyles["infobox1"]}),
        "titleyx"       : (0,1),
        "title"         : "(INFOBOX 1)",
        "style"         : curseStyle.panelStyles["infobox1"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : False}))
    ##      panel scr2-2: left middle panel                FOCUS
    scr2_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "middle1",
        "h"             : 12,
        "w"             : 20,
        "y"             : 6, 
        "x"             : 0,
        "textbox"       : None,
        "titleyx"       : (0,1),
        "title"         : "(LEFT MAIN PANE)",
        "style"         : curseStyle.panelStyles["middlepanes"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : True}))
    ##      panel scr2-3: right middle panel               FOCUS ITEMS
    scr2_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "middle2",
        "h"             : 12,
        "w"             : 69,
        "y"             : 6, 
        "x"             : 20,
        "textbox"       : None,
        "titleyx"       : (0,1),
        "title"         : "(RIGHT MAIN PANE)",
        "style"         : curseStyle.panelStyles["middlepanes"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : True}))
    ##      panel scr2-4: infobox panel 2                  TXTBOX
    scr2_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "infobox2",
        "h"             : 4,
        "w"             : 80,
        "y"             : 18, 
        "x"             : 0,
        "textbox"       : CurseTextbox(**{
            "y": 0, "x": 1, "h": 3, "w": 74,
            "style": curseStyle.panelStyles["infobox2"]}),
        "titleyx"       : (0,0),
        "title"         : "",
        "style"         : curseStyle.panelStyles["infobox2"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : False}))
    ##      panel scr2-5: input strip 
    scr2_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "input_strip",
        "h"             : 1,
        "w"             : 80,
        "y"             : 22, 
        "x"             : 0,
        "textbox"       : None,
        "titleyx"       : (0,1),
        "title"         : "(TYPED USER INPUT CAN GO HERE?)", 
        "style"         : curseStyle.panelStyles["input_strip"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : False})) 

    ###########################################################################
    ##
    ##    #### #### ####   #### #### #   #     ##          INIT PANELS
    ##    #    #    #   #  #    #    ##  #    #  #
    ##    #### #    ####   #### #### # # #      #
    ##       # #    #   #  #    #    #  ##    #  #
    ##    #### #### #    # #### #### #   #     ##
    ##
    ###########################################################################

    ##      panel scr3-0 : user strip                       FOCUS
    scr3_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "user_strip",
        "h"             : 1,
        "w"             : 80,
        "y"             : 0, 
        "x"             : 0,
        "titleyx"       : (0,0),
        "title"         : "",
        "textbox"       : None,
        "style"         : curseStyle.panelStyles["user_strip"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : False})) 
    ##      panel scr3-1 : UL art panel                     TXTBOX
    scr3_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "UL panel",
        "h"             : 13, 
        "w"             : 31, 
        "y"             : 1,  
        "x"             : 0, 
        "textbox"       : CurseTextbox(**{
            "y": 0,  #0 
            "x": 0, #0 
            "h": 13, 
            "w": 30,
            "style": curseStyle.panelStyles["dashscrbg"]}),
        "titleyx"       : (1,0),
        "title"         : "",
        "style"         : curseStyle.panelStyles["dashscrbg"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : False}))
    ##      panel scr3-2 : LL art panel                     TXTBOX
    scr3_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "LL panel",
        "h"             : 13, 
        "w"             : 31, 
        "y"             : 12, 
        "x"             : 0, 
        "textbox"       : CurseTextbox(**{
            "y": 0,  
            "x": 0, 
            "h": 12, 
            "w": 31,
            "style": curseStyle.panelStyles["dashscrbg"]}),
        "titleyx"       : (1,0),
        "title"         : "",
        "style"         : curseStyle.panelStyles["dashscrbg"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : False}))
    ##      panel scr3-3 : UR art panel                     TXTBOX
    scr3_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "UR panel",
        "h"             : 13, 
        "w"             : 31, 
        "y"             : 1,   
        "x"             : stdscr.getmaxyx()[1] - 29, 
        "textbox"       : CurseTextbox(**{
            "y": 0,  
            "x": 0, 
            "h": 12, 
            "w": 31,
            "style": curseStyle.panelStyles["dashscrbg"]}),
        "titleyx"       : (1,0),
        "title"         : "",
        "style"         : curseStyle.panelStyles["dashscrbg"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : False}))
    ##      panel scr3-4 : LR art panel                     TXTBOX
    scr3_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "LR panel",
        "h"             : 13, 
        "w"             : 31, 
        "y"             : 12,   
        "x"             : stdscr.getmaxyx()[1] - 29, 
        "textbox"       : CurseTextbox(**{
            "y": 0,   
            "x": 0,  
            "h": 12, 
            "w": 31,
            "style": curseStyle.panelStyles["dashscrbg"]}),
        "titleyx"       : (1,0),
        "title"         : "",
        "style"         : curseStyle.panelStyles["dashscrbg"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : False}))
    ##      panel scr3-5: infobox                           TXTBOX
    scr3_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "mid itemlist",
        "h"             : 15, 
        "w"             : 22, 
        "y"             : 1,  
        "x"             : 29,
        "textbox"       : None,
        "titleyx"       : (2,2),
        "title"         : " ACCOUNT CREATION",
        "style"         : curseStyle.panelStyles["middlepanes"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : True}))

    ##      panel scr3-6: infobox                           TXTBOX
    scr3_Panels.append(CursePanel(**{
        "id"            : -1, 
        "name"          : "infobox",
        "h"             : 8,
        "w"             : 22,
        "y"             : 16, 
        "x"             : 29,
        "textbox"       : CurseTextbox(**{
            "y": 1, "x": 1, "h": 7, "w": 20,
            "style": curseStyle.panelStyles["infobox2"]}),
        "titleyx"       : (0,0),
        "title"         : "",
        "style"         : curseStyle.panelStyles["infobox2"],
        "dftstyle"      : curseStyle.panelStyles["default"],
        "focusable"     : False}))

##############################################      2     #####################
############################################# INIT SCREENS ####################
##############################################            ##################### 
def init_screens():
    global scr1_Panels
    global scr2_Panels
    global scr3_Panels
    global stdscr
    global curseScreens
    global inputKeys

    #################################################
    ##
    ##      #### #### ####   #### #### #   #    #       ###  ## # ###
    ##      #    #    #   #  #    #    ##  #   ##        #   # ##  #
    ##      #### #    ####   #### #### # # #    #       ###  #  #  #
    ##         # #    #   #  #    #    #  ##    #
    ##      #### #### #    # #### #### #   #   ###      INIT SCREENS
    ##                                                 
    ##                                                  
    curseScreens["scr1"] = CurseScreen(
        **{
            "id"            : -1,
            "name"          : "scr1",
            "panels"        : [],#scr1_Panels,
            "inputkeys"     : copy.deepcopy(inputKeys),
            "findex"        : 1,
            "canpanelchange": True,
            "stdscr"        : stdscr,
            "style"         : curseStyle.panelStyles["default"],
            "usestyle"      : False
        })

    #################################################
    ##
    ##    #### #### ####   #### #### #   #     ##
    ##    #    #    #   #  #    #    ##  #    #  #
    ##    #### #    ####   #### #### # # #      #
    ##       # #    #   #  #    #    #  ##     #
    ##    #### #### #    # #### #### #   #    ####      INIT SCREENS
    ##
    curseScreens["scr2"] = CurseScreen(
        **{
            "id"            : -1,
            "name"          : "scr2",
            "panels"        : [], #scr2_Panels,
            "inputkeys"     : copy.deepcopy(inputKeys),
            "findex"        : 0,
            "canpanelchange": True,
            "stdscr"        : stdscr,
            "style"         : curseStyle.panelStyles["default"],
            "usestyle"      : False
        })

    #################################################
    ##
    ##    #### #### ####   #### #### #   #     ##
    ##    #    #    #   #  #    #    ##  #    #  #
    ##    #### #    ####   #### #### # # #      #
    ##       # #    #   #  #    #    #  ##    #  #
    ##    #### #### #    # #### #### #   #     ##       INIT SCREENS
    ##
    curseScreens["scr3"] = CurseScreen(
        **{
            "id"            : -1,
            "name"          : "scr3",
            "panels"        : [],#scr1_Panels,
            "inputkeys"     : copy.deepcopy(inputKeys),
            "findex"        : 5,
            "canpanelchange": False,
            "stdscr"        : stdscr,
            "style"         : curseStyle.panelStyles["dashscrbg"],
            "usestyle"      : True
        })

##############################################      3     #####################
############################################# LOAD PANELS  ####################
##############################################            ##################### 
## For loading: 
##      panel parents 
##      infotext
##      infotexttars
##      items
def load_panels():
    global curseScreens
    global scr1_Panels
    global scr2_Panels
    global scr3_Panels

    ###########################################################################
    ##
    ##      #### #### ####   #### #### #   #    #    #   ##
    ##      #    #    #   #  #    #    ##  #   ##    #   # #
    ##      #### #    ####   #### #### # # #    #    ### ##
    ##         # #    #   #  #    #    #  ##    #           ###  #  # #
    ##      #### #### #    # #### #### #   #   ###          ###  # ## #
    ##                                                      #    #  # ###
    ##      panel scr1-0 : user strip                   
    ##      panel scr1-1 : title panel               
    ##      panel scr1-2 : infobox
    ##
    ###########################################################################

    ##      panel scr1-0 : user strip                      FOCUS
    scr1_Panels[0].load({
        "parent"            : None,
        "infotext"          : "",
        "infotexttar"       : None})
    scr1_Panels[0].load_items([])
    ##      panel scr1-1 : title panel                     FOCUS ITEMS TXTBOX
    scr1_Panels[1].load({
        "parent"            : None,
        "infotext"          : "",
        "infotexttar"       : None})
    scr1_Panels[1].load_items([
        ##  LOG IN
        {   
            "parent"        : scr1_Panels[1],
            "lindex"        : 0,
            "y"             : 15, #12
            "x"             : 30,  #0
            "listheight"    : 4,  #4
            "listwidth"     : 20, #20
            "lbltext"       : "  log in",
            "infotext"      : "",
            "infotexttar"   : None,
            "focusable"     : True,
            "onselect"      : { 
                                "func_type" : "other",
                                "func"      : curseScreens["scr1"].hideScreen,
                                "args"      : [curseScreens["scr2"]],
                                "rinfo" : "key=scr2"
                              }, 
            "style"         : curseStyle.panelStyles["title_menu"]
        },
        ##   item 2
        {   
            "parent"        : scr1_Panels[1],
            "lindex"        : 1,
            "y"             : 16, #13 
            "x"             : 30,  #0
            "listheight"    : 4,
            "listwidth"     : 20,
            "lbltext"       : "  create account",
            "infotext"      : "",
            "infotexttar"   : None,
            "focusable"     : True,
            "onselect"      : { 
                                "func_type": "other",
                                "func"    : curseScreens["scr1"].hideScreen,
                                "args"    : [curseScreens["scr3"]],
                                "rinfo" : "scr=scr3"
                              },
            "style"         : curseStyle.panelStyles["title_menu"]
        }])
    ##      panel scr1-2 : title_infobox panel             TXTBOX      
    scr1_Panels[2].load({
        "parent"            : None,
        "infotext"          : "",
        "infotexttar"       : None})
    scr1_Panels[2].load_items([])

    ###########################################################################
    ##
    ##      #### #### ####   #### #### #   #   ##    #   ##
    ##      #    #    #   #  #    #    ##  #  #  #   #   # #
    ##      #### #    ####   #### #### # # #    #    ### ##
    ##         # #    #   #  #    #    #  ##   #            ###  #  # #
    ##      #### #### #    # #### #### #   #  ####          ###  # ## #
    ##                                                      #    #  # ###
    ##      panel scr2-0 : user strip  
    ##      panel scr2-1 : infobox panel 1                 
    ##      panel scr2-2 : left middle panel    
    ##      panel scr2-3 : right middle panel          
    ##      panel scr2-4 : infobox 2 panel       
    ##      panel scr2-5 : input strip
    ##
    ###########################################################################

    ##      panel scr2-0 : user strip                       NONE
    scr2_Panels[0].load({
        "parent"            : None,
        "infotext"          : "",
        "infotexttar"       : None})
    scr2_Panels[0].load_items([])
    ##      panel scr2-1: infobox panel 1                   TEXTBOX PAGED
    scr2_Panels[1].load({
        "parent"            : None,
        "infotext"          : "",
        "infotexttar"       : None})
    scr2_Panels[1].load_items([])
    ##      panel scr2-2: left middle panel                 TEXTTAR 
    scr2_Panels[2].load({
        "parent"            : None,
        "infotext"          : teststr1,
        "infotexttar"       : scr2_Panels[1]})
    scr2_Panels[2].load_items([])
    ##      panel scr2-3: right middle panel                TEXTTAR ITEMS
    scr2_Panels[3].load({
        "parent"            : None,
        "infotext"          : teststr2,
        "infotexttar"       : scr2_Panels[1]})
    scr2_Panels[3].load_items([{
            # item list header   
            "parent"        : scr2_Panels[3],
            "lindex"        : -1,
            "y"             : 2, 
            "x"             : 3,
            "listheight"    : 4,
            "listwidth"     : 10,
            "lbltext"       : "header",
            "infotext"      : "",
            "infotexttar"   : None,
            "focusable"     : False,
            "onselect"      : None,
            "style"         : scr2_Panels[3].style
        },{ # item 1    
            "parent"        : scr2_Panels[3],
            "lindex"        : 0,
            "y"             : 3, 
            "x"             : 3,
            "listheight"    : 4,
            "listwidth"     : 10,
            "lbltext"       : " item1",
            "infotext"      : "item 1 infotext",
            "infotexttar"   : scr2_Panels[4],
            "focusable"     : True,
            "onselect"      : None,
            "style"         : scr2_Panels[3].style
        },{ # item 2  
            "parent"        : scr2_Panels[3],
            "lindex"        : 1,
            "y"             : 4, 
            "x"             : 3,
            "listheight"    : 4,
            "listwidth"     : 10,
            "lbltext"       : " item2",
            "infotext"      : "item 2 infotext",
            "infotexttar"   : scr2_Panels[4],
            "focusable"     : True,
            "onselect"      : None,
            "style"         : scr2_Panels[3].style
        },{ # item 3   
            "parent"        : scr2_Panels[3],
            "lindex"        : 2,
            "y"             : 5, 
            "x"             : 3,
            "listheight"    : 4,
            "listwidth"     : 10,
            "lbltext"       : " item3",
            "infotext"      : "item 3 infotext",
            "infotexttar"   : scr2_Panels[4],
            "focusable"     : True,
            "onselect"      : None,
            "style"         : scr2_Panels[3].style}]) 
    ##      panel scr2-4: infobox 2 panel                   TEXTBOX
    scr2_Panels[4].load({
        "parent"            : None,
        "infotext"          : "",
        "infotexttar"       : None})                               
    scr2_Panels[4].load_items([])
    ##      panel scr2-5: input strip                       NONE
    scr2_Panels[5].load({
        "parent"            : None,
        "infotext"          : "",
        "infotexttar"       : None})
    scr2_Panels[5].load_items([])

    ###########################################################################
    ##
    ##      #### #### ####   #### #### #   #    ##    #   ##
    ##      #    #    #   #  #    #    ##  #   #  #   #   # #
    ##      #### #    ####   #### #### # # #     #    ### ##
    ##         # #    #   #  #    #    #  ##   #  #         ###  #  # #
    ##      #### #### #    # #### #### #   #    ##          ###  # ## #
    ##                                                      #    #  # ###
    ###########################################################################

    ##      panel scr3-0 : user strip                      FOCUS
    scr3_Panels[0].load({
        "parent"            : None,
        "infotext"          : "",
        "infotexttar"       : None})
    scr3_Panels[0].load_items([])
    ##      panel scr3-1 : 
    scr3_Panels[1].load({
        "parent"            : None,
        "infotext"          : "",
        "infotexttar"       : None})
    scr3_Panels[1].load_items([])
    ##      panel scr3-2 : 
    scr3_Panels[2].load({
        "parent"            : None,
        "infotext"          : "",
        "infotexttar"       : None})
    scr3_Panels[2].load_items([])
    ##      panel scr3-3 : 
    scr3_Panels[3].load({
        "parent"            : None,
        "infotext"          : "",
        "infotexttar"       : None})
    scr3_Panels[3].load_items([])
    ##      panel scr3-4 : 
    scr3_Panels[4].load({
        "parent"            : None,
        "infotext"          : "",
        "infotexttar"       : None})
    scr3_Panels[4].load_items([])                          
    ##      panel scr3-5 :                                  FOCUS ITEMS
    scr3_Panels[5].load({
        "parent"            : None,
        "infotext"          : "",
        "infotexttar"       : None})
    scr3_Panels[5].load_items([{   
        "parent"        : scr3_Panels[5],
        "lindex"        : -1,
        "y"             : 6, 
        "x"             : 3,
        "listheight"    : 4,
        "listwidth"     : 10,
        "lbltext"       : "USERNAME".center(18),
        "infotext"      : 
            "input a login name between 8 and 16 alphanumeric characters",
        "infotexttar"   : scr3_Panels[6],
        "focusable"     : True, #
        "onselect"      : { 
            "func_type": "self",
            "func"     : "get_user_string",
            "args"     : ["1100", 2, 8, True, 0, 0, False],
            "rinfo"    : "fnc=SETACT:name:"
                          },
        "style"         : scr3_Panels[5].style
        },{   
        "parent"        : scr3_Panels[5],
        "lindex"        : -1,
        "y"             : 7, 
        "x"             : 3,
        "listheight"    : 4,
        "listwidth"     : 10,
        "lbltext"       : "PASSWORD".center(18),
        "infotext"      : 
            "input a password between 8 and 16 alphanumeric characters",
        "infotexttar"   : scr3_Panels[6],
        "focusable"     : True, #
        "onselect"      : None, # write func to activate input trapper
        "style"         : scr3_Panels[5].style }])
    ##      panel scr3-6 : 
    scr3_Panels[6].load({
        "parent"            : None,
        "infotext"          : "",
        "infotexttar"       : None})
    scr3_Panels[6].load_items([])         


##############################################      4     #####################
############################################# LOAD TXTBOX   ####################
##############################################            ##################### 
def load_textboxes():
    global scr1_Panels
    global scr2_Panels
    global scr3_Panels
# (Shift + Tab) / (Tab) = < -/+ selected panel >... arrow keys(up/down) = < -/+ panel content item selection > ... arrow keys(left/right)... < -/+ textbox page > ...

    #################################################
    ##
    ##      #### #### ####   #### #### #   #    #        ### # # ### 
    ##      #    #    #   #  #    #    ##  #   ##         #   #   #  
    ##      #### #    ####   #### #### # # #    #         #  # #  #  
    ##         # #    #   #  #    #    #  ##    #
    ##      #### #### #    # #### #### #   #   ###
    ##
    scr1_Panels[1].textbox.load(scr1_Panels[1], asciiart.titlestr5)
    scr1_Panels[2].textbox.load(scr1_Panels[2], 
    "  Use keys.up and keys.down to navigate , space to select action, x to quit ")

    #################################################
    ##
    ##      #### #### ####   #### #### #   #     ##      ### # # ### 
    ##      #    #    #   #  #    #    ##  #    #  #      #   #   #  
    ##      #### #    ####   #### #### # # #      #       #  # #  # 
    ##         # #    #   #  #    #    #  ##     #
    ##      #### #### #    # #### #### #   #    ####
    ##
    scr2_Panels[1].textbox.load(scr2_Panels[1])
    scr2_Panels[4].textbox.load(scr2_Panels[4], 
    "[shift + tab , tab        : -\\+ screen panel ]  [z: previous screen] "\
    "[keys.left   , keys.right : -\\+ textbox page ]  [x: quit           ] "\
    "[keys.up     , keys.down  : -\\+ panel child  ]")\

    #################################################
    ##
    ##      #### #### ####   #### #### #   #     ##      ### # # ### 
    ##      #    #    #   #  #    #    ##  #    #  #      #   #   #  
    ##      #### #    ####   #### #### # # #      #       #  # #  #  
    ##         # #    #   #  #    #    #  ##    #  #
    ##      #### #### #    # #### #### #   #     ##
    ##
    scr3_Panels[1].textbox.load(scr3_Panels[1], asciiart.artstr3)
    scr3_Panels[2].textbox.load(scr3_Panels[2], asciiart.artstr3)
    scr3_Panels[3].textbox.load(scr3_Panels[3], asciiart.artstr3)
    scr3_Panels[4].textbox.load(scr3_Panels[4], asciiart.artstr3)
    scr3_Panels[6].textbox.load(scr3_Panels[6], 
        "select line and press ENTER to input name/password", True)

##############################################            #####################
############################################# LOAD SCREENS ####################
##############################################            ##################### 
def load_screens():
    global curseScreens
    global scr1_Panels
    global scr2_Panels
    global scr3_Panels
    #global inputKeys
    
    curseScreens["scr1"].panels = scr1_Panels
    curseScreens["scr2"].panels = scr2_Panels
    curseScreens["scr3"].panels = scr3_Panels
    curseScreens["scr3"].panels[5].focus()

def clampval(minv, maxv, v):
    return max(minv, min(maxv, v))

if __name__ == "__main__":
    # wrapper initializes curses screen settings and 
    # restores original terminal screen settings on error/close
    # wrapper is passed and calls an object 
    # that contains the main application's code
    curses.wrapper(cursedPyDbApp)