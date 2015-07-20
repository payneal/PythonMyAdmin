import curses
import curses.panel
import curses.ascii

#import locale
import textwrap

import cursePanel
import curseStyle
import curseTextbox

#locCode = None

cursePanels = []
panelCounter = 0

stdscr = None

last_select_index = -1
selected_index = -1
  
# . . . . . . . . . . . . . . . . . M A I N . . . . . . . . . . . . . . . . . . 
def cursedPyDbApp(scr):
    global cursePanels
    global last_select_index
    #global locCode
    global panelCounter 
    global selected_index
    global stdscr

    #locale.setlocale(locale.LC_ALL, '')
    #locCode = locale.getpreferredencoding()

    last_select_index = 0
    selected_index = 0
    stdscr = scr
    
    curses.curs_set(0)
    curseStyle.init_color_pairs()
    curseStyle.init_style()
    init_panels()

    #templines = cursePanels[1].textbox.linetext#"line1 line1 line1 line2 line2 line2 line3 line3 line3 line4 line4 line4 line5 line5 line5".split()
    #for i in range(0, len(templines)):
    #    stdscr.addstr(0 + i, 0, templines[i], curses.color_pair(0))
    #stdscr.getch()
    #return

    cursePanels[selected_index].focus()

    for i in range (0, panelCounter):
        cursePanels[i].win.leaveok(0)
        cursePanels[i].update(True)
    curses.doupdate()
    
    while True :
        c = cursePanels[selected_index].win.getch()
        if c == ord('q'):
            break
        elif c == ord('1'):
            selected_index = 0         
        elif c == ord('2'):
            selected_index = 1
        elif c == ord('3'):
            selected_index = 2
        elif c == ord('4'):
            selected_index = 3
        else:        
            cursePanels[selected_index].getkeyinput(c)

        if selected_index != last_select_index :
            #if last_select_index != -1:
            cursePanels[last_select_index].defocus()  
            cursePanels[selected_index].focus()

            for j in range(0, panelCounter):
                cursePanels[j].update(True)
            
            last_select_index = selected_index                  
            curses.doupdate()

# . . . . . . . . . . . . . . .  M A I N . E N D . . . . . . . . . . . . . . . 
def init_panels():
    global panelCounter
    global cursePanels
    y = 0
    cursePanels.append(cursePanel.CursePanel(**{
                    "id" : -1, 
                    "name" : "usr_strip",
                    "ppanel" : None,
                    "h" : 1,
                    "w" : 80,
                    "y" : 0, 
                    "x" : 0,
                    "ypad" : 0,
                    "xpad" : 0,
                    "titleyx" : (0,0),
                    "title" : "",
                    "textbox" : None,
                    "infotext1" : "",
                    "infotext1tar" : None,
                    "visible" : True,
                    "style" : curseStyle.panelStyles["usr_strip"],
                    "dftstyle" : curseStyle.panelStyles["default"]}))
    cursePanels.append(cursePanel.CursePanel(**{
                    "id" : -1, 
                    "name" : "infobox1",
                    "ppanel" : None,
                    "h" : 5,
                    "w" : 80,
                    "y" : 1, 
                    "x" : 0,
                    "ypad" : 1,
                    "xpad" : 1,
                    "textbox" : {
                            "y": 1,
                            "x": 4,
                            "h": 3,
                            "w": 18,
                            "basetext": "", 
                            "style": curseStyle.panelStyles["style2"]},
                    "titleyx" : (0,0),
                    "title" : "INFOBOX1",
                    "infotext1" : "",
                    "infotext1tar" : None,
                    "visible" : True,
                    "style" : curseStyle.panelStyles["style2"],
                    "dftstyle" : curseStyle.panelStyles["default"]}))
    cursePanels.append(cursePanel.CursePanel(**{
        "id" : -1, 
        "name" : "middle1",
        "ppanel" : None,
        "h" : 13,
        "w" : 20,
        "y" : 6, 
        "x" : 0,
        "ypad": 0,
        "xpad": 0,
        "textbox" : None,
        "titleyx" : (0,2),
        "title" : "MIDDLE1",
        "infotext1" : 
            "leftmiddleline1 leftmiddleline1 leftmiddleline1 leftmiddleline1"\
            "leftmiddleline2 leftmiddleline2 leftmiddleline2 leftmiddleline2"\
            "leftmiddleline3 leftmiddleline3 leftmiddleline3 leftmiddleline3"\
            "leftmiddleline4 leftmiddleline4 leftmiddleline4 leftmiddleline4"\
            "leftmiddleline5 leftmiddleline5 leftmiddleline5 leftmiddleline5"\
            "leftmiddleline6 leftmiddleline6 leftmiddleline6 leftmiddleline6",
        "infotext1tar" : cursePanels[1],
        "visible" : True,
        "style" : curseStyle.panelStyles["style2"],
        "dftstyle" : curseStyle.panelStyles["default"]}))
    cursePanels.append(cursePanel.CursePanel(**{
        "id" : -1, 
        "name" : "middle2",
        "ppanel" : None,
        "h" : 13,
        "w" : 60,
        "y" : 6, 
        "x" : 20,
        "ypad": 0,
        "xpad": 0,
        "textbox" : None,
        "titleyx" : (0,2),
        "title" : "MIDDLE2",
        "infotext1" : 
            "rightmiddlline1 rightmiddlline1 rightmiddlline1 rightmiddlline1"\
            "rightmiddlline2 rightmiddlline2 rightmiddlline2 rightmiddlline2"\
            "rightmiddlline3 rightmiddlline3 rightmiddlline3 rightmiddlline3"\
            "rightmiddlline4 rightmiddlline4 rightmiddlline4 rightmiddlline4"\
            "rightmiddlline5 rightmiddlline5 rightmiddlline5 rightmiddlline5"\
            "rightmiddlline6 rightmiddlline6 rightmiddlline6 rightmiddlline6",
        "infotext1tar" : cursePanels[1],
        "visible" : True,
        "style" : curseStyle.panelStyles["style2"],
        "dftstyle" : curseStyle.panelStyles["default"]}))
    cursePanels.append(cursePanel.CursePanel(**{
                    "id" : -1, 
                    "name" : "infobox2",
                    "ppanel" : None,
                    "h" : 3,
                    "w" : 80,
                    "y" : 19, 
                    "x" : 0,
                    "ypad": 0,
                    "xpad": 0,
                    "textbox" : None,
                    "titleyx" : (0,1),
                    "title" : "",
                    "infotext1" : "",
                    "infotext1tar" : None,
                    "visible" : True,
                    "style" : curseStyle.panelStyles["infobox2"],
                    "dftstyle" : curseStyle.panelStyles["default"]}))
    cursePanels.append(cursePanel.CursePanel(**{
                    "id" : -1, 
                    "name" : "input_strip",
                    "ppanel" : None,
                    "h" : 1,
                    "w" : 80,
                    "y" : 22, 
                    "x" : 0,
                    "ypad": 0,
                    "xpad": 0,
                    "textbox" : None,
                    "titleyx" : (0,0),
                    "title" : "", 
                    "infotext1" : "",
                    "infotext1tar" : None,
                    "visible" : True,
                    "style" : curseStyle.panelStyles["infobox2"],
                    "dftstyle" : curseStyle.panelStyles["default"]}))
    panelCounter = len(cursePanels)

def clampval(minv, maxv, v):
    return max(minv, min(maxv, v))

if __name__ == "__main__":
    # wrapper initializes curses screen settings and 
    # restores original terminal screen settings on error/close
    # wrapper is passed and calls an object 
    # that contains the main application's code
    curses.wrapper(cursedPyDbApp)