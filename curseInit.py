import copy
import curses

from curseScreen import CurseScreen
from cursePanel import CursePanel
from curseTextbox import CurseTextbox
from curseItem import CurseItem

from types import MethodType

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

#   SEARCH INDEX: USE UNIQUE XX-XX-XX-XX CODE WITH CTRL-F TO FIND WHERE
#                       COMPONENT IS CREATED
#                                                                       FUNCS 
#                                                                  ITEM   |
#                                                            TEXTBOX  |   |
#                                                           PANEL  |  |   |
#                                                       SCREEN  |  |  |	  |
# CurseScreen   | CursePanel               Curse     Curse   |  |  |  |   |
#               |                         Textbox    Item    SC PA TB IT  V
#---------------|---------------------------|-|--------------!!-!!-!!-!!
#title_screen---|---------------------------|-|--------------00-..-..-..
#---------------|title_scr_user_strip-------|-|--------------00-00-..-..
#---------------|title_scr_panel------------|-|--------------00-01-..-..
#---------------|---------------------------|X|--------------00-01-00-..
#---------------|---------------------------|-|login_link----00-01-..-00
#---------------|---------------------------|-|act_create_lk-00-01-..-01
#---------------|---------------------------|-|about_DB_link-00-01-..-02
#---------------|title_scr_infopanel--------|-|--------------00-02-..-..
#---------------|---------------------------|X|--------------00-02-00-..
#---------------|title_scr_background-------|-|--------------00-03-..-..
#test_screen----|---------------------------|-|--------------01-..-..-..
#---------------|test_scr_user_strip--------|-|--------------01-00-..-..
#---------------|test_scr_upper_infopanel---|-|--------------01-01-..-..
#---------------|---------------------------|X|--------------01-01-00-..
#---------------|test_scr_left_mid_panel----|-|--------------01-02-..-..
#---------------|test_scr_r_mid_panel-------|-|--------------01-03-..-..
#---------------|---------------------------|-|list_hdr------01-03-..-00
#---------------|---------------------------|-|item1---------01-03-..-01
#---------------|---------------------------|-|item2---------01-03-..-02
#---------------|---------------------------|-|item3---------01-03-..-03
#---------------|test_scr_lower_infopanel---|-|--------------01-04-..-..
#---------------|---------------------------|X|--------------01-04-00-..
#---------------|test_scr_input_strip-------|-|--------------01-05-..-..
#account_screen-|---------------------------|-|--------------02-..-..-..
#---------------|acct_scr_user_strip--------|-|--------------02-00-..-..
#---------------|acct_scr_NW_text_art-------|-|--------------02-01-..-..
#---------------|---------------------------|X|--------------02-01-00-..
#---------------|acct_scr_SW_text_art-------|-|--------------02-02-..-..
#---------------|---------------------------|X|--------------02-02-00-..
#---------------|acct_scr_NE_text_art-------|-|--------------02-03-..-..
#---------------|---------------------------|X|--------------02-03-00-..
#---------------|acct_scr_SE_text_art-------|-|--------------02-04-..-..
#---------------|---------------------------|X|--------------02-04-00-..
#---------------|acct_scr_mid_back_panel----|-|--------------02-08-..-..
#---------------|acct_scr_mid_panel---------|-|--------------02-05-..-..
#---------------|---------------------------|-|username------02-05-..-00 IFUNC_001
#---------------|---------------------------|-|password------02-05-..-01 IFUNC_002
#---------------|---------------------------|-|submit_acct---02-05-..-02 IFUNC_003
#---------------|acct_scr_infobox-----------|-|--------------02-06-..-..
#---------------|---------------------------|X|--------------02-06-00-..
#---------------|acct_scr_name_strip--------|-|--------------02-07-..-..
#---------------|acct_scr_pw_strip----------|-|--------------02-08-..-..
#about_screen---|---------------------------|-|--------------03-..-..-..
#---------------|about_scr_user_strip-------|-|--------------03-00-..-..
#---------------|about_scr_bg_text_art------|-|--------------03-01-..-..
#---------------|---------------------------|X|--------------03-01-00-..
#---------------|about_scr_team_txt_panel---|-|--------------03-02-..-..
#---------------|---------------------------|X|--------------03-02-00-..
#---------------|about_scr_info_strip-------|-|--------------03-03-..-..
#login_screen---|---------------------------|-|--------------04-..-..-..
#---------------|login_scr_bg---------------|-|--------------04-00-..-..
#---------------|login_scr_user_strip-------|-|--------------04-01-..-..
#---------------|login_scr_menu_pnl---------|-|--------------04-02-..-..
#---------------|---------------------------|-|logname-------04-02-..-00 IFUNC_004
#---------------|---------------------------|-|logpw---------04-02-..-01 IFUNC_005
#---------------|---------------------------|-|logsubmit-----04-02-..-02 IFUNC_006
#---------------|login_scr_infobox----------|-|--------------04-03-..-..
#---------------|---------------------------|X|--------------04-03-00-..
#---------------|login_scr_mid_bg_panel-----|-|--------------04-05-..-..
#---------------|login_scr_name_strip-------|-|--------------04-06-..-..
#---------------|login_scr_pw_strip---------|-|--------------04-07-..-..
#usermain_screen|---------------------------|-|--------------05-..-..-..
#---------------|usermain_scr_bg------------|-|--------------05-00-..-..
#---------------|usermain_scr_ustrip--------|-|--------------05-01-..-..
#---------------|usermain_scr_menu_pnl------|-|--------------05-02-..-..


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
        global_storage  = {}) 
    return curse_container 

def init_screens(curse_container):
    global layers
    key_action_map      = curse_container["key_action_map"]
    curseStyles         = curse_container["styles"]
    curseScreens        = curse_container["screens"]

    default_msg_map     = curse_container["act_msg_maps"]["screen"]
    global_storage      = curse_container["global_storage"]

    # 00-..-..-..                     
    curseScreens["title_screen"]    = CurseScreen(**{
    "global_storage"    : global_storage,
    "user_strip"        : "title_scr_user_strip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "title_scr_panel",
    "can_panel_change"  : True,
    "style"             : curseStyles["dashscrbg"]})
    # 01-..-..-..
    curseScreens["test_screen"]     = CurseScreen(**{
    "global_storage"    : global_storage,
    "user_strip"        : "test_scr_user_strip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "test_scr_left_mid_panel",
    "can_panel_change"  : True,
    "style"             : curseStyles["dashscrbg"]})
    # 02-..-..-..
    curseScreens["account_screen"]  = CurseScreen(**{
    "global_storage"    : global_storage,
    "user_strip"        : "acct_scr_user_strip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "acct_scr_mid_panel",
    "can_panel_change"  : False,
    "style"             : curseStyles["dashscrbg"]})  
    # 03-..-..-..
    curseScreens["about_screen"]    = CurseScreen(**{
    "global_storage"    : global_storage,
    "user_strip"        : "about_scr_user_strip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : None,
    "can_panel_change"  : False,
    "style"             : curseStyles["dashscrbg"]})
    # 04-..-..-..
    curseScreens["login_screen"]    = CurseScreen(**{
    "global_storage"    : global_storage,
    "user_strip"        : "login_scr_user_strip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "login_scr_menu_pnl",
    "can_panel_change"  : False,
    "style"             : curseStyles["dashscrbg"]})
    # 05-..-..-..
    #curseScreens["usermain_screen"]    = CurseScreen(**{
    #"global_storage"    : global_storage,
    #"user_strip"        : "usermain_scr_ustrip",
    #"key_action_map"    : key_action_map,
    #"act_msg_map"       : default_msg_map,
    #"default_focus_key" : "usermain_scr_menu_pnl",
    #"can_panel_change"  : False,
    #"style"             : curseStyles["dashscrbg"]})

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
    login_screen    = curseScreens["login_screen"]  

    panel_msg_map = curse_container["act_msg_maps"]["panel_msg_map"]
    global_storage = curse_container["global_storage"]
                                                                               
    # 00-03-..-..      y, x, h, w
    title_screen.panels["title_scr_background"]            = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : title_screen,
    "size"          : (0, 0, 24, 80),   
    "style"         : curseStyles["title_panel"]})
    # 00-00-..-..
    title_screen.panels["title_scr_user_strip"]            = CursePanel(**{
    "global_storage"       : global_storage,
    "parent"        : title_screen,
    "size"          : (0, 0, 1, 80), 
    "style"         : curseStyles["user_strip"]})
    # 00-01-..-..
    title_screen.panels["title_scr_panel"]                 = CursePanel(**{
    "global_storage"       : global_storage,
    "act_msg_map"   : panel_msg_map,
    "parent"        : title_screen,
    "size"          : (1, 0, 20, 80),       
    "style"         : curseStyles["title_panel"],
    "focusable"     : True})
    # 00-02-..-..
    title_screen.panels["title_scr_infopanel"]             = CursePanel(**{
    "global_storage"       : global_storage,
    "parent"        : title_screen,
    "size"          : (21, 0, 1, 80),   
    "style"         : curseStyles["infobox2"]})
    # panels are updated/ drawn in the order below- this affects
    # overlapping panels so pay attention to this!      
    title_screen.panel_indexes = [
        "title_scr_background",
        "title_scr_user_strip", 
        "title_scr_panel",
        "title_scr_infopanel"]
    title_screen.panel_count = len(title_screen.panel_indexes)

    # 01-00-..-..      y, x, h, w
    test_screen.panels["test_scr_user_strip"]              = CursePanel(**{
    "global_storage" : global_storage,
    "parent"        : test_screen,
    "size"          : (0, 0, 1, 80),  
    "style"         : curseStyles["user_strip"]})
    # 01-01-..-.. 
    test_screen.panels["test_scr_upper_infopanel"]         = CursePanel(**{
    "global_storage"       : global_storage,
    "parent"        : test_screen,    
    "size"          : (1, 0, 5, 80),
    "style"         : curseStyles["infobox1"],    
    "title"         : ("(INFOBOX 1)", 0, 1)})
    # 01-02-..-..
    test_screen.panels["test_scr_left_mid_panel"]          = CursePanel(**{
    "global_storage"       : global_storage,
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
    "global_storage" : global_storage,
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
    "global_storage" : global_storage,
    "parent"        : test_screen,
    "size"          : (18, 0, 4, 80),
    "style"         : curseStyles["infobox2"]})
    # 01-05-..-..
    test_screen.panels["test_scr_input_strip"]             = CursePanel(**{
    "global_storage" : global_storage,
    "parent"        : test_screen,
    "size"          : (22, 0, 1, 80),
    "style"         : curseStyles["input_strip"],    
    "title"         : ( "(TYPED USER INPUT CAN GO HERE?)", 0, 0)})
    # panels are updated/ drawn in the order below- this affects
    # overlapping panels so pay attention to this!
    test_screen.panel_indexes = [
        "test_scr_user_strip", 
        "test_scr_upper_infopanel",
        "test_scr_left_mid_panel",
        "test_scr_r_mid_panel",
        "test_scr_lower_infopanel",
        "test_scr_input_strip"]
    test_screen.panel_count = len(test_screen.panel_indexes)
                           
    # 02-00-..-..
    account_screen.panels["acct_scr_user_strip"]           = CursePanel(**{
    "global_storage"       : global_storage,
    "parent"        : account_screen,
    "size"          : (0, 0, 1, 80),  
    "style"         : curseStyles["user_strip"]})
    # 02-01-..-..
    account_screen.panels["acct_scr_NW_text_art"]          = CursePanel(**{
    "global_storage"       : global_storage,
    "parent"        : account_screen,
    "size"          : (1, 0, 13, 30),  # w.31->w.29
    "style"         : curseStyles["dashscrbg"]})
    # 02-02-..-..
    account_screen.panels["acct_scr_SW_text_art"]          = CursePanel(**{
    "global_storage"       : global_storage,
    "parent"        : account_screen,
    "size"          : (12, 0, 13, 30), # w.31->w.29
    "style"         : curseStyles["dashscrbg"]})
    # 02-03-..-..
    account_screen.panels["acct_scr_NE_text_art"]          = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : account_screen,
    "size"          : (1, 51, 13, 30),
    "style"         : curseStyles["dashscrbg"]})
    # 02-04-..-..
    account_screen.panels["acct_scr_SE_text_art"]          = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : account_screen,
    "size"          : (12, 51, 13, 30), 
    "style"         : curseStyles["dashscrbg"]})
    # 02-08-..-..
    account_screen.panels["acct_scr_mid_back_panel"]       = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : account_screen,
    "size"          : (10, 29, 6, 22),
    "style"         : curseStyles["middlepanes"]})
    # 02-05-..-..
    account_screen.panels["acct_scr_mid_panel"]            = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : account_screen,
    "act_msg_map"   : panel_msg_map,
    "size"          : (1, 29, 9, 22),
    "title"         : ( "ACCOUNT CREATION".center(16), 2, 3), 
    "style"         : curseStyles["middlepanes"],   
    "focusable"     : True})
    # 02-06-..-..
    account_screen.panels["acct_scr_infobox"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : account_screen,
    "size"          : (17, 29, 6, 22),
    "style"         : curseStyles["infobox2"]})
    # 02-07-..-..
    account_screen.panels["acct_scr_name_strip"]           = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : account_screen,
    "title"         : ( "ACCOUNT NAME".center(18), 0, 0), 
    "size"          : (11, 31, 2, 18),
    "style"         : curseStyles["input_strip3"]})
    # 02-08-..-..
    account_screen.panels["acct_scr_pw_strip"]             = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : account_screen,
    "title"         : ( "ACCOUNT PASSWORD".center(18), 0, 0), 
    "size"          : (13, 31, 2, 18),
    "style"         : curseStyles["input_strip3"]})
    # 02-09-..-..
    account_screen.panels["acct_scr_back_panel"]             = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : account_screen,
    "size"          : (1, 26, 24, 26),
    "style"         : curseStyles["colonscrbg2"]})
    # panels are updated/ drawn in the order below- this affects
    # overlapping panels so pay attention to this! 
    account_screen.panel_indexes = [
        "acct_scr_NW_text_art",
        "acct_scr_SW_text_art",
        "acct_scr_NE_text_art",
        "acct_scr_SE_text_art",
        "acct_scr_back_panel",
        "acct_scr_mid_back_panel",
        "acct_scr_mid_panel",
        "acct_scr_infobox",
        "acct_scr_name_strip",
        "acct_scr_pw_strip",
        "acct_scr_user_strip"]
    account_screen.panel_count = len(account_screen.panel_indexes)
                                                                                                                                               
    # 03-00-..-..
    about_screen.panels["about_scr_user_strip"]            = CursePanel(**{
    "global_storage" : global_storage,
    "parent"        : about_screen,
    "size"          : (0, 0, 1, 80),
    "style"         : curseStyles["user_strip"]})
    # 03-01-..-..
    about_screen.panels["about_scr_bg_text_art"]           = CursePanel(**{
    "global_storage" : global_storage,
    "parent"        : about_screen,
    "size"          : (1, 0, 22, 61), # w: 62->61
    "style"         : curseStyles["dashscrbg"]})
    # 03-02-..-..
    about_screen.panels["about_scr_team_txt_panel"]        = CursePanel(**{
    "global_storage" : global_storage,
    "parent"        : about_screen,
    "size"          : (1, 61, 21, 19),
    "style"         : curseStyles["middlepanes2"]})
    # 03-03-..-..
    about_screen.panels["about_scr_info_strip"]            = CursePanel(**{
    "global_storage" : global_storage,
    "parent"        : about_screen,
    "size"          : (22, 0, 1, 80), # x. 23->22
    "style"         : curseStyles["infobox2"],
    "title"         : (
        "Press Z to return to Title Screen, if you dare...".center(79), 0, 0)})
    # panels are updated/ drawn in the order below- this affects
    # overlapping panels so pay attention to this! 
    about_screen.panel_indexes = [
        "about_scr_user_strip", 
        "about_scr_bg_text_art",
        "about_scr_team_txt_panel",
        "about_scr_info_strip"]
    about_screen.panel_count = len(about_screen.panel_indexes)

    # 04-00-..-..      y, x, h, w
    login_screen.panels["login_scr_bg"]                    = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "size"          : (0, 0, 24, 80),
    "style"         : curseStyles["at_scrbg"]}) 
    # 04-05-..-..
    login_screen.panels["login_scr_mid_bg_panel"]          = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "size"          : (9, 29, 6, 22),
    "style"         : curseStyles["middlepanes"]})
    # 04-01-..-.. 
    login_screen.panels["login_scr_user_strip"]            = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "size"          : (0, 0, 1, 80),
    "style"         : curseStyles["user_strip"]})     
    # 04-02-..-.. 
    login_screen.panels["login_scr_menu_pnl"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "act_msg_map"   : panel_msg_map,
    "size"          : (8, 7, 9, 22),
    "style"         : curseStyles["middlepanes"],   
    "focusable"     : True})
    # 04-03-..-..
    login_screen.panels["login_scr_infobox"]               = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : account_screen,
    "size"          : (8, 51, 9, 22),
    "style"         : curseStyles["infobox2"]})
    # 04-04-..-..
    login_screen.panels["login_scr_name_strip"]            = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "size"          : (11, 31, 1, 18),
    "style"         : curseStyles["input_strip2"]})
    # 04-06-..-..
    login_screen.panels["login_scr_pw_strip"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "size"          : (12, 31, 1, 18),
    "style"         : curseStyles["input_strip2"]})
    # 04-07
    login_screen.panels["login_scr_title_panel"]           = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "title"         : ("ACCOUNT LOGIN".center(16), 1, 3),
    "size"          : (4, 29, 3, 22),
    "style"         : curseStyles["middlepanes3"]})                            
    # panels are updated/ drawn in the order below- this affects
    # overlapping panels so pay attention to this!
    login_screen.panel_indexes = [
        "login_scr_bg",
        "login_scr_mid_bg_panel", 
        "login_scr_user_strip",
        "login_scr_menu_pnl",
        "login_scr_title_panel",
        "login_scr_infobox",
        "login_scr_name_strip",
        "login_scr_pw_strip"]
    login_screen.panel_count = len(login_screen.panel_indexes)


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def init_items(curse_container):
    """ make the curseItems for all cursePanels

    instantiate and set fields of panel child items. 
    all fields of an item are set here EXCEPT:
        item.infotar 
    """
    curseStyles         = curse_container["styles"]
    curseScreens        = curse_container["screens"]

    global_storage = curse_container["global_storage"]

    title_panels   = curseScreens["title_screen"].panels
    test_panels    = curseScreens["test_screen"].panels
    account_panels = curseScreens["account_screen"].panels
    about_scr_panels   = curseScreens["about_screen"].panels
    login_scr_panels   = curseScreens["login_screen"].panels
    
    # 00-01-..-00
    title_panels["title_scr_panel"].items["login_link"]     = CurseItem(**{
    "global_storage" : global_storage,
    "parent"        : title_panels["title_scr_panel"],
    "parent_screen"  : curseScreens["title_screen"],
    "size"          : (15, 30, 1, 20), # y, x, h, w
    "style"         : curseStyles["title_menu"],
    "label"         : "account log in".center(20),
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "main", 
        recv_name   = "main",   
        on_recv     = "call_function", 
        recv_act    = "changeScreen",
        recv_args   = ["login_screen"],
        ret_info    = None)})
    # 00-01-..-01
    title_panels["title_scr_panel"].items["act_create_lk"]  = CurseItem(**{
    "global_storage" : global_storage,
    "parent"        : title_panels["title_scr_panel"],
    "parent_screen"  : curseScreens["title_screen"],
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
    title_panels["title_scr_panel"].items["about_DB_link"]  = CurseItem(**{
    "global_storage" : global_storage,
    "parent"        : title_panels["title_scr_panel"],
    "parent_screen"  : curseScreens["title_screen"],
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

    # 01-03-..-00
    test_panels["test_scr_r_mid_panel"].items["list_hdr"]   = CurseItem(**{
    "global_storage" : global_storage,
    "parent"        : test_panels["test_scr_r_mid_panel"],
    "parent_screen"  : curseScreens["test_screen"],
    "size"          : (2, 3, 4, 10), # y, x, h, w
    "style"         : test_panels["test_scr_r_mid_panel"].style,
    "label"         : "header",
    "focusable"     : False })
    # 01-03-..-01
    test_panels["test_scr_r_mid_panel"].items["item1"]      = CurseItem(**{
    "global_storage" : global_storage,
    "parent"        : test_panels["test_scr_r_mid_panel"],
    "parent_screen"  : curseScreens["test_screen"],
    "size"          : (3, 3, 4, 10), # y, x, h, w
    "style"         : test_panels["test_scr_r_mid_panel"].style,
    "label"         : "item1"})
    # 01-03-..-02
    test_panels["test_scr_r_mid_panel"].items["item2"]      = CurseItem(**{
    "global_storage" : global_storage,
    "parent"        : test_panels["test_scr_r_mid_panel"],
    "parent_screen"  : curseScreens["test_screen"],
    "size"          : (4, 3, 4, 10), # y, x, h, w
    "style"         : test_panels["test_scr_r_mid_panel"].style,
    "label"         : "item2"})
    # 01-03-..-03
    test_panels["test_scr_r_mid_panel"].items["item3"]      = CurseItem(**{
    "global_storage" : global_storage,
    "parent"       : test_panels["test_scr_r_mid_panel"],
    "parent_screen"  : curseScreens["test_screen"],
    "size"          : (5, 3, 4, 10), # y, x, h, w
    "style"         : test_panels["test_scr_r_mid_panel"].style,
    "label"         : "item3"})
    test_panels["test_scr_r_mid_panel"].item_count = 4
    test_panels["test_scr_r_mid_panel"].item_indexes = [
        "list_hdr", 
        "item1", 
        "item2",
        "item3"]

    # 02-05-..-00       IFUNC_001
    account_panels["acct_scr_mid_panel"].items["username"]  = CurseItem(**{
    "global_storage" : global_storage,
    "parent"        : account_panels["acct_scr_mid_panel"],
    "parent_screen"  : curseScreens["account_screen"],
    "size"          : (4, 3, 4, 10), # y, x, h, w
    "style"         : account_panels["acct_scr_mid_panel"].style,
    "label"         : "USERNAME".center(16),
    "info"          : "name must be 4-18 alphanumeric char\n"\
                      "hit SPACE to begin "\
                      "hit RETURN to finish",
    "infotar"       : "acct_scr_infobox",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item",
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "createAcctName",
        recv_args   = [],
        ret_info    = None)})  
    # 02-05-..-01       IFUNC_002
    account_panels["acct_scr_mid_panel"].items["password"]  = CurseItem(**{
    "global_storage" : global_storage,
    "parent"        : account_panels["acct_scr_mid_panel"],
    "parent_screen" : curseScreens["account_screen"],
    "size"          : (5, 3, 4, 10), # y, x, h, w
    "style"         : account_panels["acct_scr_mid_panel"].style,
    "label"         : "PASSWORD".center(16),
    "info"          : "pw must be 4-18 alphanumeric char\n"\
                      "hit SPACE to begin "\
                      "hit RETURN to finish",
    "infotar"       : "acct_scr_infobox",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "createAcctPW",
        recv_args   = [],
        ret_info    = None)})
    # 02-05-..-02       IFUNC_003
    account_panels["acct_scr_mid_panel"].items["submit_acct"]=CurseItem(**{
    "global_storage" : global_storage,
    "parent"        : account_panels["acct_scr_mid_panel"],
    "parent_screen" : curseScreens["account_screen"],
    "size"          : (6, 3, 4, 10), # y, x, h, w
    "style"         : account_panels["acct_scr_mid_panel"].style,
    "label"         : "SUBMIT".center(16),
    "info"          : "press SPACE to submit account name and password",
    "infotar"       : "acct_scr_infobox",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "submitAccount",
        recv_args   = [],
        ret_info    = None)})
    account_panels["acct_scr_mid_panel"].item_count = 3
    account_panels["acct_scr_mid_panel"].item_indexes = [
        "username", 
        "password",
        "submit_acct"]

    # 03-..-..-..
    pass

    # 04-02-..-00       IFUNC_004
    login_scr_panels["login_scr_menu_pnl"].items["logname"] = CurseItem(**{
    "global_storage": global_storage,
    "parent"        : login_scr_panels["login_scr_menu_pnl"],
    "parent_screen" : curseScreens["login_screen"],
    "size"          : (3, 3, 4, 10), # y, x, h, w
    "style"         : login_scr_panels["login_scr_menu_pnl"].style,
    "label"         : "USERNAME".center(16),
    "info"          : "press SPACE to enter your account log-in name "\
                      "................. "\
                      "hit RETURN to finish entry",
    "infotar"       : "login_scr_infobox",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item",
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "loginName",
        recv_args   = [],
        ret_info    = None)})
    # 04-02-..-01       IFUNC_005
    login_scr_panels["login_scr_menu_pnl"].items["logpw"]   = CurseItem(**{
    "global_storage": global_storage,
    "parent"        : login_scr_panels["login_scr_menu_pnl"],
    "parent_screen" : curseScreens["login_screen"],
    "size"          : (4, 3, 4, 10), # y, x, h, w
    "style"         : login_scr_panels["login_scr_menu_pnl"].style,
    "label"         : "PASSWORD".center(16),
    "info"          : "press SPACE to enter your account log-in password "\
                      "................. "\
                      "hit RETURN to finish entry",
    "infotar"       : "login_scr_infobox",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item",
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "loginPW",
        recv_args   = [],
        ret_info    = None)})
    # 04-02-..-02       IFUNC_006
    login_scr_panels["login_scr_menu_pnl"].items["logsubmit"]=CurseItem(**{
    "global_storage": global_storage,
    "parent"        : login_scr_panels["login_scr_menu_pnl"],
    "parent_screen" : curseScreens["login_screen"],
    "size"          : (6, 3, 4, 10), # y, x, h, w
    "style"         : login_scr_panels["login_scr_menu_pnl"].style,
    "label"         : "SUBMIT".center(16),
    "info"          : "press SPACE to submit login credentials",
    "infotar"       : "login_scr_infobox",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item",
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "logSubmit",
        recv_args   = [],
        ret_info    = None)})
    login_scr_panels["login_scr_menu_pnl"].item_count = 3
    login_scr_panels["login_scr_menu_pnl"].item_indexes = [
        "logname", 
        "logpw",
        "logsubmit"]

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def init_textboxes(curse_container):
    title_panels   = curse_container["screens"]["title_screen"].panels
    test_panels    = curse_container["screens"]["test_screen"].panels
    account_panels = curse_container["screens"]["account_screen"].panels
    about_panels   = curse_container["screens"]["about_screen"].panels
    login_panels   = curse_container["screens"]["login_screen"].panels
    curse_styles   = curse_container["styles"]
    
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
            base_text    = "select field and press SPACE to begin "\
                           "account name/password entry",           
            size        = (1, 1, 5, 20),   
            style       = curse_styles["infobox2"],
            center      = True))
                          
    # 03-01-00-..          y, x, h, w   
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

    # 04-03-00-..          y, x, h, w   
    login_panels["login_scr_infobox"].textbox        = CurseTextbox(**dict(
            parent      = login_panels["login_scr_infobox"],
            base_text   = "select field and press SPACE to begin "\
                           "entry",              
            size        = (2, 2, 6, 18),   
            style       = curse_styles["infobox2"],
            center      = True))
    pass

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def load_targets(curse_container):
    """ assign item/panel infotars to object references named in infotar_str"""
    for screen_key in curse_container["screens"]:
        screen = curse_container["screens"][screen_key]
        screen.user_strip = screen.panels[screen.user_strip_str]
        for panel_key in screen.panels:
            panel = screen.panels[panel_key]
            if panel.infotar_str != None:
                panel.infotar = screen.getPanelByName(panel.infotar_str)
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

def init_funcs(curse_container):
    curseStyles         = curse_container["styles"]
    curseScreens        = curse_container["screens"]

    title_panels   = curseScreens["title_screen"].panels
    test_panels    = curseScreens["test_screen"].panels
    account_panels = curseScreens["account_screen"].panels
    about_scr_panels   = curseScreens["about_screen"].panels
    login_screen       = curseScreens["login_screen"]
    login_scr_panels   = login_screen.panels

    # 01-..-..-..       SFUNC_001
    #def showUserInfo(self, target_panel):
    #    if "username" in self.global_storage:
    #        name = copy.copy(self.global_storage["username"])
    #        target_panel.win.addstr(0, 1, "USERNAME: "+ name, 
    #            target_panel.style.txt_atr | target_panel.style.txt_clr)
    #tscreen = curseScreens["title_screen"]
    #tscreenshowUserInfo = MethodType(showUserInfo,tscreen)

    # 00-..-..-..
    pass

    # 01-..-..-..
    pass

    # 02-05-..-00       IFUNC_001
    min = 4
    max = 18
    def createAcctName(self):
        """ get user password and store it for validation """
        result = self.getUserString("1100", curses.color_pair(10), 
                       account_panels["acct_scr_name_strip"],      
                       (1,0), min, max, True, False, False)
        if result[0] == "OK_DONE":
            self.parent_panel.panel_storage[
                "account_name"] = copy.copy(result[1])
        else:
            self.showErrorMsg(result[0], [min], True, 
                account_panels["acct_scr_infobox"].textbox)
            if "account_name" in self.parent_panel.panel_storage:
                del self.parent_panel.panel_storage["account_name"]
    act_item1          = account_panels["acct_scr_mid_panel"].items["username"]
    act_item1.createAcctName = MethodType(createAcctName, act_item1, CurseItem)
    # 02-05-..-01       IFUNC_002
    def createAcctPW(self):
        """ get user password and store it for validation """
        result = self.getUserString("1100", curses.color_pair(10), 
                       account_panels["acct_scr_pw_strip"],      
                       (1,0), min, max, True, True, False)
        if result[0] == "OK_DONE":
            self.parent_panel.panel_storage["account_pw"] = copy.copy(result[1])
        else:
            self.showErrorMsg(result[0], [min], True,
                account_panels["acct_scr_infobox"].textbox)
            if "account_pw" in self.parent_panel.panel_storage:
                del self.parent_panel.panel_storage["account_pw"]
    act_item2          = account_panels["acct_scr_mid_panel"].items["password"]
    act_item2.createAcctPW     = MethodType(createAcctPW, act_item2, CurseItem)
    # 02-05-..-02       IFUNC_003
    def submitAccount(self):pass
    act_item3       = account_panels["acct_scr_mid_panel"].items["submit_acct"]
    act_item3.submitAccount   = MethodType(submitAccount, act_item3, CurseItem)

    # 03-..-..-..
    pass

    # 04-02-..-00       IFUNC_004
    def loginName(self):
        """ get user login name and store it for validation """
        result = self.getUserString("1100", curses.color_pair(10), 
                       login_scr_panels["login_scr_name_strip"],       
                       (0,0), min, max, True, False, False)
        if result[0] == "OK_DONE":
            self.global_storage["log_name"] = copy.copy(result[1])
            login_screen.setUserStripInfo()
            login_screen.drawUserStripInfo()
        else:
            self.showErrorMsg(result[0], [min], True, 
                login_scr_panels["login_scr_infobox"].textbox)
            if "log_name" in self.global_storage:
                del self.global_storage["log_name"]
    log_item1       = login_scr_panels["login_scr_menu_pnl"].items["logname"]
    log_item1.loginName       = MethodType(loginName, log_item1, CurseItem)  
    # 04-02-..-01       IFUNC_005
    def loginPW(self):
        """ get user login pw and store it for validation """
        result = self.getUserString("1100", curses.color_pair(10), 
                       login_scr_panels["login_scr_pw_strip"],       
                       (0,0), min, max, True, True, False)
        if result[0] == "OK_DONE":
            self.global_storage["log_pw"] = copy.copy(result[1])
            login_screen.setUserStripInfo()
            login_screen.drawUserStripInfo()
        else:
            self.showErrorMsg(result[0], [min], True, 
                login_scr_panels["login_scr_infobox"].textbox)
            if "log_pw" in self.global_storage:
                del self.global_storage["log_pw"]
    log_item2       = login_scr_panels["login_scr_menu_pnl"].items["logpw"]
    log_item2.loginPW       = MethodType(loginPW, log_item2, CurseItem)
    # 04-02-..-02       IFUNC_006
    def logSubmit(self):pass
    log_item3     = login_scr_panels["login_scr_menu_pnl"].items["logsubmit"]
    log_item3.logSubmit       = MethodType(logSubmit, log_item3, CurseItem)

def load_globals(curse_container):
    curse_container["global_storage"]["log_name"] = "NONE"
    curse_container["global_storage"]["log_pw"] = "NONE"
       
    
     