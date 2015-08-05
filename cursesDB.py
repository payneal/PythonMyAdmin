import copy
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

curse_container = {}
input_win       = None
key_action_map  = None

screen_key      = None
previous_key    = None
current_screen  = None

loop = True

account_name = "BUGS"
  
# . . . . . . . . . . . . . . . . . M A I N . . . . . . . . . . . . . . . . . . 
def cursedPyDbApp(scr):
    global curse_container
    global screen_key               # key to active screen in screen dictionary
    global input_win 
    global key_action_map
    global loop          

    input_win = curses.newwin(1,1,22,80) 
    input_win.keypad(1)
    key_action_map = init_action_map()

    curses.curs_set(0)
    curseStyle.init_color_pairs()       

    curse_container = curseInit.init_container(
        key_action_map, curseStyle.init_style())
    curse_container["global_storage"]["input_win"] = input_win

    curseInit.init_screens(curse_container)
    curseInit.init_panels(curse_container)
    curseInit.init_items(curse_container)
    curseInit.init_textboxes(curse_container)
    curseInit.load_targets(curse_container)
    curseInit.init_funcs(curse_container)
    curseInit.load_globals(curse_container)

    changeScreen("title_screen")

    # MAIN PROGRAM LOOP
    while loop:
        curses.doupdate()
        input_i = input_win.getch()
        message = current_screen.checkInput(str(input_i))
        readMessage(message)
        current_screen.updateScreen()
                                        
# . . . . . . . . . . . . . . .  M A I N . E N D . . . . . . . . . . . . . . ..

def init_action_map():
    """ the key-action map converts raw user input into action strings"""

    key_action_map = {}
    key_action_map[str(ord("a"))]            = "prev"
    key_action_map[str(ord("d"))]            = "next"
    key_action_map[str(ord(" "))]            = "select"
    key_action_map[str(ord("\n"))]           = "return"
    key_action_map[str(ord("q"))]            = "quit"
    key_action_map[str(ord("z"))]            = "prev_scr"

    key_action_map[str(curses.KEY_BTAB)]     = "back"
    key_action_map[str(ord("\t"))]           = "forward"
    key_action_map[str(curses.KEY_LEFT)]     = "left"
    key_action_map[str(curses.KEY_RIGHT)]    = "right"
    key_action_map[str(curses.KEY_UP)]       = "up"
    key_action_map[str(curses.KEY_DOWN)]     = "down"

    key_action_map[str(curses.KEY_DC)]           = "delete"

    return key_action_map

def readMessage(msg):
    if msg == None: return
        
    if msg["msg_status"] == "unread":
        if msg["recv_layer"] == "main" or msg["recv_layer"] == "self":
            if msg["on_recv"] == "call_function":
                func = globals()[msg["recv_act"]]

                if msg["recv_args"] == None:           
                    msg["ret_info"] = func()
                else:                 
                    msg["ret_info"] = func(*msg["recv_args"])
                msg["msg_status"] = "read"

def quitCurses():
    global loop
    loop = False

def changeScreen(new_key_str):
    """ changes current view to new screen """
    global curse_container
    global current_screen
    global screen_key
    global previous_key

    if current_screen != None:                      
        current_screen.hideScreen()

    if new_key_str == "_previous":
        if previous_key != None:                     
            new_key_str = previous_key

    current_screen = curse_container["screens"][new_key_str]
    current_screen.showScreen()     

    if previous_key != None:                         
        previous_key = screen_key
    else:                                                
        previous_key = "none"

    screen_key = new_key_str

def clampval(minv, maxv, v):
    return max(minv, min(maxv, v))

if __name__ == "__main__":
    # wrapper initializes curses screen settings and 
    # restores original terminal screen settings on error/close
    # wrapper is passed and calls an object 
    # that contains the main application's code
    curses.wrapper(cursedPyDbApp)