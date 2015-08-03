import copy
import curses

from curseScreen import CurseScreen
from cursePanel import CursePanel
from curseTextbox import CurseTextbox
from curseItem import CurseItem

import asciiart
import curseItem

layers = { "main": 0, "screen": 1, "panel": 2, "item":3 }

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

#         SEARCH INDEX: USE UNIQUE XX-XX-XX-XX CODE WITH CTRL-F TO FIND WHERE
#                       COMPONENT IS CREATED
#                                                                            ITEM
#                                                                      TEXTBOX  |
#                                                                     PANEL  |  |
# CurseScreen    | CursePanel                 | Curse   | Curse   SCREEN  |  |  |  
#                |                            | Textbox | Item         SC PA TB IT
#----------------|----------------------------|---------|--------------!!-!!-!!-!!
#-title_screen---|----------------------------|---------|--------------00-..-..-..
#----------------|-title_scr_user_strip-------|---------|--------------00-00-..-..
#----------------|-title_scr_panel------------|---------|--------------00-01-..-..
#----------------|----------------------------|(textbox)|--------------00-01-00-..
#----------------|----------------------------|---------|login_link----00-01-..-00
#----------------|----------------------------|---------|act_create_lk-00-01-..-01
#----------------|----------------------------|---------|about_DB_link-00-01-..-02
#----------------|-title_scr_infopanel--------|---------|--------------00-02-..-..
#----------------|----------------------------|(textbox)|--------------00-02-00-..
#----------------|-title_scr_background-------|---------|--------------00-03-..-..
#-test_screen----|----------------------------|---------|--------------01-..-..-..
#----------------|-test_scr_user_strip--------|---------|--------------01-00-..-..
#----------------|-test_scr_upper_infopanel---|---------|--------------01-01-..-..
#----------------|----------------------------|(textbox)|--------------01-01-00-..
#----------------|-test_scr_left_mid_panel----|---------|--------------01-02-..-..
#----------------|-test_scr_r_mid_panel-------|---------|--------------01-03-..-..
#----------------|-test_scr_lower_infopanel---|---------|--------------01-04-..-..
#----------------|----------------------------|(textbox)|--------------01-04-00-..
#----------------|-test_scr_input_strip-------|---------|--------------01-05-..-..
#-account_screen-|----------------------------|---------|--------------02-..-..-..
#----------------|-acct_scr_user_strip--------|---------|--------------02-00-..-..
#----------------|-acct_scr_NW_text_art-------|---------|--------------02-01-..-..
#----------------|----------------------------|(textbox)|--------------02-01-00-..
#----------------|-acct_scr_SW_text_art-------|---------|--------------02-02-..-..
#----------------|----------------------------|(textbox)|--------------02-02-00-..
#----------------|-acct_scr_NE_text_art-------|---------|--------------02-03-..-..
#----------------|----------------------------|(textbox)|--------------02-03-00-..
#----------------|-acct_scr_SE_text_art-------|---------|--------------02-04-..-..
#----------------|----------------------------|(textbox)|--------------02-04-00-..
#----------------|-acct_scr_mid_back_panel----|---------|--------------02-08-..-..
#----------------|-acct_scr_mid_panel---------|---------|--------------02-05-..-..
#----------------|----------------------------|---------|---username---02-05-..-00
#----------------|----------------------------|---------|---password---02-05-..-00
#----------------|-acct_scr_infobox-----------|---------|--------------02-06-..-..
#----------------|----------------------------|(textbox)|--------------02-06-00-..
#----------------|-acct_scr_input_strip-------|---------|--------------02-07-..-..
#-about_screen---|----------------------------|---------|--------------03-..-..-..
#----------------|-about_scr_user_strip-------|---------|--------------03-00-..-..
#----------------|-about_scr_bg_text_art------|---------|--------------03-01-..-..
#----------------|----------------------------|(textbox)|--------------03-01-00-..
#----------------|-about_scr_team_txt_panel---|---------|--------------03-02-..-..
#----------------|----------------------------|(textbox)|--------------03-02-00-..
#----------------|-about_scr_info_strip-------|---------|--------------03-03-..-..
#-login_screen---|----------------------------|---------|--------------04-..-..-..

#--- TITLE SCREEN: "title_screen"-----------------------------------00-..-..-..
#--- TEST SCREEN: "test_screen"-------------------------------------01-..-..-..
#--- ACCOUNT SCREEN: "account_screen"-------------------------------02-..-..-..
#--- ABOUT SCREEN: "about_screen"-----------------------------------03-..-..-..
#--- LOGIN SCREEN --------------------------------------------------04-..-..-..

def init_container(key_acts, curseStyles):
    curse_container = dict(
        key_action_map  = key_acts,
        act_msg_maps = init_act_msg_maps(),    
        styles          = curseStyles,
        screens         = {},
        global_curseDB  = {}) 
    return curse_container 

def init_screens(curse_container):
    global layers
    key_action_map      = curse_container["key_action_map"]
    curseStyles         = curse_container["styles"]
    curseScreens        = curse_container["screens"]

    default_msg_map     = curse_container["act_msg_maps"]["screen"]
    global_curseDB      = curse_container["global_curseDB"]

#"title_screen"----00-..-..-..                          
    curseScreens["title_screen"] = CurseScreen(**{
    "globals"           : global_curseDB,
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "title_scr_panel",
    "can_panel_change"  : True,
    "style"             : curseStyles["dashscrbg"]})

#"test_screen"-----01-..-..-..
    curseScreens["test_screen"] = CurseScreen(**{
    "globals"           : global_curseDB,
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "test_scr_left_mid_panel",
    "can_panel_change"  : True,
    "style"             : curseStyles["dashscrbg"]})

#"account_screen"--02-..-..-..
    curseScreens["account_screen"] = CurseScreen(**{
    "globals"           : global_curseDB,
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "acct_scr_mid_panel",
    "can_panel_change"  : False,
    "style"             : curseStyles["dashscrbg"]})
    
#"about_screen"----03-..-..-..
    curseScreens["about_screen"] = CurseScreen(**{
    "globals"           : global_curseDB,
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : None,
    "can_panel_change"  : False,
    "style"             : curseStyles["dashscrbg"]})

#"login_screen"----04-..-..-..
    pass 
    #curseScreens["login_screen"] = CurseScreen(**{
    #"parent"        : stdscr,
    #"inputkeys"     : input_keys,
    #"inputwin"      : in_win,
    #"findex"        : 5,
    #"canpanelchange": True,
    #"stdscr"        : stdscr,
    #"style"         : curseStyles["dashscrbg"],
    #"usestyle"      : True})

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def init_panels(curse_container):
    """ make the cursePanels for all curseScreens
    
    instantiate and set fields of screen child panels.
    all fields of a panel are set here EXCEPT:
        panel.items             (set in init_items)
        panel.textbox           (set in init_textboxes)
        panel.infotar           (set in load_targets)  
    """

    curseScreens = curse_container["screens"]
    curseStyles = curse_container["styles"]

    title_screen    = curseScreens["title_screen"]
    test_screen     = curseScreens["test_screen"]
    account_screen  = curseScreens["account_screen"]  
    about_screen    = curseScreens["about_screen"]  

    panel_msg_map = curse_container["act_msg_maps"]["panel_msg_map"]
    global_curseDB = curse_container["global_curseDB"]
                                                                         
#"title_screen"----00-..-..-..            
  
    # 00-03-..-..      y, x, h, w
    title_screen.panels["title_scr_background"]            = CursePanel(**{
    "globals"       : global_curseDB,
    "parent"        : title_screen,
    "size"          : (0, 0, 24, 80),   
    "style"         : curseStyles["title_panel"]})

    # 00-00-..-..
    title_screen.panels["title_scr_user_strip"]            = CursePanel(**{
    "globals"       : global_curseDB,
    "parent"        : title_screen,
    "size"          : (0, 0, 1, 80), 
    "style"         : curseStyles["user_strip"]})

    # 00-01-..-..
    title_screen.panels["title_scr_panel"]                 = CursePanel(**{
    "globals"       : global_curseDB,
    "act_msg_map"   : panel_msg_map,
    "parent"        : title_screen,
    "size"          : (1, 0, 20, 80),       
    "style"         : curseStyles["title_panel"],
    "focusable"     : True})

    # 00-02-..-..
    title_screen.panels["title_scr_infopanel"]             = CursePanel(**{
    "globals"       : global_curseDB,
    "parent"        : title_screen,
    "size"          : (21, 0, 1, 80),   
    "style"         : curseStyles["infobox2"]})

    # panels are updated/ drawn in the order below- this affects
    # overlapping panels so pay attention to this!      
    title_screen.panel_count = 4
    title_screen.panel_indexes = [
        "title_scr_background",
        "title_scr_user_strip", 
        "title_scr_panel",
        "title_scr_infopanel"]

#"test_screen"------------------------------------------------------01-..-..-..

    # 01-00-..-..      y, x, h, w
    test_screen.panels["test_scr_user_strip"]              = CursePanel(**{
    "globals": global_curseDB,
    "parent"        : test_screen,
    "size"          : (0, 0, 1, 80),  
    "style"         : curseStyles["user_strip"]})
    # 01-01-..-.. 
    test_screen.panels["test_scr_upper_infopanel"]         = CursePanel(**{
    "globals"       : global_curseDB,
    "parent"        : test_screen,    
    "size"          : (1, 0, 5, 80),
    "style"         : curseStyles["infobox1"],    
    "title"         : ("(INFOBOX 1)", 0, 1)})
    # 01-02-..-..
    test_screen.panels["test_scr_left_mid_panel"]          = CursePanel(**{
    "globals": global_curseDB,
    "parent"        : test_screen,
    "act_msg_map"   : panel_msg_map,
    "size"          : (6, 0, 12, 20),
    "style"         : curseStyles["middlepanes"],   
    "focusable"     : True,
    "title"         : ("(LEFT MAIN PANE)", 0, 1), # string, y, x  
    "info"          : teststr1,
    "infotar"       : "test_scr_upper_infopanel"})
    # 01-03-..-..
    test_screen.panels["test_scr_r_mid_panel"]             = CursePanel(**{
    "globals": global_curseDB,
    "parent"        : test_screen,
    "act_msg_map": panel_msg_map,
    "size"          : (6, 20, 12, 69), 
    "style"         : curseStyles["middlepanes"],    
    "focusable"     : True,
    "title"         : ("(RIGHT MAIN PANE)", 0, 1),
    "info"          : teststr2,
    "infotar"       : "test_scr_upper_infopanel"})
    # 01-04-..-..
    test_screen.panels["test_scr_lower_infopanel"]         = CursePanel(**{
    "globals": global_curseDB,
    "parent"        : test_screen,
    "size"          : (18, 0, 4, 80),
    "style"         : curseStyles["infobox2"]})
    # 01-05-..-..
    test_screen.panels["test_scr_input_strip"]             = CursePanel(**{
    "globals": global_curseDB,
    "parent"        : test_screen,
    "size"          : (22, 0, 1, 80),
    "style"         : curseStyles["input_strip"],    
    "title"         : ( "(TYPED USER INPUT CAN GO HERE?)", 0, 0)})
 
    # panels are updated/ drawn in the order below- this affects
    # overlapping panels so pay attention to this!                                                                       
    test_screen.panel_count = 6
    test_screen.panel_indexes = [
        "test_scr_user_strip", 
        "test_scr_upper_infopanel",
        "test_scr_left_mid_panel",
        "test_scr_r_mid_panel",
        "test_scr_lower_infopanel",
        "test_scr_input_strip"]

#"account_screen"---------------------------------------------------02-..-..-..   
                             
    # 02-00-..-..
    account_screen.panels["acct_scr_user_strip"]           = CursePanel(**{
    "globals"       : global_curseDB,
    "parent"        : account_screen,
    "size"          : (0, 0, 1, 80),  
    "style"         : curseStyles["user_strip"]})
    # 02-01-..-..
    account_screen.panels["acct_scr_NW_text_art"]          = CursePanel(**{
    "globals"       : global_curseDB,
    "parent"        : account_screen,
    "size"          : (1, 0, 13, 30),  # w.31->w.29
    "style"         : curseStyles["dashscrbg"]})
    # 02-02-..-..
    account_screen.panels["acct_scr_SW_text_art"]          = CursePanel(**{
    "globals"       : global_curseDB,
    "parent"        : account_screen,
    "size"          : (12, 0, 13, 30), # w.31->w.29
    "style"         : curseStyles["dashscrbg"]})
    # 02-03-..-..
    account_screen.panels["acct_scr_NE_text_art"]          = CursePanel(**{
    "globals"       : global_curseDB,
    "parent"        : account_screen,
    "size"          : (1, 51, 13, 30),
    "style"         : curseStyles["dashscrbg"]})
    # 02-04-..-..
    account_screen.panels["acct_scr_SE_text_art"]          = CursePanel(**{
    "globals"       : global_curseDB,
    "parent"        : account_screen,
    "size"          : (12, 51, 13, 30), 
    "style"         : curseStyles["dashscrbg"]})
    # 02-08-..-..
    account_screen.panels["acct_scr_mid_back_panel"]       = CursePanel(**{
    "globals"       : global_curseDB,
    "parent"        : account_screen,
    "size"          : (9, 29, 8, 22),
    "style"         : curseStyles["middlepanes"]})
    # 02-05-..-..
    account_screen.panels["acct_scr_mid_panel"]            = CursePanel(**{
    "globals"       : global_curseDB,
    "parent"        : account_screen,
    "act_msg_map": panel_msg_map,
    "size"          : (1, 29, 8, 22),
    "title"         : ( "ACCOUNT CREATION", 2, 3), 
    "style"         : curseStyles["middlepanes"],   
    "focusable"     : True})
    # 02-06-..-..
    account_screen.panels["acct_scr_infobox"]              = CursePanel(**{
    "globals"       : global_curseDB,
    "parent"        : account_screen,
    "size"          : (17, 29, 7, 22),
    "style"         : curseStyles["infobox2"]})
    # 02-07-..-..
    account_screen.panels["acct_scr_input_strip"]          = CursePanel(**{
    "globals"       : global_curseDB,
    "parent"        : account_screen,
    "size"          : (12, 30, 1, 20),
    "style"         : curseStyles["input_strip2"]})
    
    # panels are updated/ drawn in the order below- this affects
    # overlapping panels so pay attention to this! 
    account_screen.panel_count = 9
    account_screen.panel_indexes = [
        "acct_scr_user_strip", 
        "acct_scr_NW_text_art",
        "acct_scr_SW_text_art",
        "acct_scr_NE_text_art",
        "acct_scr_SE_text_art",
        "acct_scr_mid_back_panel",
        "acct_scr_mid_panel",
        "acct_scr_infobox",
        "acct_scr_input_strip"]
                                                                          
#"about_screen"-----------------------------------------------------03-..-..-..                                                                            
    # 03-00-..-..
    about_screen.panels["about_scr_user_strip"]               = CursePanel(**{
    "globals": global_curseDB,
    "parent"        : about_screen,
    "size"          : (0, 0, 1, 80),
    "style"         : curseStyles["user_strip"]})
    # 03-01-..-..
    about_screen.panels["about_scr_bg_text_art"]              = CursePanel(**{
    "globals": global_curseDB,
    "parent"        : about_screen,
    "size"          : (1, 0, 22, 61), # w: 62->61
    "style"         : curseStyles["dashscrbg"]})
    # 03-02-..-..
    about_screen.panels["about_scr_team_txt_panel"]          = CursePanel(**{
    "globals": global_curseDB,
    "parent"        : about_screen,
    "size"          : (1, 61, 21, 19),
    "style"         : curseStyles["middlepanes2"]})
    # 03-03-..-..
    about_screen.panels["about_scr_info_strip"]               = CursePanel(**{
    "globals": global_curseDB,
    "parent"        : about_screen,
    "size"          : (22, 0, 1, 80), # x. 23->22
    "style"         : curseStyles["infobox2"],
    "title"         : (
        "Press Z to return to Title Screen, if you dare...".center(79), 0, 0)})

    about_screen.panel_count = 4
    about_screen.panel_indexes = [
        "about_scr_user_strip", 
        "about_scr_bg_text_art",
        "about_scr_team_txt_panel",
        "about_scr_info_strip"]

#"login_screen"-----------------------------------------------------04-..-..-.. 
    pass

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def init_items(curse_container):
    """ make the curseItems for all cursePanels

    instantiate and set fields of panel child items. 
    all fields of an item are set here EXCEPT:
        item.infotar 
    """
    curseStyles         = curse_container["styles"]
    curseScreens        = curse_container["screens"]

    global_curseDB = curse_container["global_curseDB"]

    title_panels   = curseScreens["title_screen"].panels
    test_panels    = curseScreens["test_screen"].panels
    account_panels = curseScreens["account_screen"].panels
    about_scr_panels   = curseScreens["about_screen"].panels
    #login_scr_panels   = curseScreens["login_screen"].panels

    # 00-01-..-00
    title_panels["title_scr_panel"].items["login_link"] = CurseItem(**{
    "globals": global_curseDB,
    "parent"        : title_panels["title_scr_panel"],
    "size"          : (15, 30, 1, 20), # y, x, h, w
    "style"         : curseStyles["title_menu"],
    "label"         : "log in".center(20),
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "main", 
        recv_name   = "main",   
        on_recv     = "call_function", 
        recv_act    = "changeScreen",
        recv_args   = ["test_screen"],
        ret_info    = None)})
    # 00-01-..-01
    title_panels["title_scr_panel"].items["act_create_lk"] = CurseItem(**{
    "globals": global_curseDB,
    "parent"        : title_panels["title_scr_panel"],
    "size"          : (16, 30, 1, 20), # y, x, h, w
    "style"         : curseStyles["title_menu"],
    "label"         : "create account".center(20),
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "main", 
        recv_name   = "main",   
        on_recv     = "call_function", 
        recv_act    = "changeScreen",
        recv_args   = ["account_screen"],
        ret_info    = None)})
    # 00-01-..-02
    title_panels["title_scr_panel"].items["about_DB_link"] = CurseItem(**{
    "globals": global_curseDB,
    "parent"        : title_panels["title_scr_panel"],
    "size"          : (17, 30, 1, 20), # y, x, h, w
    "style"         : curseStyles["title_menu"],
    "label"         : "about curseDB".center(20),
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "main", 
        recv_name   = "main",   
        on_recv     = "call_function", 
        recv_act    = "changeScreen",
        recv_args   = ["about_screen"],
        ret_info    = None)})

    title_panels["title_scr_panel"].item_count = 3
    title_panels["title_scr_panel"].item_indexes = [
        "login_link", 
        "act_create_lk", 
        "about_DB_link"]

#"test_screen"-----01-..-..-..

    test_panels["test_scr_r_mid_panel"].items["list_hdr"]   = CurseItem(**{
    "globals": global_curseDB,
    "parent"        : test_panels["test_scr_r_mid_panel"],
    "size"          : (2, 3, 4, 10), # y, x, h, w
    "style"         : test_panels["test_scr_r_mid_panel"].style,
    "label"         : "header",
    "focusable"     : False })

    test_panels["test_scr_r_mid_panel"].items["item1"]      = CurseItem(**{
    "globals": global_curseDB,
    "parent"        : test_panels["test_scr_r_mid_panel"],
    "size"          : (3, 3, 4, 10), # y, x, h, w
    "style"         : test_panels["test_scr_r_mid_panel"].style,
    "label"         : "item1"})

    test_panels["test_scr_r_mid_panel"].items["item2"]      = CurseItem(**{
    "globals": global_curseDB,
    "parent"        : test_panels["test_scr_r_mid_panel"],
    "size"          : (4, 3, 4, 10), # y, x, h, w
    "style"         : test_panels["test_scr_r_mid_panel"].style,
    "label"         : "item2"})

    test_panels["test_scr_r_mid_panel"].items["item3"]      = CurseItem(**{
    "globals": global_curseDB,
    "parent"       : test_panels["test_scr_r_mid_panel"],
    "size"          : (5, 3, 4, 10), # y, x, h, w
    "style"         : test_panels["test_scr_r_mid_panel"].style,
    "label"         : "item3"})

    test_panels["test_scr_r_mid_panel"].item_count = 4
    test_panels["test_scr_r_mid_panel"].item_indexes = [
        "list_hdr", 
        "item1", 
        "item2",
        "item3"]

#"account_screen"--02-..-..-..
    account_panels["acct_scr_mid_panel"].items["username"]   = CurseItem(**{
    "globals": global_curseDB,
    "parent"        : account_panels["acct_scr_mid_panel"],
    "size"          : (4, 3, 4, 10), # y, x, h, w
    "style"         : account_panels["acct_scr_mid_panel"].style,
    "label"         : "USERNAME".center(16),
    "info"          : "input between 4 and 10 alphanumeric char "\
                      "press SPACE BAR to begin entry",
    "infotar"       : "acct_scr_infobox",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "getUserString",
        recv_args   = ["1100", curses.color_pair(10), 
                       account_panels["acct_scr_input_strip"].win, 
                       account_panels["acct_scr_infobox"],       
                       (0,1), 4, 18, True, False, True],
        ret_info    = None)})    

    account_panels["acct_scr_mid_panel"].items["password"]   = CurseItem(**{
    "globals": global_curseDB,
    "parent"       : account_panels["acct_scr_mid_panel"],
    "size"          : (5, 3, 4, 10), # y, x, h, w
    "style"         : account_panels["acct_scr_mid_panel"].style,
    "label"         : "PASSWORD".center(16),
    "info"          : "input between 4 and 10 alphanumeric char "\
                      "press SPACE BAR to begin entry",
    "infotar"       : "acct_scr_infobox",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "getUserString",
        recv_args   = ["1100", curses.color_pair(10), 
                       account_panels["acct_scr_input_strip"].win, 
                       account_panels["acct_scr_infobox"],       
                       (0,1), 4, 18, True, True, True],
        ret_info    = None)})

    account_panels["acct_scr_mid_panel"].item_count = 2
    account_panels["acct_scr_mid_panel"].item_indexes = [
        "username", 
        "password"]

#"about_screen"----03-..-..-..
    pass
#"login_screen"----04-..-..-.. 
    pass

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def init_textboxes(curse_container):
    title_panels   = curse_container["screens"]["title_screen"].panels
    test_panels    = curse_container["screens"]["test_screen"].panels
    account_panels = curse_container["screens"]["account_screen"].panels
    about_panels   = curse_container["screens"]["about_screen"].panels
    curse_styles    = curse_container["styles"]
    #login_panels   = curse_container["screens"]["login_screen"].panels

#"title_screen"-----------------------------------------------------00-..-..-..
    
    # 00-01-00-..          y, x, h, w  
    title_panels["title_scr_panel"].textbox          = CurseTextbox(**dict(
    parent      = title_panels["title_scr_panel"],
    base_text    = asciiart.titlestr5,
    size        = (3, 9, 10, 63), 
    style       = curse_styles["title_panel"]))
    # 00-02-00-..
    title_panels["title_scr_infopanel"].textbox      = CurseTextbox(**dict(
            parent      = title_panels["title_scr_infopanel"],
            base_text    = "  Use keys.up and keys.down to navigate , "\
                          "space to select action, q to quit ",
            size        =  (0, 0, 1, 78),
            style       = curse_styles["infobox2"]))

#"test_screen"------------------------------------------------------01-..-..-..
        
    # 01-01-00-..          y, x, h, w 
    test_panels["test_scr_upper_infopanel"].textbox  = CurseTextbox(**dict(
            parent      = test_panels["test_scr_upper_infopanel"],
            base_text    = "",
            size        = (1, 4, 3, 72),  
            style       = curse_styles["infobox1"]))
    # 01-04-00-..
    test_panels["test_scr_lower_infopanel"].textbox  = CurseTextbox(**dict(
            parent      = test_panels["test_scr_lower_infopanel"],
            base_text    = 
"(SHIFT+TAB)-(   TAB    ) -> [prev / next panel] || (\'z\') -> [prev screen] "\
"(KEYS.LEFT)-(KEYS.RIGHT) -> [prev / next page ] || (\'q\') -> [   quit    ] "\
"(KEYS.UP  )-(KEYS.DOWN ) -> [prev / next item ] "    ,
            size        = (0, 1, 3, 78), 
            style       = curse_styles["infobox2"]))

#"account_screen"---------------------------------------------------02-..-..-..
                             
    # 02-01-00-..          y, x, h, w 
    account_panels["acct_scr_NW_text_art"].textbox   = CurseTextbox(**dict(
            parent      = account_panels["acct_scr_NW_text_art"],
            base_text    = asciiart.artstr3,
            size        = (0, 0, 12, 30),   
            style       = curse_styles["dashscrbg"]))
    # 02-02-00-..
    account_panels["acct_scr_SW_text_art"].textbox   = CurseTextbox(**dict(
            parent      = account_panels["acct_scr_SW_text_art"],
            base_text    = asciiart.artstr3,
            size        = (0, 0, 12, 30),   
            style       = curse_styles["dashscrbg"]))
    # 02-03-00-..
    account_panels["acct_scr_NE_text_art"].textbox   = CurseTextbox(**dict(
            parent      = account_panels["acct_scr_NE_text_art"],
            base_text    = asciiart.artstr3,
            size        = (0, 0, 12, 30),   
            style       = curse_styles["dashscrbg"]))
    # 02-04-00-..
    account_panels["acct_scr_SE_text_art"].textbox   = CurseTextbox(**dict(
            parent      = account_panels["acct_scr_SE_text_art"],
            base_text    = asciiart.artstr3,
            size        = (0, 0, 12, 30),   
            style       = curse_styles["dashscrbg"]))
    # 02-05-00-..
    account_panels["acct_scr_infobox"].textbox       = CurseTextbox(**dict(
            parent      = account_panels["acct_scr_infobox"],
            base_text    = "select line and press ENTER to input name/password",           
            size        = (1, 1, 5, 20),   
            style       = curse_styles["infobox2"],
            center      = True))

#"about_screen"-----------------------------------------------------03-..-..-..
    #                      y, x, h, w               
    # 03-01-00-..
    about_panels["about_scr_bg_text_art"].textbox    = CurseTextbox(**dict(
            parent      = about_panels["about_scr_bg_text_art"],
            base_text   = asciiart.titlestr3b,
            size        = (0, 0, 21, 62),   
            style       = curse_styles["dashscrbg"]))
    # 03-02-00-..
    about_panels["about_scr_team_txt_panel"].textbox = CurseTextbox(**dict(
            parent      = about_panels["about_scr_team_txt_panel"],
            base_text   =         
                " The CursesDB Team:"\
                " *--*-------*--* "\
                " -- Ali Payne -- "\
                " ---*-------*--- "\
                "   Josh McQueen  "\
                " ---*-------*--- "\
                "   Tyler Hadley  "\
                " *--*-------*--* ",
            size        = (6, 1, 12, 17),   
            style       = curse_styles["middlepanes2"],
            center      = True))

#"login_screen"-----------------------------------------------------04-..-..-..
    pass

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def load_targets(curse_container):
    """ assign item/panel infotars to object references named in infotar_str"""
    for screen_key in curse_container["screens"]:
        screen = curse_container["screens"][screen_key]
        for panel_key in screen.panels:
            panel = screen.panels[panel_key]
            if panel.infotar_str != None:
                panel.infotar = screen.getPanel(panel.infotar_str)
            for item_key in panel.items:
                item = panel.items[item_key]
                if item.infotar_str != None:
                    item.infotar = screen.panels[item.infotar_str]

# key-action map:   ordinal converted keyboard input to action string
# action map    :   action string to message
#           key:    action string
#           value:  a "message" as defined below
#
# readMessage() :   message to command execution / function call
#
# message = {   
#       msg_status  = "unread", 
#       send_layer  = "screen", 
#       recv_layer  = "main", 
#       recv_name   = "main",   
#       on_recv     = "call_function", 
#       recv_act    = "changeScreen", 
#       recv_args   = ["_previous"])}
#

def init_act_msg_maps():
    act_msg_maps = {
        "screen": {
            "back"      : dict(  msg_status  = "unread", 
                send_layer  = "screen", 
                recv_layer  = "self", 
                recv_name   = "self",   
                on_recv     = "call_function", 
                recv_act    = "prevPanel",
                recv_args   = None,
                ret_info    = None),
            "forward"      : dict(  msg_status  = "unread", 
                send_layer  = "screen", 
                recv_layer  = "self", 
                recv_name   = "self",   
                on_recv     = "call_function",  
                recv_act    = "nextPanel",
                recv_args   = None,
                ret_info    = None),
            "quit"      : dict(  msg_status  = "unread", 
                send_layer  = "screen", 
                recv_layer  = "main", 
                recv_name   = "main",   
                on_recv     = "call_function", 
                recv_act    = "quitCurses",
                recv_args   = None,
                ret_info    = None),
            "prev_scr"  : dict(  msg_status  = "unread", 
                send_layer  = "screen", 
                recv_layer  = "main", 
                recv_name   = "main",   
                on_recv     = "call_function", 
                recv_act    = "changeScreen", 
                recv_args   = ["_previous"],
                ret_info    = None)},
        "panel_msg_map" : {
            "left"      : dict(  msg_status  = "unread", 
                send_layer  = "panel", 
                recv_layer  = "self", 
                recv_name   = "self",   
                on_recv     = "call_function", 
                recv_act    = "turnPage",
                recv_args   = ["prev", "infotar"],
                ret_info    = None),
            "right"      : dict(  msg_status  = "unread", 
                send_layer  = "panel", 
                recv_layer  = "self", 
                recv_name   = "self",   
                on_recv     = "call_function",  
                recv_act    = "turnPage",
                recv_args   = ["next", "infotar"],
                ret_info    = None),
            "up"      : dict(  msg_status  = "unread", 
                send_layer  = "panel", 
                recv_layer  = "self", 
                recv_name   = "self",   
                on_recv     = "call_function",  
                recv_act    = "prevItem",
                recv_args   = None,
                ret_info    = None),
            "down"      : dict(  msg_status  = "unread", 
                send_layer  = "panel", 
                recv_layer  = "self", 
                recv_name   = "self",   
                on_recv     = "call_function",  
                recv_act    = "nextItem",
                recv_args   = None,
                ret_info    = None),
            "select"      : dict(  msg_status  = "unread", 
                send_layer  = "panel", 
                recv_layer  = "self", 
                recv_name   = "self",   
                on_recv     = "call_function",  
                recv_act    = "select",
                recv_args   = None,
                ret_info    = None)}}

    return act_msg_maps
