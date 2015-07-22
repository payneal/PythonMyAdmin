import curses
import curses.panel
import curses.ascii

import locale
import textwrap

import cursePanel
import curseStyle
import curseTextbox
import curseScreen

import copy

#locCode = None

cursePanels = []
curseScreens = {}
inputKeys = {}
inputWin = None

#loop = False

panelCounter = 0

stdscr = None
screenKey = None
  
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

# . . . . . . . . . . . . . . . . . M A I N . . . . . . . . . . . . . . . . . . 
def cursedPyDbApp(scr):
    global cursePanels
    global curseScreens
    #global locCode
    global panelCounter 
    global screenIndex

    global stdscr
    global inputWin

    #global loop

    #locale.setlocale(locale.LC_ALL, '')
    #locCode = locale.getpreferredencoding()
    stdscr = scr
    
    curses.curs_set(0)
    curseStyle.init_color_pairs()
    curseStyle.init_style()
    init_panels()
    init_keys()
    init_screens()

    inputWin = curses.newwin(1,1,22,80)

    #loop = True
    endchar = False
    screenKey = "test_screen"
    curseScreens[screenKey].showScreen()
    curses.doupdate()

    # MAIN PROGRAM LOOP
    while True:
        inputc = inputWin.getch()
        status = curseScreens[screenKey].update(str(inputc))
        curses.doupdate()
        if status != None:
            if status == "exit":
                break

# . . . . . . . . . . . . . . .  M A I N . E N D . . . . . . . . . . . . . . . 
def init_keys():
    global inputKeys
    inputKeys[str(ord("a"))] = "prev"
    inputKeys[str(ord("d"))] = "next"
    inputKeys[str(ord(" "))] = "select"
    inputKeys[str(ord("q"))] = "quit"

def init_panels():
    global panelCounter
    global cursePanels
  
    cursePanels.append(cursePanel.CursePanel(**{
        "id" : -1, 
        "name" : "usr_strip",
        "h" : 1,
        "w" : 80,
        "y" : 0, 
        "x" : 0,
        "titleyx" : (0,0),
        "title" : "",
        "textbox" : None,
        "style" : curseStyle.panelStyles["usr_strip"],
        "dftstyle" : curseStyle.panelStyles["default"],
        "focusable" : True})) #0 user strip
    cursePanels.append(cursePanel.CursePanel(**{
        "id" : -1, 
        "name" : "infobox1",
        "h" : 5,
        "w" : 80,
        "y" : 1, 
        "x" : 0,
        "textbox" : curseTextbox.CurseTextbox(**{"y": 1, "x": 4, "h": 3, "w": 72,
            #"parent" : None,
            #"basetext": "",
            "style": curseStyle.panelStyles["infobox1"]}),
        "titleyx" : (0,1),
        "title" : "(INFOBOX 1)",
        "style" : curseStyle.panelStyles["infobox1"],
        "dftstyle" : curseStyle.panelStyles["default"],
        "focusable" : False})) #1 infobox 1
    cursePanels.append(cursePanel.CursePanel(**{
        "id" : -1, 
        "name" : "middle1",
        "h" : 12,
        "w" : 20,
        "y" : 6, 
        "x" : 0,
        "textbox" : None,
        "titleyx" : (0,1),
        "title" : "(LEFT MAIN PANE)",
        "style" : curseStyle.panelStyles["middlepanes"],
        "dftstyle" : curseStyle.panelStyles["default"],
        "focusable" : True})) #2 left mid
    cursePanels.append(cursePanel.CursePanel(**{
        "id" : -1, 
        "name" : "middle2",
        "h" : 12,
        "w" : 60,
        "y" : 6, 
        "x" : 20,
        "textbox" : None,
        "titleyx" : (0,1),
        "title" : "(RIGHT MAIN PANE)",
        "style" : curseStyle.panelStyles["middlepanes"],
        "dftstyle" : curseStyle.panelStyles["default"],
        "focusable" : True})) #3 right mid
    cursePanels.append(cursePanel.CursePanel(**{
        "id" : -1, 
        "name" : "infobox2",
        "h" : 4,
        "w" : 80,
        "y" : 18, 
        "x" : 0,
        "textbox" : curseTextbox.CurseTextbox(**{"y": 0, "x": 1, "h": 3, "w": 55,
            #"parent" : None,
            #"basetext": "testing",
            "style": curseStyle.panelStyles["infobox2"]}),
        "titleyx" : (0,0),
        "title" : "",
        "style" : curseStyle.panelStyles["infobox2"],
        "dftstyle" : curseStyle.panelStyles["default"],
        "focusable" : False})) #4 infobox 2
    cursePanels.append(cursePanel.CursePanel(**{
        "id" : -1, 
        "name" : "input_strip",
        "h" : 1,
        "w" : 80,
        "y" : 22, 
        "x" : 0,
        "textbox" : None,
        "titleyx" : (0,1),
        "title" : "(TYPED USER INPUT CAN GO HERE?)", 
        "style" : curseStyle.panelStyles["input_strip"],
        "dftstyle" : curseStyle.panelStyles["default"],
        "focusable" : False})) #5 input strip

    load_panels()
    init_textboxes()

    panelCounter = len(cursePanels)

def load_panels():
    global cursePanels

    cursePanels[0].load({
            "ppanel" : None,
            "infotext" : "",
            "infotexttar" : None,
         })
    cursePanels[1].load({
            "ppanel" : None,
            "infotext": "",
            "infotexttar" : None,
         })
    cursePanels[2].load({
            "ppanel" : None,
            "infotext" : teststr1,
            "infotexttar" : cursePanels[1]
         })
    cursePanels[3].load({
            "ppanel" : None,
            "infotext" : teststr2,
            "infotexttar" : cursePanels[1],
        })
    cursePanels[4].load({
            "ppanel" : None,
            "infotext" : "",
            "infotexttar" : None,
        })
    cursePanels[5].load({
            "ppanel" : None,
            "infotext" : "",
            "infotexttar" : None,
         })

def init_textboxes():
    global cursePanels
    cursePanels[1].textbox.load(cursePanels[1])
    cursePanels[4].textbox.load(cursePanels[4], 
        "Press \"a\" or \"d\" to move to the previous/next panel "\
        "Press \"w\" or \"s\" to flip info text pages back/forth "\
        "Press \"q\" to quit")

def init_screens():
    global cursePanels
    global curseScreens
    global inputKeys
    curseScreens["test_screen"] = curseScreen.CurseScreen(
        **{
            "id": -1,
            "name": "test screen",
            "panels": cursePanels,
            "inkeys": copy.deepcopy(inputKeys),
            "findex": 0
        })

def clampval(minv, maxv, v):
    return max(minv, min(maxv, v))

if __name__ == "__main__":
    # wrapper initializes curses screen settings and 
    # restores original terminal screen settings on error/close
    # wrapper is passed and calls an object 
    # that contains the main application's code
    curses.wrapper(cursedPyDbApp)