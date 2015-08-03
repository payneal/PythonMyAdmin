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
input_win = None
key_action_map = None

screen_key = None
previous_key = None
current_screen = None

input_mode = "NAV" # ( NAV, INPUT)

account_name = "BUGS"
  
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

global loop
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
    curseStyle.init_color_pairs()       # setup curses.color_pair() values

    curse_container = curseInit.init_container(
        key_action_map, curseStyle.init_style())
    curse_container["global_curseDB"]["input_win"] = input_win

    curseInit.init_screens(curse_container)
    curseInit.init_panels(curse_container)
    curseInit.init_items(curse_container)
    curseInit.init_textboxes(curse_container)
    curseInit.load_targets(curse_container)

    changeScreen("title_screen")

    # MAIN PROGRAM LOOP
    loop = True
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