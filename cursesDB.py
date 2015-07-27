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

import curseInit

curseScreens = []
cursePanels = []

inputKeys = {}
inputWin = None

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
    global cursePanels
    global screenKey          # key to active screen in screen dictionary
    global inputKeys
    #global stdscr             # set panel vars dependant on other panel/screen
                              #     curses library initialization
    global inputWin           # inputWin gets user keyboard input and forwards
                              #     to active screen

    stdscr = scr               
    stdscr.refresh()            

    curses.curs_set(0)

    inputWin = curses.newwin(1,1,22,80) # input win is tucked away in LR corner
    inputWin.keypad(1) 

    curseStyle.init_color_pairs()   # setup curses.color_pair() values
    curseStyle.init_style()         # setup curseStyles for use with UI objects

    init_keys()               # setup input key -> cmd dictionary, screen level

    curseInit.init_screens(stdscr, curseScreens, inputKeys, 
        curseStyle.panelStyles, inputWin)
    curseInit.init_panels(stdscr, curseScreens, cursePanels, curseStyle.panelStyles)
    curseInit.load_panels(curseScreens, cursePanels, curseStyle.panelStyles)
    curseInit.load_textboxes(cursePanels)
    curseInit.load_screens(cursePanels, curseScreens)
 
    # input win was here

    screenIndex = 0
    curseScreens[screenIndex].showScreen()
    curses.doupdate()

    # MAIN PROGRAM LOOP
    while True:
        #1      get user input
        input_i = inputWin.getch() 
        #2      give input to screen, get status codes from panels/items
        status = curseScreens[screenIndex].update(input_i)
        #3      update physical screen with virtual screen
        curses.doupdate()
        #4      check for returned status codes
        if status != None:
            stat_code = status[0:4]              #4A     status code           
            stat_val  = status[5:]               #4B     status code value
            
            if   stat_code == "exit":            # command:      exit program
                break           
            elif stat_code == "schg":            # command:      screen change
                screenIndex = int(stat_val)
                curses.ungetch(ord("u"))
            elif stat_code == "call":            # command:      call function
                if stat_val[0:8] == "SETACCNT":
                    field = stat_val[9:13]
                    fetch_status = stat_val[14:18] 
                    if fetch_status == "GOOD":
                        content = stat_val[19:]
                    else:
                        content = "FAIL"
                    setaccount(fetch_status, field, content)
                  
            #                            14
            #                          13 |   18
            #         0       7 8 9  12 | | 17 |19
            #         |       | | |   | | |  | | |
            # "[fnc]=[func_code]:[field]$[stat]:[content]

# . . . . . . . . . . . . . . .  M A I N . E N D . . . . . . . . . . . . . . . 
def setaccount(fetch_status, field, content):
    global accountName
    global cursePanels
    accountName = content
    namelen = len(accountName)
    ptitlelen = len(cursePanels[2][0].title)

    if namelen > ptitlelen:
        endr = namelen
    else:
        endr = ptitlelen

    if ptitlelen > 0:
        for r in range (0, endr):
            cursePanels[2][0].win.delch(
                cursePanels[2][0].titleyx[0],
                cursePanels[2][0].titleyx[1]+r)

    cursePanels[2][0].title= accountName
    cursePanels[2][0].draw_title()
    cursePanels[2][0].win.refresh()

    

def init_keys():
    global inputKeys
    inputKeys[str(ord("a"))]            = "prev"
    inputKeys[str(ord("d"))]            = "next"
    inputKeys[str(ord(" "))]            = "slct"
    inputKeys[str(ord("\n"))]           = "rtrn"
    inputKeys[str(ord("q"))]            = "quit"
    inputKeys[str(ord("z"))]            = "pscr"

    inputKeys[str(curses.KEY_BTAB)]     = "back"
    inputKeys[str(ord("\t"))]           = "fwrd"
    inputKeys[str(curses.KEY_LEFT)]     = "left"
    inputKeys[str(curses.KEY_RIGHT)]    = "rght"
    inputKeys[str(curses.KEY_UP)]       = "up"
    inputKeys[str(curses.KEY_DOWN)]     = "down"

def clampval(minv, maxv, v):
    return max(minv, min(maxv, v))

if __name__ == "__main__":
    # wrapper initializes curses screen settings and 
    # restores original terminal screen settings on error/close
    # wrapper is passed and calls an object 
    # that contains the main application's code
    curses.wrapper(cursedPyDbApp)