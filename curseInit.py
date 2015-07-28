import copy
import curses
from curseScreen import CurseScreen
from cursePanel import CursePanel
from curseTextbox import CurseTextbox

import asciiart

import curseItem

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

##############################################      1       #####
############################################## INIT SCREENS #####
##############################################              #####
def init_screens(stdscr, curseScreens, inputKeys, inputKeys2, panelStyles, inwin):
###############################################################################
##                                                               INIT_SCREENS 1
##      SCREEN 0 (TITLE SCREEN)                                                   
##      
###############################################################################                                            
    curseScreens.append(CurseScreen(
        **{
            "id"            : 0,
            "name"          : "scr0",
            "panels"        : [],
            "inputkeys"     : inputKeys,
            "inputwin"      : inwin,
            "findex"        : 1,
            "canpanelchange": True,
            "stdscr"        : stdscr,
            "style"         : panelStyles["default"],
            "usestyle"      : False
        }))

###############################################################################
##                                                               INIT_SCREENS 2
##      SCREEN 2    TEST SCREEN                                                   
##      
############################################################################### 
    curseScreens.append(CurseScreen(
        **{
            "id"            : 1,
            "name"          : "scr1",
            "panels"        : [], 
            "inputkeys"     : inputKeys,
            "inputwin"      : inwin,
            "findex"        : 0,
            "canpanelchange": True,
            "stdscr"        : stdscr,
            "style"         : panelStyles["default"],
            "usestyle"      : False
        }))

###############################################################################
##                                                               INIT_SCREENS 3
##      SCREEN 2 (ACCOUNT SCREEN)                                                    
##      
############################################################################### 
    curseScreens.append(CurseScreen(
        **{
            "id"            : 2,
            "name"          : "scr2",
            "panels"        : [],
            "inputkeys"     : inputKeys,
            "inputwin"      : inwin,
            "findex"        : 5,
            "canpanelchange": False,
            "stdscr"        : stdscr,
            "style"         : panelStyles["dashscrbg"],
            "usestyle"      : True
        }))

###############################################################################
##                                                               INIT_SCREENS 3
##      SCREEN 4 (LOGIN)                                                    
##      
############################################################################### 
    curseScreens.append(CurseScreen(
        **{
            "id"            : 3,
            "name"          : "scr3",
            "panels"        : [],
            "inputkeys"     : inputKeys,
            "inputwin"      : inwin,
            "findex"        : 5,
            "canpanelchange": True,
            "stdscr"        : stdscr,
            "style"         : panelStyles["dashscrbg"],
            "usestyle"      : True
        }))

##############################################     2       ###
############################################## INIT PANELS ###
##############################################             ###
def init_panels(stdscr, curseScreens, cursePanels, panelStyles):
###############################################################################
##                                                            INIT_PANELS 1
##      SCREEN 0                                        TBP
##                                              FCS ITM TBX NFO NFT 
##      panel scr0-0 : user strip               FCS
##      panel scr0-1 : title panel              FCS ITM TBX
##      panel scr0-2 : title_infobox panel              TBX  
##
###############################################################################
    cursePanels.append([
    ##      panel scr0-0 : user strip           FCS
    CursePanel(**{
    "id"            : -1, 
    "name"          : "user_strip",
    "parent"        : curseScreens[0],
    "h"             : 1,
    "w"             : 80,
    "y"             : 0, 
    "x"             : 0,
    "titleyx"       : (0,0),
    "title"         : "",
    "textbox"       : None,
    "style"         : panelStyles["user_strip"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False}),

    ##      panel scr0-1 : title panel          FCS ITM TBX
    CursePanel(**{
    "id"            : -1, 
    "name"          : "title panel",
    "parent"        : curseScreens[0],
    "h"             : 22, 
    "w"             : 80, 
    "y"             : 1,  
    "x"             : 0, 
    "textbox"       : CurseTextbox(**{
        "y": 3,  
        "x": 9, 
        "h": 10, 
        "w": 63,
        "style": panelStyles["title_panel"]}),
    "titleyx"       : (1,0),
    "title"         : "",
    "style"         : panelStyles["title_panel"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : True}),

    ##      panel scr0-2 : title_infobox panel          TBX
    CursePanel(**{
    "id"            : -1, 
    "name"          : "title_infobox",
    "parent"        : curseScreens[0],
    "h"             : 1, 
    "w"             : 78,
    "y"             : 21, 
    "x"             : 1,
    "textbox"       : CurseTextbox(**{
        "y": 0, 
        "x": 0, 
        "h": 1, 
        "w": 78,
        "style": panelStyles["infobox2"]}),
    "titleyx"       : (0,0),
    "title"         : "",
    "style"         : panelStyles["infobox2"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False})
    ])

###############################################################################
##                                                            INIT_PANELS 1
##      SCREEN 1                                        TBP
##                                              FCS ITM TBX NFO NFT 
##      panel scr1-0 : user strip               FCS     
##      panel scr1-1 : infobox panel 1                  TBP
##      panel scr1-2 : left middle panel        FCS
##      panel scr1-3 : right middle panel       FCS ITM
##      panel scr1-4 : infobox 2 panel                 TBX
##      panel scr1-5 : input strip                      
##
###############################################################################

    cursePanels.append([
    ##      panel scr1-0 : user_strip           FCS
    CursePanel(**{
    "id"            : -1, 
    "name"          : "user_strip",
    "parent"        : curseScreens[1],
    "h"             : 1,
    "w"             : 80,
    "y"             : 0, 
    "x"             : 0,
    "titleyx"       : (0,0),
    "title"         : "",
    "textbox"       : None,
    "style"         : panelStyles["user_strip"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : True}),
     
    ##      panel scr1-1: infobox panel 1               TBP
    CursePanel(**{
    "id"            : -1, 
    "name"          : "infobox1",
    "parent"        : curseScreens[1],
    "h"             : 5,
    "w"             : 80,
    "y"             : 1, 
    "x"             : 0,
    "textbox"       : CurseTextbox(**{"y": 1, "x": 4, "h": 3, "w": 72,
        "style" : panelStyles["infobox1"]}),
    "titleyx"       : (0,1),
    "title"         : "(INFOBOX 1)",
    "style"         : panelStyles["infobox1"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False}),

    ##      panel scr1-2: left middle panel     FCS
    CursePanel(**{
    "id"            : -1, 
    "name"          : "middle1",
    "parent"        : curseScreens[1],
    "h"             : 12,
    "w"             : 20,
    "y"             : 6, 
    "x"             : 0,
    "textbox"       : None,
    "titleyx"       : (0,1),
    "title"         : "(LEFT MAIN PANE)",
    "style"         : panelStyles["middlepanes"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : True}),

    ##      panel scr1-3: right middle panel    FCS ITM
    CursePanel(**{
    "id"            : -1, 
    "name"          : "middle2",
    "parent"        : curseScreens[1],
    "h"             : 12,
    "w"             : 69,
    "y"             : 6, 
    "x"             : 20,
    "textbox"       : None,
    "titleyx"       : (0,1),
    "title"         : "(RIGHT MAIN PANE)",
    "style"         : panelStyles["middlepanes"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : True}),

    ##      panel scr1-4: infobox panel 2               TBX
    CursePanel(**{
    "id"            : -1, 
    "name"          : "infobox2",
    "parent"        : curseScreens[1],
    "h"             : 4,
    "w"             : 80,
    "y"             : 18, 
    "x"             : 0,
    "textbox"       : CurseTextbox(**{
        "y": 0, 
        "x": 1, 
        "h": 3, 
        "w": 74,
        "style": panelStyles["infobox2"]}),
    "titleyx"       : (0,0),
    "title"         : "",
    "style"         : panelStyles["infobox2"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False}),

    ##      panel scr1-5: input strip 
    CursePanel(**{
    "id"            : -1, 
    "name"          : "input_strip",
    "parent"        : curseScreens[1],
    "h"             : 1,
    "w"             : 80,
    "y"             : 22, 
    "x"             : 0,
    "textbox"       : None,
    "titleyx"       : (0,1),
    "title"         : "(TYPED USER INPUT CAN GO HERE?)", 
    "style"         : panelStyles["input_strip"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False})
    ]) 

###############################################################################
##                                                            INIT_PANELS 2
##      SCREEN 2                                        TBP
##                                              FCS ITM TBX NFO NFT 
##      panel scr2-0 :  user strip                      
##      panel scr2-1 :  UL art panel                    TBX
##      panel scr2-2 :  LL art panel                    TBX
##      panel scr2-3 :  UR art panel                    TBX
##      panel scr2-4 :  LR art panel                    TBX
##      panel scr2-5 :  middle option menu      FCS ITM
##      panel scr2-6 :  infobox                         TBX
##            
###############################################################################
                      
    cursePanels.append([
    ##      panel scr2-0 : user strip    
    CursePanel(**{
    "id"            : -1, 
    "name"          : "user_strip",
    "parent"        : curseScreens[2],
    "h"             : 1,
    "w"             : 80,
    "y"             : 0, 
    "x"             : 0,
    "titleyx"       : (0,2),
    "title"         : "",
    "textbox"       : None,
    "style"         : panelStyles["user_strip"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False}),

    ##      panel scr2-1 : UL art panel                 TBX
    CursePanel(**{
    "id"            : -1, 
    "name"          : "UL panel",
    "parent"        : curseScreens[2],
    "h"             : 13, 
    "w"             : 31, 
    "y"             : 1,  
    "x"             : 0, 
    "textbox"       : CurseTextbox(**{
        "y": 0, 
        "x": 0,  
        "h": 13, 
        "w": 30,
        "style": panelStyles["dashscrbg"]}),
    "titleyx"       : (1,0),
    "title"         : "",
    "style"         : panelStyles["dashscrbg"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False}),

    ##      panel scr2-2 : LL art panel                 TBX
    CursePanel(**{
    "id"            : -1, 
    "name"          : "LL panel",
    "parent"        : curseScreens[2],
    "h"             : 13, 
    "w"             : 31, 
    "y"             : 12, 
    "x"             : 0, 
    "textbox"       : CurseTextbox(**{
        "y": 0,  
        "x": 0, 
        "h": 12, 
        "w": 31,
        "style": panelStyles["dashscrbg"]}),
    "titleyx"       : (1,0),
    "title"         : "",
    "style"         : panelStyles["dashscrbg"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False}),

    ##      panel scr2-3 : UR art panel                 TBX
    CursePanel(**{
    "id"            : -1, 
    "name"          : "UR panel",
    "parent"        : curseScreens[2],
    "h"             : 13, 
    "w"             : 31, 
    "y"             : 1,   
    "x"             : stdscr.getmaxyx()[1] - 29, 
    "textbox"       : CurseTextbox(**{
        "y": 0,  
        "x": 0, 
        "h": 12, 
        "w": 31,
        "style": panelStyles["dashscrbg"]}),
    "titleyx"       : (1,0),
    "title"         : "",
    "style"         : panelStyles["dashscrbg"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False}),

    ##      panel scr2-4 : LR art panel                 TBX
    CursePanel(**{
    "id"            : -1, 
    "name"          : "LR panel",
    "parent"        : curseScreens[2],
    "h"             : 13, 
    "w"             : 31, 
    "y"             : 12,   
    "x"             : stdscr.getmaxyx()[1] - 29, 
    "textbox"       : CurseTextbox(**{
        "y": 0,   
        "x": 0,  
        "h": 12, 
        "w": 31,
        "style": panelStyles["dashscrbg"]}),
    "titleyx"       : (1,0),
    "title"         : "",
    "style"         : panelStyles["dashscrbg"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False}),

    ##      panel scr2-5: middle option menu    FCS ITM TBX
    CursePanel(**{
    "id"            : -1, 
    "name"          : "mid itemlist",
    "parent"        : curseScreens[2],
    "h"             : 8, 
    "w"             : 22, 
    "y"             : 1,  
    "x"             : 29,
    "textbox"       : None,
    "titleyx"       : (2,2),
    "title"         : "ACCOUNT CREATION",
    "style"         : panelStyles["middlepanes"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : True}),

    ##      panel scr2-6: infobox                       TBX
    CursePanel(**{
    "id"            : -1, 
    "name"          : "infobox",
    "parent"        : curseScreens[2],
    "h"             : 6,
    "w"             : 22,
    "y"             : 17, 
    "x"             : 29,
    "textbox"       : CurseTextbox(**{
        "y": 1, 
        "x": 1, 
        "h": 5, 
        "w": 20,
        "style": panelStyles["infobox2"]}),
    "titleyx"       : (0,0),
    "title"         : "",
    "style"         : panelStyles["infobox2"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False}),

    ##      panel scr2-7: entrytar infobox              TBX
    CursePanel(**{
    "id"            : -1, 
    "name"          : "entrybox",
    "parent"        : curseScreens[2],
    "h"             : 1,
    "w"             : 20,
    "y"             : 12, 
    "x"             : 30,
    "textbox"       : None,
    "titleyx"       : (0,0),
    "title"         : "",
    "style"         : panelStyles["input_strip2"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False})
    ])

###############################################################################
##                                                            INIT_PANELS 3
##      SCREEN 3                                        TBP
##                                              FCS ITM TBX NFO NFT 
##      panel scr3-0 :  user strip                      
##      panel scr3-1 :  bg art panel                    TBX
##      panel scr3-2 :  team panel                      TBX            
##      panel scr3-3 :  info panel                      
##
###############################################################################

    cursePanels.append([
    ##      panel scr3-0 : user strip    
    CursePanel(**{
    "id"            : -1, 
    "name"          : "user_strip",
    "parent"        : curseScreens[3],
    "h"             : 1,
    "w"             : 80,
    "y"             : 0, 
    "x"             : 0,
    "titleyx"       : (0,2),
    "title"         : "",
    "textbox"       : None,
    "style"         : panelStyles["user_strip"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False}),

    ##      panel scr3-1 : BG art panel                 TBX
    CursePanel(**{
    "id"            : -1, 
    "name"          : "BG panel",
    "parent"        : curseScreens[3],
    "h"             : 22, 
    "w"             : 62, 
    "y"             : 1,   
    "x"             : 0, 
    "textbox"       : CurseTextbox(**{
        "y": 0,   
        "x": 0,  
        "h": 21, 
        "w": 62,
        "style": panelStyles["dashscrbg"]}),
    "titleyx"       : (0,0),
    "title"         : "",
    "style"         : panelStyles["dashscrbg"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False}),

    ##      panel scr3-2 : team panel                  TBX
    CursePanel(**{
    "id"            : -1, 
    "name"          : "team panel",
    "parent"        : curseScreens[3],
    "h"             : 21, 
    "w"             : 19, 
    "y"             : 1,   
    "x"             : 61, 
    "textbox"       : CurseTextbox(**{
        "y": 6,   
        "x": 1,  
        "h": 12, 
        "w": 17,
        "style": panelStyles["middlepanes2"]}),
    "titleyx"       : (0,0),
    "title"         : "",
    "style"         : panelStyles["middlepanes2"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False}),

    ##      panel scr3-3 : info strip                  
    CursePanel(**{
    "id"            : -1, 
    "name"          : "info_strip",
    "parent"        : curseScreens[3],
    "h"             : 1,
    "w"             : 80,
    "y"             : 23, 
    "x"             : 0,
    "titleyx"       : (0,0),
    "title"         : 
        "Press Z to return to Title Screen, if you dare...".center(79),
    "textbox"       : None,
    "style"         : panelStyles["infobox2"],
    "dftstyle"      : panelStyles["default"],
    "focusable"     : False})

    ])



#############################################      3      ####
############################################# LOAD PANELS ####
#############################################             #### 
##    loads cursePanel.parent, .infotext, .infotexttar, .items
def load_panels(curseScreens, cursePanels, panelStyles):
    global teststr1
    global teststr2
###############################################################################
##                                                            LOAD_PANELS 1
##      SCREEN 0                                        TBP
##                                              FCS ITM TBX NFO NFT 
##      panel scr0-0 : user strip               FCS
##      panel scr0-1 : title panel              FCS ITM TBX
##      panel scr0-2 : title_infobox panel              TBX  
##
###############################################################################

    ##      panel scr0-0 : user strip                    
    cursePanels[0][0].load({  
    "infotext"          : "",
    "infotexttar"       : None})

    ##      panel scr0-1 : title panel              ITM
    cursePanels[0][1].load({
    "infotext"          : "",
    "infotexttar"       : None})
    cursePanels[0][1].load_items([
    ##      ITEM: LOG IN                        FCS
    {
        "parent"        : cursePanels[0][1],
        "lindex"        : 0,
        "y"             : 15, 
        "x"             : 30, 
        "listheight"    : 4,  
        "listwidth"     : 20, 
        "lbltext"       : "log in",
        "infotext"      : "",
        "infotexttar"   : None,
        "focusable"     : True,
        "onselect"      : { 
            "func_type" : "other",
            "func"      : curseScreens[0].hideScreen,
            "args"      : [curseScreens[1]],
            "rinfo" : "schg=1"}, 
        "style"         : panelStyles["title_menu"]
    },
    ##      ITEM: ACCOUNT CREATE                FCS 
    {
        "parent"        : cursePanels[0][1],
        "lindex"        : 1,
        "y"             : 16, 
        "x"             : 30, 
        "listheight"    : 4,
        "listwidth"     : 20,
        "lbltext"       : "create account",
        "infotext"      : "",
        "infotexttar"   : None,
        "focusable"     : True,
        "onselect"      : { 
            "func_type": "other",
            "func"    : curseScreens[0].hideScreen,
            "args"    : [curseScreens[2]],
            "rinfo" : "schg=2"
                            },
        "style"         : panelStyles["title_menu"]
    },
    ##      ITEM: ABOUT CURSEDB                 FCS 
    {
        "parent"        : cursePanels[0][1],
        "lindex"        : 1,
        "y"             : 17, 
        "x"             : 30, 
        "listheight"    : 4,
        "listwidth"     : 20,
        "lbltext"       : "about curseDB",
        "infotext"      : "",
        "infotexttar"   : None,
        "focusable"     : True,
        "onselect"      : { 
            "func_type": "other",
            "func"    : curseScreens[0].hideScreen,
            "args"    : [curseScreens[3]],
            "rinfo" : "schg=3"
                            },
        "style"         : panelStyles["title_menu"]
    }])     
                       
    ##      panel scr0-2 : title_infobox panel                   
    cursePanels[0][2].load({
        "infotext"          : "",
        "infotexttar"       : None})

###############################################################################
##                                                            LOAD_PANELS 1
##      SCREEN 1                                        TBP
##                                              FCS ITM TBX NFO NFT                                                  
##      panel scr1-0 : user strip  
##      panel scr1-1 : infobox panel 1                 
##      panel scr1-2 : left middle panel    
##      panel scr1-3 : right middle panel          
##      panel scr1-4 : infobox 2 panel       
##      panel scr1-5 : input strip
##
###############################################################################

    ##      panel scr1-0 : user strip                       
    cursePanels[1][0].load({
        "infotext"          : "",
        "infotexttar"       : None})

    ##      panel scr1-1: infobox panel 1                   
    cursePanels[1][1].load({
        "infotext"          : "",
        "infotexttar"       : None})

    ##      panel scr1-2: left middle panel                 NFO NFT 
    cursePanels[1][2].load({
        "infotext"          : teststr1,
        "infotexttar"       : cursePanels[1][1]})

    ##      panel scr1-3: right middle panel        ITM     NFO NFT 
    cursePanels[1][3].load({
        "infotext"          : teststr2,
        "infotexttar"       : cursePanels[1][1]})
    cursePanels[1][3].load_items([
    ##      ITEM: LIST HEADER
        {
        "parent"        : cursePanels[1][3],
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
        "style"         : cursePanels[1][3].style
        },
    ##      ITEM: ITEM1        
        {
            "parent"        : cursePanels[1][3],
            "lindex"        : 0,
            "y"             : 3, 
            "x"             : 3,
            "listheight"    : 4,
            "listwidth"     : 10,
            "lbltext"       : " item1",
            "infotext"      : "item 1 infotext",
            "infotexttar"   : cursePanels[1][4],
            "focusable"     : True,
            "onselect"      : None,
            "style"         : cursePanels[1][3].style
        },
    ##      ITEM: ITEM2
        {
            "parent"        : cursePanels[1][3],
            "lindex"        : 1,
            "y"             : 4, 
            "x"             : 3,
            "listheight"    : 4,
            "listwidth"     : 10,
            "lbltext"       : " item2",
            "infotext"      : "item 2 infotext",
            "infotexttar"   : cursePanels[1][4],
            "focusable"     : True,
            "onselect"      : None,
            "style"         : cursePanels[1][3].style
        },
    ##      ITEM: ITEM3 
        {
            "parent"        : cursePanels[1][3],
            "lindex"        : 2,
            "y"             : 5, 
            "x"             : 3,
            "listheight"    : 4,
            "listwidth"     : 10,
            "lbltext"       : " item3",
            "infotext"      : "item 3 infotext",
            "infotexttar"   : cursePanels[1][4],
            "focusable"     : True,
            "onselect"      : None,
            "style"         : cursePanels[1][3].style}]) 

    ##      panel scr1-4: infobox 2 panel               
    cursePanels[1][4].load({
        "infotext"          : "",
        "infotexttar"       : None})                               

    ##      panel scr1-5: input strip                       
    cursePanels[1][5].load({
        "infotext"          : "",
        "infotexttar"       : None})

###############################################################################
##                                                            LOAD_PANELS 2
##      SCREEN 2                                        TBP
##                                              FCS ITM TBX NFO NFT
##      panel scr2-0 :  user strip                      
##      panel scr2-1 :  UL art panel                TXTBOX
##      panel scr2-2 :  LL art panel                TXTBOX
##      panel scr2-3 :  UR art panel                TXTBOX
##      panel scr2-4 :  LR art panel                TXTBOX
##      panel scr2-5 :  middle option menu          FOCUS ITEMS
##      panel scr2-6 :  infobox                     TXTBOX
##                       
###############################################################################

    ##      panel scr2-0 : user strip                      
    cursePanels[2][0].load({
    "infotext"          : "",
    "infotexttar"       : None})

    ##      panel scr2-1 : 
    cursePanels[2][1].load({
    "infotext"          : "",
    "infotexttar"       : None})

    ##      panel scr2-2 : 
    cursePanels[2][2].load({
    "infotext"          : "",
    "infotexttar"       : None})

    ##      panel scr2-3 : 
    cursePanels[2][3].load({
    "infotext"          : "",
    "infotexttar"       : None})

    ##      panel scr2-4 : 
    cursePanels[2][4].load({
    "infotext"          : "",
    "infotexttar"       : None})
                        
    ##      panel scr2-5 :                        
    cursePanels[2][5].load({
    "infotext"          : "",
    "infotexttar"       : None})
    cursePanels[2][5].load_items([
    ##      ITEM: USERNAME
        {
        "parent"        : cursePanels[2][5],
        "lindex"        : -1,
        "y"             : 4, 
        "x"             : 3,
        "listheight"    : 4,
        "listwidth"     : 10,
        "lbltext"       : "USERNAME".center(16),
        "infotext"      : 
            "input name between 2 and 8 alphanumeric char "\
            "hit enter to submit",
        "infotexttar"   : cursePanels[2][6],
        "focusable"     : True, #
        "onselect"      : { 
            "func_type" : "self",
            "func"      : "get_user_string",
            "args"      : [[True, True, False, False], 
                           cursePanels[2][7], 2,8,True,0,0,False],
            "rinfo"     : "call=SETACCNT:name$"
                          },
        "style"         : cursePanels[2][5].style
        },
    ##      ITEM: PASSWORD
        {
        "parent"        : cursePanels[2][5],
        "lindex"        : -1,
        "y"             : 5, 
        "x"             : 3,
        "listheight"    : 4,
        "listwidth"     : 10,
        "lbltext"       : "PASSWORD".center(16),
        "infotext"      : 
            "input password between 2 and 8 alphanumeric chars "\
            "hit enter to submit",
        "infotexttar"   : cursePanels[2][6],
        "focusable"     : True, #
        "onselect"      : { 
            "func_type" : "self",
            "func"      : "get_user_string",
            "args"      : [[True, True, False, False], 
                           cursePanels[2][7], 2,8,True,0,0,True],
            "rinfo"     : "call=SETACCNT:pass$"
                          },
        "style"         : cursePanels[2][5].style}])

    ##      panel scr2-6 : 
    cursePanels[2][6].load({
    "infotext"          : "",
    "infotexttar"       : None})

    ##      panel scr2-7 : 
    cursePanels[2][7].load({
    "infotext"          : "",
    "infotexttar"       : None})

###############################################################################
##                                                            INIT_PANELS 3
##      SCREEN 3                                        TBP
##                                              FCS ITM TBX NFO NFT 
##      panel scr3-0 :  user strip                      
##      panel scr3-1 :  bg art panel                    TBX
##            
###############################################################################

    ##      panel scr3-0 : user strip                      
    cursePanels[3][0].load({
    "infotext"          : "",
    "infotexttar"       : None})

    ##      panel scr3-1 : 
    cursePanels[3][1].load({
    "infotext"          : "",
    "infotexttar"       : None})

    ##      panel scr3-2 : 
    cursePanels[3][2].load({
    "infotext"          : "",
    "infotexttar"       : None})

    ##      panel scr3-3 : 
    cursePanels[3][3].load({
    "infotext"          : "",
    "infotexttar"       : None})

##########################################      4         ####
########################################## LOAD TEXTBOXES ####
##########################################                #### 
def load_textboxes(cursePanels):
###############################################################################
##                                                         LOAD TEXTBOXES 0
##      SCREEN 0                                        TBP
##                                              FCS ITM TBX NFO NFT                                                        
##      panel scr0-0 : user strip                   
##      panel scr0-1 : title panel               
##      panel scr0-2 : infobox
##
###############################################################################
    cursePanels[0][1].textbox.load(cursePanels[0][1], asciiart.titlestr5)
    cursePanels[0][2].textbox.load(cursePanels[0][2], 
        "  Use keys.up and keys.down to navigate , "\
        "space to select action, x to quit ")

###############################################################################
##                                                         LOAD TEXTBOXES 1
##      SCREEN 1                                        TBP
##                                              FCS ITM TBX NFO NFT 
##      panel scr1-0 : user strip               FCS
##      panel scr1-1 : infobox panel 1                  TBP
##      panel scr1-2 : left middle panel        FCS
##      panel scr1-3 : right middle panel       FCS ITM
##      panel scr1-4 : infobox 2 panel                  TXB
##      panel scr1-5 : input strip                      
##
###############################################################################
    cursePanels[1][1].textbox.load(cursePanels[1][1])
    cursePanels[1][4].textbox.load(cursePanels[1][4], 
    "[shift + tab , tab        : -\\+ screen panel ]  [z: previous screen] "\
    "[keys.left   , keys.right : -\\+ textbox page ]  [q: quit           ] "\
    "[keys.up     , keys.down  : -\\+ panel child  ]")\

###############################################################################
##                                                         LOAD TEXTBOXES 2
##      SCREEN 2                                        TBP
##                                              FCS ITM TBX NFO NFT 
##      panel scr2-0 :  user strip                      
##      panel scr2-1 :  UL art panel                    TXB
##      panel scr2-2 :  LL art panel                    TXB
##      panel scr2-3 :  UR art panel                    TXB
##      panel scr2-4 :  LR art panel                    TXB
##      panel scr2-5 :  middle option menu      FCS ITM
##      panel scr2-6 :  infobox                         TXB
##            
###############################################################################
    cursePanels[2][1].textbox.load(cursePanels[2][1], asciiart.artstr3)
    cursePanels[2][2].textbox.load(cursePanels[2][2], asciiart.artstr3)
    cursePanels[2][3].textbox.load(cursePanels[2][3], asciiart.artstr3)
    cursePanels[2][4].textbox.load(cursePanels[2][4], asciiart.artstr3)
    cursePanels[2][6].textbox.load(cursePanels[2][6], 
        "select line and press ENTER to input name/password", True)
    
###############################################################################
##                                                            LOAD TEXTBOXES 3
##      SCREEN 3                                        TBP
##                                              FCS ITM TBX NFO NFT 
##      panel scr3-0 :  user strip                      
##      panel scr3-1 :  bg art panel                    TBX
##      panel scr3-2 :  about panel                     TBX      
##      panel scr3-3 :  info panel
##
###############################################################################
    cursePanels[3][1].textbox.load(cursePanels[3][1], asciiart.titlestr3b)
    cursePanels[3][2].textbox.load(cursePanels[3][2],
        " The CursesDB Team:"\
        " *--*-------*--* "\
        " -- Ali Payne -- "\
        " ---*-------*--- "\
        "   Josh McQueen  "\
        " ---*-------*--- "\
        "   Tyler Hadley  "\
        " *--*-------*--* ",
        True)

###############################################      5     #####################
############################################## LOAD SCREENS ####################
###############################################            ##################### 
def load_screens(cursePanels, curseScreens):
    #global inputKeys
    
    curseScreens[0].panels = cursePanels[0]
    curseScreens[1].panels = cursePanels[1]
    curseScreens[2].panels = cursePanels[2]
    curseScreens[2].panels[5].focus()             
    curseScreens[3].panels = cursePanels[3]
