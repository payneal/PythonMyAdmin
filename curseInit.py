#!/usr/bin/env python3
import copy
import curses

from curseScreen import CurseScreen
from cursePanel import CursePanel
from curseTextbox import CurseTextbox
from curseItem import CurseItem

from types import MethodType

import asciiart
import curseItem

import psycopg2 
import json
import decimal
import cursesPostgresTemp
import curseMysqlTemp

#layers = { "main": 0, "screen": 1, "panel": 2, "item":3 }

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

def appendix():
    pass
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
#---------------|test_scr_l_mid_panel-------|-|--------------01-02-..-..
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
#---------------|acct_scr_back_panel--------|-|--------------02-10-..-..
#---------------|acct_scr_mid_back_panel----|-|--------------02-07-..-..
#---------------|acct_scr_mid_panel---------|-|--------------02-05-..-..
#---------------|---------------------------|-|username------02-05-..-00 001
#---------------|---------------------------|-|password------02-05-..-01 001
#---------------|---------------------------|-|submit_acct---02-05-..-02 
#---------------|acct_scr_infobox-----------|-|--------------02-06-..-..
#---------------|---------------------------|X|--------------02-06-00-..
#---------------|acct_scr_name_strip--------|-|--------------02-08-..-..
#---------------|acct_scr_pw_strip----------|-|--------------02-09-..-..
#about_screen---|---------------------------|-|--------------03-..-..-..
#---------------|about_scr_user_strip-------|-|--------------03-00-..-..
#---------------|about_scr_bg_text_art------|-|--------------03-01-..-..
#---------------|---------------------------|X|--------------03-01-00-..
#---------------|about_scr_team_txt_panel---|-|--------------03-02-..-..
#---------------|---------------------------|X|--------------03-02-00-..
#---------------|about_scr_info_strip-------|-|--------------03-03-..-..
#login_screen---|---------------------------|-|--------------04-..-..-..
#---------------|login_scr_bg---------------|-|--------------04-00-..-..
#---------------|login_scr_mid_bg_panel-----|-|--------------04-01-..-..
#---------------|login_scr_user_strip-------|-|--------------04-02-..-..
#---------------|login_scr_menu_pnl---------|-|--------------04-03-..-..
#---------------|---------------------------|-|logname-------04-03-..-00 001
#---------------|---------------------------|-|logpw---------04-03-..-01 001
#---------------|---------------------------|-|logdb---------04-03-..-02 001
#---------------|---------------------------|-|loglang-------04-03-..-03 002
#---------------|---------------------------|-|logsubmit-----04-03-..-04 003
#---------------|login_scr_infobox----------|-|--------------04-04-..-..
#---------------|---------------------------|X|--------------04-04-00-..
#---------------|login_scr_name_strip-------|-|--------------04-05-..-..
#---------------|login_scr_pw_strip---------|-|--------------04-06-..-..
#---------------|login_scr_db_strip---------|-|--------------04-07-..-..
#---------------|login_scr_lang_optbox------|-|--------------04-08-..-..
#---------------|---------------------------|-|OmySQL--------04-08-..-00 
#---------------|---------------------------|-|Opostgre------04-08-..-01 
#---------------|login_scr_title_panel------|-|--------------04-09-..-..
#---------------|login_scr_footer-----------|-|--------------04-10-..-..
#usermain_screen|---------------------------|-|--------------05-..-..-..
#---------------|usermain_scr_bg------------|-|--------------05-00-..-..
#---------------|usermain_scr_ustrip--------|-|--------------05-01-..-..
#---------------|usermain_scr_u_info--------|-|--------------05-02-..-..
#---------------|---------------------------|X|--------------05-02-00-..
#---------------|user_scr_menu_pnl------|-|--------------05-03-..-..
#---------------|---------------------------|-|hdr-----------05-03-..-00
#---------------|---------------------------|-|viewDB--------05-03-..-01
#---------------|---------------------------|-|mngDBS--------05-03-..-02
#---------------|---------------------------|-|cfgAcct-------05-03-..-03
#---------------|---------------------------|-|logout--------05-03-..-04
#---------------|usermain_scr_m_pnl---------|-|--------------05-04-..-..
#---------------|---------------------------|-|hdr-----------05-04-..-00T
#---------------|---------------------------|-|viewDB--------05-04-..-01T
#---------------|---------------------------|-|mngDBS--------05-04-..-02T
#---------------|usermain_scr_l_info--------|-|--------------05-05-..-..
#---------------|---------------------------|X|--------------05-05-00-..
#viewDB_screen--|---------------------------|-|--------------06-..-..-..
#---------------|viewDB_scr_bg--------------|-|--------------06-00-..-..
#---------------|viewDB_scr_ustrip----------|-|--------------06-01-..-..
#---------------|viewDB_scr_menu_pnl--------|-|--------------06-02-..-..
#manageDB_screen|---------------------------|-|--------------07-..-..-..
#---------------|mngDBS_scr_bg--------------|-|--------------07-00-..-..
#---------------|mngDBS_scr_ustrip----------|-|--------------07-01-..-..
#---------------|mngDBS_scr_menu_pnl--------|-|--------------07-02-..-..
#cfg_acct_screen|---------------------------|-|--------------08-..-..-..
#---------------|cfgAcct_scr_bg-------------|-|--------------08-00-..-..
#---------------|cfgAcct_scr_ustrip---------|-|--------------08-01-..-..
#---------------|cfgAcct_scr_menu_pnl-------|-|--------------08-02-..-..
    pass

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

class CurseContainer(object):
    def __init__(self, *args):
        self.key_action_map = args[0]
        self.styles         = args[1]
        self.act_msg_maps   = init_act_msg_maps()
        self.screens        = {}
        self.global_storage = {}

    def getScreenByName(self, screen_key):
        if screen_key in self.screens:
            return self.screens[screen_key]
        return None

    def getPanelByName(self, panel_key):
        for screen_key in self.screens:
            screen = self.screens[screen_key]
            if panel_key in screen.panels:
                return screen.panels[panel_key]
        return None

    def getItemByName(self, item_key):
        for screen_key in self.screens:
            screen = self.screens[screen_key]
            for panel_key in screen.panels:
                panel = screen.panels[panel_key]
                if item_key in panel.items:
                    return panel.items[item_key]
        return None

    def getTextboxByName(self, textbox_parent_key):
        for screen_key in self.screens:
            screen = self.screens[screen_key]
            if textbox_parent_key in screen.panels:
                panel = screen.panels[textbox_parent_key]
                if panel.textbox != None:
                    return panel.textbox               
        return None

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def init_screens(curse_container):
    key_action_map      = curse_container.key_action_map 
    curseStyles         = curse_container.styles        
    curseScreens        = curse_container.screens       

    default_msg_map     = curse_container.act_msg_maps["screen"]  
    usermain_msg_map    = curse_container.act_msg_maps["user_screen"] 
    login_msg_map       = curse_container.act_msg_maps["login_screen"] 
    global_storage      = curse_container.global_storage 

    # 00-..-..-..                     
    curseScreens["title_screen"]    = CurseScreen(**{
    "global_storage"    : global_storage,
    "screens"           : curseScreens,
    "user_strip"        : "title_scr_user_strip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "title_scr_panel",
    "can_panel_change"  : True,
    "style"             : curseStyles["dashscrbg"],
    "ftr_strip"         : None})
    # 01-..-..-..
    curseScreens["test_screen"]     = CurseScreen(**{
    "global_storage"    : global_storage,
    "screens"           : curseScreens,
    "user_strip"        : "test_scr_user_strip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "test_scr_left_mid_panel",
    "can_panel_change"  : True,
    "style"             : curseStyles["dashscrbg"],
    "ftr_strip"         : None})
    # 02-..-..-..
    curseScreens["account_screen"]  = CurseScreen(**{
    "global_storage"    : global_storage,
    "screens"           : curseScreens,
    "user_strip"        : "acct_scr_user_strip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "acct_scr_mid_panel",
    "can_panel_change"  : False,
    "style"             : curseStyles["dashscrbg"],
    "ftr_strip"         : None})
    # 03-..-..-..
    curseScreens["about_screen"]    = CurseScreen(**{
    "global_storage"    : global_storage,
    "screens"           : curseScreens,
    "user_strip"        : "about_scr_user_strip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : None,
    "can_panel_change"  : False,
    "style"             : curseStyles["dashscrbg"],
    "ftr_strip"         : None})
    # 04-..-..-..
    curseScreens["login_screen"]    = CurseScreen(**{
    "global_storage"    : global_storage,
    "screens"           : curseScreens,
    "user_strip"        : "login_scr_user_strip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "login_scr_menu_pnl",
    "can_panel_change"  : False,
    "style"             : curseStyles["dashscrbg"],
    "ftr_strip"         : None})
    # 05-..-..-..
    curseScreens["usermain_screen"] = CurseScreen(**{
    "global_storage"    : global_storage,
    "screens"           : curseScreens,
    "user_strip"        : "usermain_scr_ustrip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "user_scr_menu_pnl",
    "can_panel_change"  : True,
    "style"             : curseStyles["dashscrbg"],
    "ftr_strip"         : "user_scr_footer"})
    # 06-..-..-..
    curseScreens["viewDB_screen"]   = CurseScreen(**{
    "global_storage"    : global_storage,
    "screens"           : curseScreens,
    "user_strip"        : "viewDB_scr_ustrip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "viewDB_scr_menu_pnl",
    "can_panel_change"  : False,
    "style"             : curseStyles["dashscrbg"],
    "ftr_strip"         : None})
    # 07-..-..-..
    curseScreens["manageDB_screen"] = CurseScreen(**{
    "global_storage"    : global_storage,
    "screens"           : curseScreens,
    "user_strip"        : "mngDBS_scr_ustrip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "mngDBS_scr_menu_pnl",
    "can_panel_change"  : False,
    "style"             : curseStyles["dashscrbg"],
    "ftr_strip"         : None})
    # 08-..-..-..
    curseScreens["cfg_acct_screen"] = CurseScreen(**{
    "global_storage"    : global_storage,
    "screens"           : curseScreens,
    "user_strip"        : "cfgAcct_scr_ustrip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : default_msg_map,
    "default_focus_key" : "cfgAcct_scr_menu_pnl",
    "can_panel_change"  : False,
    "style"             : curseStyles["dashscrbg"],
    "ftr_strip"         : None})

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def init_panels(curse_container):
    """ make the cursePanels for all curseScreens
    
    instantiate and set fields of screen child panels.
    all fields of a panel are set here EXCEPT:
        panel.items             (set in init_items)
        panel.textbox           (set in init_textboxes)
        panel.infotar           (set in load_targets)  
    """

    curseScreens = curse_container.screens      
    curseStyles = curse_container.styles       

    title_screen    = curseScreens["title_screen"]
    test_screen     = curseScreens["test_screen"]
    account_screen  = curseScreens["account_screen"]  
    about_screen    = curseScreens["about_screen"]
    login_screen    = curseScreens["login_screen"]
    user_screen     = curseScreens["usermain_screen"]
    viewDB_screen   = curseScreens["viewDB_screen"]  
    mngDBS_screen   = curseScreens["manageDB_screen"]  
    cfgAcct_screen  = curseScreens["cfg_acct_screen"]    

    panel_msg_map = curse_container.act_msg_maps["panel_msg_map2"]
    list_msg_map = curse_container.act_msg_maps["list_msg_map"]
    #panel_msg_map2 = curse_container.act_msg_maps["panel_msg_map2"]
    global_storage = curse_container.global_storage 
                                                                               
    # 00-03-..-..      y, x, h, w
    title_screen.panels["title_scr_background"]            = CursePanel(**{
    "global_storage"          : global_storage,
    "parent"                  : title_screen,
    "size"                    : (0, 0, 24, 80),   
    "style"                   : curseStyles["title_panel"]})
    # 00-00-..-..
    title_screen.panels["title_scr_user_strip"]            = CursePanel(**{
    "global_storage"          : global_storage,
    "parent"                  : title_screen,
    "size"                    : (0, 0, 1, 80), 
    "style"                   : curseStyles["user_strip"]})
    # 00-01-..-..
    title_screen.panels["title_scr_panel"]                 = CursePanel(**{
    "global_storage"          : global_storage,
    "act_msg_map"             : panel_msg_map,
    "parent"                  : title_screen,
    "size"                    : (1, 0, 20, 80),       
    "style"                   : curseStyles["title_panel"],
    "focusable"               : True,
    "_default_focus_item_key" : "login_link"})
    # 00-02-..-..
    title_screen.panels["title_scr_infopanel"]             = CursePanel(**{
    "global_storage"          : global_storage,
    "parent"                  : title_screen,
    "size"                    : (23, 0, 1, 80),   
    "style"                   : curseStyles["infobox2"]})
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
    "global_storage": global_storage,
    "parent"        : test_screen,
    "size"          : (0, 0, 1, 80),  
    "style"         : curseStyles["user_strip"]})
    # 01-01-..-.. 
    test_screen.panels["test_scr_upper_infopanel"]         = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : test_screen,    
    "size"          : (1, 0, 5, 80),
    "style"         : curseStyles["infobox1"],    
    "title"         : ("(INFOBOX 1)", 0, 1)})
    # 01-02-..-..
    test_screen.panels["test_scr_l_mid_panel"]             = CursePanel(**{
    "global_storage": global_storage,
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
    "global_storage": global_storage,
    "parent"        : test_screen,
    "act_msg_map"   : panel_msg_map,
    "size"          : (6, 20, 12, 69), 
    "style"         : curseStyles["middlepanes"],    
    "focusable"     : True,
    "title"         : ("(RIGHT MAIN PANE)", 0, 1),
    "info"          : teststr2,
    "infotar"       : "test_scr_upper_infopanel"})
    # 01-04-..-..
    test_screen.panels["test_scr_lower_infopanel"]         = CursePanel(**{
    "global_storage": global_storage,
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
        "test_scr_l_mid_panel",
        "test_scr_r_mid_panel",
        "test_scr_lower_infopanel",
        "test_scr_input_strip"]
    test_screen.panel_count = len(test_screen.panel_indexes)
                           
    ## 02-00-..-..      y, x, h, w
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
    # 02-07-..-..
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
    # 02-08-..-..
    account_screen.panels["acct_scr_name_strip"]           = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : account_screen,
    "title"         : ( "ACCOUNT NAME".center(18), 0, 0), 
    "size"          : (11, 31, 2, 18),
    "style"         : curseStyles["input_strip3"]})
    # 02-09-..-..
    account_screen.panels["acct_scr_pw_strip"]             = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : account_screen,
    "title"         : ( "ACCOUNT PASSWORD".center(18), 0, 0), 
    "size"          : (13, 31, 2, 18),
    "style"         : curseStyles["input_strip3"]})
    # 02-10-..-..
    account_screen.panels["acct_scr_back_panel"]           = CursePanel(**{
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
                                                                                                                                               
    # 03-00-..-..      y, x, h, w
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
    about_screen.panels["about_scr_footer"]                = CursePanel(**{
    "global_storage" : global_storage,
    "parent"        : about_screen,
    "size"          : (23, 0, 1, 80), # x. 23->22
    "style"         : curseStyles["infobox2"],
    "title"         : (
        "Press Z to return to Title Screen, if you dare...".center(79), 0, 0)})
    # panels are updated/ drawn in the order below- this affects
    # overlapping panels so pay attention to this! 
    about_screen.panel_indexes = [
        "about_scr_user_strip", 
        "about_scr_bg_text_art",
        "about_scr_team_txt_panel",
        "about_scr_footer"]
    about_screen.panel_count = len(about_screen.panel_indexes)

    # 04-00-..-..      y, x, h, w
    login_screen.panels["login_scr_bg"]                    = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "size"          : (0, 0, 24, 80),
    "style"         : curseStyles["at_scrbg"]}) 
    # 04-01-..-..
    login_screen.panels["login_scr_mid_bg_panel"]          = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "size"          : (8, 29, 10, 22),
    "style"         : curseStyles["middlepanes"]})
    # 04-02-..-.. 
    login_screen.panels["login_scr_user_strip"]            = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "size"          : (0, 0, 1, 80),
    "style"         : curseStyles["user_strip"]})     
    # 04-03-..-.. 
    login_screen.panels["login_scr_menu_pnl"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "act_msg_map"   : panel_msg_map,
    "size"          : (8, 7, 10, 22),
    "style"         : curseStyles["middlepanes"],   
    "focusable"     : True,
    "_default_focus_item_key" : "logname"})
    # 04-04-..-..
    login_screen.panels["login_scr_infobox"]               = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "size"          : (8, 51, 9, 22),
    "style"         : curseStyles["infobox2"]})
    # 04-05-..-..
    login_screen.panels["login_scr_name_strip"]            = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "size"          : (10, 31, 1, 18),
    "style"         : curseStyles["login_entry"]})
    # 04-06-..-..
    login_screen.panels["login_scr_pw_strip"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "size"          : (11, 31, 1, 18),
    "style"         : curseStyles["login_entry"]})
    # 04-07-..-..
    login_screen.panels["login_scr_db_strip"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "size"          : (12, 31, 1, 18),
    "style"         : curseStyles["login_entry"]})
    # 04-08-..-..
    login_screen.panels["login_scr_lang_optbox"]           = CursePanel(**{
    "global_storage": global_storage,
    "act_msg_map"   : panel_msg_map,
    "parent"        : login_screen,
    "size"          : (13, 31, 1, 18),
    "style"         : curseStyles["login_optionbox"],
    "_default_focus_item_key" : "OmySQL",
    "is_sec_focus"  : True})
    # 04-09
    login_screen.panels["login_scr_title_panel"]           = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "title"         : ("ACCOUNT LOGIN".center(16), 1, 3),
    "size"          : (4, 29, 3, 22),
    "style"         : curseStyles["middlepanes3"]})
    # 04-10
    login_screen.panels["login_scr_footer"]                = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "size"          : (23, 0, 1, 80),
    "style"         : curseStyles["input_strip"]})
                                
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
        "login_scr_pw_strip",
        "login_scr_db_strip",
        "login_scr_lang_optbox",
        "login_scr_footer"]
    login_screen.panel_count = len(login_screen.panel_indexes)

    # 05-00-..-..      y, x, h, w
    user_screen.panels["usermain_scr_bg"]                  = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : user_screen,
    "size"          : (0, 0, 24, 80),
    "style"         : curseStyles["title_panel"]}) 
    # 05-01-..-..
    user_screen.panels["usermain_scr_ustrip"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : user_screen,
    "size"          : (0, 0, 1, 80),
    "style"         : curseStyles["user_strip"]})  
    # 05-02-..-..
    user_screen.panels["usermain_scr_u_info"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : user_screen,    
    "size"          : (1, 0, 5, 80),
    "style"         : curseStyles["infobox1"]})
    # 05-03-..-..
    user_screen.panels["user_scr_menu_pnl"]                = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : user_screen,
    "title"         : ("USER MAIN MENU".center(18), 2, 1),
    "act_msg_map"   : panel_msg_map,
    "size"          : (6, 0, 12, 26 ),
    "style"         : curseStyles["middlepanes"],   
    "focusable"     : True,
    "info"          : "press SPACE to select item, q to quit, "\
                      "z to cancel, v to return to previous screen",
    "infotar"       : "usermain_scr_u_info",
    "_default_focus_item_key" : "viewDB_lnk"})
    # 05-04-..-..
    user_screen.panels["usermain_scr_m_pnl"]               = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : user_screen,
    "title"         : ("ACCOUNT DATABASES".center(19), 0, 2),
    "act_msg_map"   : panel_msg_map,
    "size"          : (6, 26, 12, 24), 
    "style"         : curseStyles["middlepanes"],    
    "focusable"     : True,
    "_default_focus_item_key" : "temp_db1",
    "info"          : "press SPACE to select item, q to quit, "\
                      "z to cancel, v to return to previous screen",
    "infotar"       : "usermain_scr_u_info"})
    # 05-05-..-..
    user_screen.panels["usermain_scr_l_info"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : user_screen,
    "size"          : (18, 0, 5, 80),
    "style"         : curseStyles["infobox2"]})
    # 05-06-..-..
    user_screen.panels["usermain_scr_r_pnl"]               = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : user_screen,
    "act_msg_map"   : list_msg_map,
    "size"          : (7, 51, 10, 29), 
    "style"         : curseStyles["usermain_listbox"],    
    "info"          : "use ARROW KEYS to browse list, q to quit, "\
                      "z to cancel, v to return to previous screen",
    "infotar"       : "usermain_scr_u_info",
    "is_pad"        : True,
    "psize"         : (1000, 1000)})
    # 05-07-..-..
    user_screen.panels["user_scr_footer"]                   = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : login_screen,
    "size"          : (23, 0, 1, 80),
    "style"         : curseStyles["input_strip"]})
    # panels are updated/ drawn in the order below- this affects
    # overlapping panels so pay attention to this!
    user_screen.panel_indexes = [
        "usermain_scr_bg",
        "user_scr_footer",
        "usermain_scr_u_info",
        "user_scr_menu_pnl",
        "usermain_scr_m_pnl",
        "usermain_scr_r_pnl",
        "usermain_scr_l_info",
        "usermain_scr_ustrip"]
    user_screen.panel_count = len(user_screen.panel_indexes)

    # 06-00-..-..      y, x, h, w
    viewDB_screen.panels["viewDB_scr_bg"]                  = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : viewDB_screen,
    "size"          : (0, 0, 24, 80),
    "style"         : curseStyles["title_panel"]})
    # 06-01-..-.. 
    viewDB_screen.panels["viewDB_scr_ustrip"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : viewDB_screen,
    "size"          : (0, 0, 1, 80),
    "style"         : curseStyles["user_strip"]})
    # 06-02-..-..
    viewDB_screen.panels["viewDB_scr_menu_pnl"]            = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : viewDB_screen,
    "title"         : ("VIEW DATABASE".center(18), 2, 1),
    "act_msg_map"   : panel_msg_map,
    "size"          : (6, 0, 12, 26 ),
    "style"         : curseStyles["middlepanes"],   
    "focusable"     : True})
    # panels are updated/ drawn in the order below- this affects
    # overlapping panels so pay attention to this!
    viewDB_screen.panel_indexes = [
        "viewDB_scr_bg",
        "viewDB_scr_menu_pnl",
        "viewDB_scr_ustrip"]
    viewDB_screen.panel_count = len(viewDB_screen.panel_indexes)

    # 07-00-..-..      y, x, h, w
    mngDBS_screen.panels["mngDBS_scr_bg"]                  = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : mngDBS_screen,
    "size"          : (0, 0, 24, 80),
    "style"         : curseStyles["title_panel"]})
    # 07-01-..-.. 
    mngDBS_screen.panels["mngDBS_scr_ustrip"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : mngDBS_screen,
    "size"          : (0, 0, 1, 80),
    "style"         : curseStyles["user_strip"]})
    # 07-02-..-..
    mngDBS_screen.panels["mngDBS_scr_menu_pnl"]            = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : mngDBS_screen,
    "title"         : ("MANAGE DATABASES".center(18), 2, 1),
    "act_msg_map"   : panel_msg_map,
    "size"          : (6, 0, 12, 26 ),
    "style"         : curseStyles["middlepanes"],   
    "focusable"     : True})
    # panels are updated/ drawn in the order below- this affects
    # overlapping panels so pay attention to this!
    mngDBS_screen.panel_indexes = [
        "mngDBS_scr_bg",
        "mngDBS_scr_menu_pnl",
        "mngDBS_scr_ustrip"]
    mngDBS_screen.panel_count = len(mngDBS_screen.panel_indexes)

    # 08-00-..-..      y, x, h, w
    cfgAcct_screen.panels["cfgAcct_scr_bg"]                = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : cfgAcct_screen,
    "size"          : (0, 0, 24, 80),
    "style"         : curseStyles["title_panel"]})
    # 08-01-..-.. 
    cfgAcct_screen.panels["cfgAcct_scr_ustrip"]            = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : cfgAcct_screen,
    "size"          : (0, 0, 1, 80),
    "style"         : curseStyles["user_strip"]})
    # 08-02-..-..
    cfgAcct_screen.panels["cfgAcct_scr_menu_pnl"]          = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : cfgAcct_screen,
    "title"         : ("ACCOUNT CONFIG".center(18), 2, 1),
    "act_msg_map"   : panel_msg_map,
    "size"          : (6, 0, 12, 26 ),
    "style"         : curseStyles["middlepanes"],   
    "focusable"     : True})
    # panels are updated/ drawn in the order below- this affects
    # overlapping panels so pay attention to this!
    cfgAcct_screen.panel_indexes = [
        "cfgAcct_scr_bg",
        "cfgAcct_scr_menu_pnl",
        "cfgAcct_scr_ustrip"]
    cfgAcct_screen.panel_count = len(cfgAcct_screen.panel_indexes)
    
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def init_items(curse_container):
    """ make the curseItems for all cursePanels

    instantiate and set fields of panel child items. 
    all fields of an item are set here EXCEPT:
        item.infotar 
    """
    curseStyles         = curse_container.styles            #["styles"]
    colors              = curseStyles["COLORS"]
    curseScreens        = curse_container.screens           #["screens"]

    global_storage      = curse_container.global_storage    #["global_storage"]

    title_panels        = curseScreens["title_screen"].panels
    test_panels         = curseScreens["test_screen"].panels
    account_panels      = curseScreens["account_screen"].panels
    about_scr_panels    = curseScreens["about_screen"].panels
    login_scr_panels    = curseScreens["login_screen"].panels
    user_scr_panels     = curseScreens["usermain_screen"].panels
    

    # 00-01-..-00
    title_panels["title_scr_panel"].items["login_link"]    = CurseItem(**{ 
    "container"     : curse_container,
    "global_storage": global_storage,
    "parent"        : title_panels["title_scr_panel"],
    "parent_screen" : curseScreens["title_screen"],
    "size"          : (15, 30, 1, 20), # y, x, h, w
    "style"         : curseStyles["title_menu"],
    "label"         : "log in".center(20),
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "main", 
        recv_name   = "main",   
        on_recv     = "call_function", 
        recv_act    = "changeScreen",
        recv_args   = ["login_screen"],
        ret_info    = None)})
    # 00-01-..-01
    title_panels["title_scr_panel"].items["act_create_lk"] = CurseItem(**{ 
    "container" : curse_container,
    "global_storage": global_storage,
    "parent"        : title_panels["title_scr_panel"],
    "parent_screen" : curseScreens["title_screen"],
    "size"          : (16, 30, 1, 20), # y, x, h, w
    "style"         : curseStyles["title_menu"],
    "label"         : "(x) create account".center(20),
    "active"        : False,
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "main", 
        recv_name   = "main",   
        on_recv     = "call_function", 
        recv_act    = "changeScreen",
        recv_args   = ["account_screen"],
        ret_info    = None)})
    # 00-01-..-03
    title_panels["title_scr_panel"].items["usr_main_link"] = CurseItem(**{ 
    "container"     : curse_container,
    "global_storage": global_storage,
    "parent"        : title_panels["title_scr_panel"],
    "parent_screen" : curseScreens["title_screen"],
    "size"          : (17, 30, 1, 20), # y, x, h, w
    "style"         : curseStyles["title_menu"],
    "label"         : " user portal".center(20),
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "main", 
        recv_name   = "main",   
        on_recv     = "call_function", 
        recv_act    = "changeScreen",
        recv_args   = ["usermain_screen"],
        ret_info    = None)})
    # 00-01-..-02
    title_panels["title_scr_panel"].items["about_DB_link"] = CurseItem(**{ 
    "container" : curse_container,
    "global_storage" : global_storage,
    "parent"        : title_panels["title_scr_panel"],
    "parent_screen"  : curseScreens["title_screen"],
    "size"          : (18, 30, 1, 20), # y, x, h, w
    "style"         : curseStyles["title_menu"],
    "label"         : "about curseDB".center(21),
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "main", 
        recv_name   = "main",   
        on_recv     = "call_function", 
        recv_act    = "changeScreen",
        recv_args   = ["about_screen"],
        ret_info    = None)})
    title_panels["title_scr_panel"].item_indexes = [
        "login_link", 
        "act_create_lk",
        "usr_main_link", 
        "about_DB_link"]
    title_panels["title_scr_panel"].item_count = len(
        title_panels["title_scr_panel"].item_indexes)

    # 01-03-..-00
    test_panels["test_scr_r_mid_panel"].items["list_hdr"]  = CurseItem(**{ 
        "container" : curse_container,
    "global_storage" : global_storage,
    "parent"        : test_panels["test_scr_r_mid_panel"],
    "parent_screen"  : curseScreens["test_screen"],
    "size"          : (2, 3, 4, 10), # y, x, h, w
    "style"         : test_panels["test_scr_r_mid_panel"].style,
    "label"         : "header",
    "focusable"     : False })
    # 01-03-..-01
    test_panels["test_scr_r_mid_panel"].items["item1"]     = CurseItem(**{ 
        "container" : curse_container,
    "global_storage" : global_storage,
    "parent"        : test_panels["test_scr_r_mid_panel"],
    "parent_screen"  : curseScreens["test_screen"],
    "size"          : (3, 3, 4, 10), # y, x, h, w
    "style"         : test_panels["test_scr_r_mid_panel"].style,
    "label"         : "item1"})
    # 01-03-..-02
    test_panels["test_scr_r_mid_panel"].items["item2"]     = CurseItem(**{ 
        "container" : curse_container,
    "global_storage" : global_storage,
    "parent"        : test_panels["test_scr_r_mid_panel"],
    "parent_screen"  : curseScreens["test_screen"],
    "size"          : (4, 3, 4, 10), # y, x, h, w
    "style"         : test_panels["test_scr_r_mid_panel"].style,
    "label"         : "item2"})
    # 01-03-..-03
    test_panels["test_scr_r_mid_panel"].items["item3"]     = CurseItem(**{ 
        "container" : curse_container,
    "global_storage" : global_storage,
    "parent"       : test_panels["test_scr_r_mid_panel"],
    "parent_screen"  : curseScreens["test_screen"],
    "size"          : (5, 3, 4, 10), # y, x, h, w
    "style"         : test_panels["test_scr_r_mid_panel"].style,
    "label"         : "item3"})
    test_panels["test_scr_r_mid_panel"].item_indexes = [
        "list_hdr", 
        "item1", 
        "item2",
        "item3"]
    test_panels["test_scr_r_mid_panel"].item_count = len(
        test_panels["test_scr_r_mid_panel"].item_indexes)


    # 02-05-..-00       IFUNC_001
    account_panels["acct_scr_mid_panel"].items["username"] = CurseItem(**{ 
    "container" : curse_container,
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
    # 02-05-..-01       IFUNC_001
    account_panels["acct_scr_mid_panel"].items["password"] = CurseItem(**{ 
    "container" : curse_container,
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
    # 02-05-..-02       IFUNC_001
    account_panels["acct_scr_mid_panel"].items["submit_acct"]=CurseItem(**{
    "container" : curse_container,
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
    account_panels["acct_scr_mid_panel"].item_indexes = [
        "username", 
        "password",
        "submit_acct"]
    account_panels["acct_scr_mid_panel"].item_count = len(
        account_panels["acct_scr_mid_panel"].item_indexes)


    # 03-..-..-..
    pass


    # 04-03-..-00       IFUNC_001 (getEntry)
    login_scr_panels["login_scr_menu_pnl"].items["logname"]= CurseItem(**{ 
    "container"     : curse_container,
    "global_storage": global_storage,
    "parent"        : login_scr_panels["login_scr_menu_pnl"],
    "parent_screen" : curseScreens["login_screen"],
    "size"          : (2, 3, 4, 10), # y, x, h, w
    "style"         : login_scr_panels["login_scr_menu_pnl"].style,
    "label"         : "USERNAME".center(16),
    "info"          : "press SPACE to enter database log-in name "\
                      "................. "\
                      "hit RETURN to finish entry",
    "infotar"       : "login_scr_infobox",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item",
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "getEntry",
        recv_args   = [
            "login_scr_name_strip", colors["RGRN"], "1100", (4,64,17), 
            (True,False,False),global_storage,"log_name","login_scr_infobox"],
        ret_info    = None)})
    # 04-03-..-01       IFUNC_001 (getEntry)
    login_scr_panels["login_scr_menu_pnl"].items["logpw"]  = CurseItem(**{ 
    "container"     : curse_container,
    "global_storage": global_storage,
    "parent"        : login_scr_panels["login_scr_menu_pnl"],
    "parent_screen" : curseScreens["login_screen"],
    "size"          : (3, 3, 4, 10), # y, x, h, w
    "style"         : login_scr_panels["login_scr_menu_pnl"].style,
    "label"         : "PASSWORD".center(16),
    "info"          : "press SPACE to enter database log-in password "\
                      "................. "\
                      "hit RETURN to finish entry",
    "infotar"       : "login_scr_infobox",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item",
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "getEntry",
        recv_args   = [
            "login_scr_pw_strip", curses.color_pair(10), "1101", (4,64,17), 
            (True,True,False),global_storage,"log_pw","login_scr_infobox"],
        ret_info    = None)})
    # 04-03-..-02       IFUNC_001 (getEntry)
    login_scr_panels["login_scr_menu_pnl"].items["logdb"]  = CurseItem(**{ 
    "container"     : curse_container,
    "global_storage": global_storage,
    "parent"        : login_scr_panels["login_scr_menu_pnl"],
    "parent_screen" : curseScreens["login_screen"],
    "size"          : (4, 3, 4, 10), # y, x, h, w
    "style"         : login_scr_panels["login_scr_menu_pnl"].style,
    "label"         : "DATABASE NAME".center(16),
    "info"          : "press SPACE to enter database name\n"\
                      "................. "\
                      "hit RETURN to finish entry",
    "infotar"       : "login_scr_infobox",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item",
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "getEntry",
        recv_args   = [
            "login_scr_db_strip", curses.color_pair(10), "1100", (4,64,17), 
            (True,False,False),global_storage,"log_db","login_scr_infobox",
            "login_scr_footer"],
        ret_info    = None)})
    # 04-03-..-03       IFUNC_002 (getOption)
    login_scr_panels["login_scr_menu_pnl"].items["loglang"]= CurseItem(**{ 
    "container"     : curse_container,
    "global_storage": global_storage,
    "parent"        : login_scr_panels["login_scr_menu_pnl"],
    "parent_screen" : curseScreens["login_screen"],
    "size"          : (5, 3, 4, 10), # y, x, h, w
    "style"         : login_scr_panels["login_scr_menu_pnl"].style,
    "label"         : "QUERY LANGUAGE".center(16),
    "info"          : "use TAB to select database query language\n"\
                      "................. "\
                      "press SPACE to select language",
    "infotar"       : "login_scr_infobox",
    #"_focus_key"    : "login_scr_lang_optbox",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item",
        recv_layer  = "screen", 
        recv_name   = "login_screen",   
        on_recv     = "call_function", 
        recv_act    = "openNestedPanel",
        recv_args   = ["login_scr_lang_optbox"],
        ret_info    = None)})
    # 04-03-..-04       IFUNC_003 (logSubmit)
    login_scr_panels["login_scr_menu_pnl"].items["logsubmit"]=CurseItem(**{
    "container"     : curse_container,
    "global_storage": global_storage,
    "parent"        : login_scr_panels["login_scr_menu_pnl"],
    "parent_screen" : curseScreens["login_screen"],
    "size"          : (7, 3, 4, 10), # y, x, h, w
    "style"         : login_scr_panels["login_scr_menu_pnl"].style,
    "label"         : "SUBMIT".center(16),
    "info"          : "press SPACE to submit login credentials",
    "infotar"       : "login_scr_infobox",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item",
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "databaseLoginTest",
        recv_args   = ["login_scr_infobox"],
        ret_info    = None)})
    login_scr_panels["login_scr_menu_pnl"].item_indexes = [
        "logname", 
        "logpw",
        "logdb",
        "loglang",
        "logsubmit"]
    login_scr_panels["login_scr_menu_pnl"].item_count = len(
        login_scr_panels["login_scr_menu_pnl"].item_indexes)

    # 04-08-..-00
    login_scr_panels["login_scr_lang_optbox"].items["OmySQL"]=CurseItem(**{
    "container"     : curse_container,
    "global_storage": global_storage,
    "parent"        : login_scr_panels["login_scr_lang_optbox"],
    "parent_screen" : curseScreens["login_screen"],
    "size"          : (0, 0, 1, 5), # y, x, h, w
    "style"         : curseStyles["login_optionbox"],
    "label"         : "mySQL",
    "info"          : "login database uses mySQL",
    "infotar"       : "login_scr_infobox",    
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item",
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "setOption",
        recv_args   = [
                        login_scr_panels["login_scr_lang_optbox"],
                        global_storage, 
                        "log_lang",
                        True ],
        #recv_act    = "getOption",
        #recv_args   = ["login_scr_lang_optbox", global_storage, "log_lang"],
        ret_info    = None)})
    # 04-08-..-01
    login_scr_panels["login_scr_lang_optbox"].items["Opostgre"]=CurseItem(**{
    "container"     : curse_container,
    "global_storage": global_storage,
    "parent"        : login_scr_panels["login_scr_lang_optbox"],
    "parent_screen" : curseScreens["login_screen"],
    "size"          : (0, 8, 1, 10), # y, x, h, w
    "style"         : curseStyles["login_optionbox"],
    "label"         : "postgresql",
    "info"          : "login database uses postgresql",
    "infotar"       : "login_scr_infobox",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item",
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "setOption",
        recv_args   = [
                        login_scr_panels["login_scr_lang_optbox"],
                        global_storage, 
                        "log_lang",
                        True ],
        #recv_act    = "getOption",
        #recv_args   = ["login_scr_lang_optbox", global_storage, "log_lang"],
        ret_info    = None)    })
    login_scr_panels["login_scr_lang_optbox"].item_indexes = [
        "OmySQL", 
        "Opostgre"]
    login_scr_panels["login_scr_lang_optbox"].item_count = len(
        login_scr_panels["login_scr_lang_optbox"].item_indexes)


    # 05-03-..-00
    user_scr_panels["user_scr_menu_pnl"].items["hdr"]      = CurseItem(**{ 
        "container" : curse_container,
    "global_storage": global_storage,
    "parent"        : user_scr_panels["user_scr_menu_pnl"],
    "parent_screen" : curseScreens["usermain_screen"],
    "size"          : (3, 3, 4, 20), # y, x, h, w
    "style"         : user_scr_panels["user_scr_menu_pnl"].style,
    "label"         : "",
    "focusable"     : False })
    # 05-03-..-01
    user_scr_panels["user_scr_menu_pnl"].items["viewDB_lnk"]=CurseItem(**{
    "container"     : curse_container,
    "global_storage": global_storage,
    "parent"        : user_scr_panels["user_scr_menu_pnl"],
    "parent_screen" : curseScreens["usermain_screen"],
    "size"          : (4, 3, 4, 20), # y, x, h, w
    "style"         : user_scr_panels["user_scr_menu_pnl"].style,
    "label"         : "view database",
    "info"          : ""\
        "view all databases that you can access with current privileges",
    "infotar"       : "usermain_scr_l_info", 
    #"_focus_key"    : "usermain_scr_m_pnl",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item",
        recv_layer  = "screen", 
        recv_name   = "login_screen",   
        on_recv     = "call_function", 
        recv_act    = "openNestedPanel",
        recv_args   = ["usermain_scr_m_pnl"],
        ret_info    = None)})
    # 05-03-..-02
    user_scr_panels["user_scr_menu_pnl"].items["mngDBS_lnk"]= CurseItem(**{
        "container" : curse_container,
    "global_storage": global_storage,
    "parent"        : user_scr_panels["user_scr_menu_pnl"],
    "parent_screen" : curseScreens["usermain_screen"],
    "size"          : (5, 3, 4, 20), # y, x, h, w
    "style"         : user_scr_panels["user_scr_menu_pnl"].style,
    "label"         : "manage databases",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "main", 
        recv_name   = "main",   
        on_recv     = "call_function", 
        recv_act    = "changeScreen",
        recv_args   = ["manageDB_screen"],
        ret_info    = None)})
    # 05-03-..-03
    user_scr_panels["user_scr_menu_pnl"].items["cfgAcct_lnk"]=CurseItem(**{
        "container" : curse_container,
    "global_storage": global_storage,
    "parent"        : user_scr_panels["user_scr_menu_pnl"],
    "parent_screen" : curseScreens["usermain_screen"],
    "size"          : (6, 3, 4, 20), # y, x, h, w
    "style"         : user_scr_panels["user_scr_menu_pnl"].style,
    "label"         : "edit account options",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "main", 
        recv_name   = "main",   
        on_recv     = "call_function", 
        recv_act    = "changeScreen",
        recv_args   = ["cfg_acct_screen"],
        ret_info    = None)})
    # 05-03-..-04
    user_scr_panels["user_scr_menu_pnl"].items["logout"]    = CurseItem(**{
        "container" : curse_container,
    "global_storage": global_storage,
    "parent"        : user_scr_panels["user_scr_menu_pnl"],
    "parent_screen" : curseScreens["usermain_screen"],
    "size"          : (7, 3, 4, 20), # y, x, h, w
    "style"         : user_scr_panels["user_scr_menu_pnl"].style,
    "label"         : "log out"})
    user_scr_panels["user_scr_menu_pnl"].item_indexes = [
        "hdr", 
        "viewDB_lnk", 
        "mngDBS_lnk",
        "cfgAcct_lnk",
        "logout"]
    user_scr_panels["user_scr_menu_pnl"].item_count = len(
        user_scr_panels["user_scr_menu_pnl"].item_indexes)

    # 05-04-..-00T
    user_scr_panels["usermain_scr_m_pnl"].items["temp_db1"] = CurseItem(**{ 
    "container"     : curse_container,
    "global_storage": global_storage,
    "parent"        : user_scr_panels["usermain_scr_m_pnl"],
    "parent_screen" : curseScreens["usermain_screen"],
    "size"          : (4, 3, 4, 18), # y, x, h, w
    "style"         : user_scr_panels["usermain_scr_m_pnl"].style,
    "label"         : "database 1",
    "selectable"    : True,
    "info"          : "select database to view tables",
    "infotar"       : "usermain_scr_l_info", 
    #"_focus_key"    : "usermain_scr_r_pnl",
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "loadResult",
        recv_args   = [
            ["dinner dog loves a hog fallen in the winter bog-"\
             "though he's broken all his wheels and cogs",
             "while like a ghastly rapid river, through the pale door, "\
             "a hideous throng rush out forever, and laugh- but smile no more",
             "And all our yesterdays have lighted fools the way "\
             "to dusty death. Out, out, brief candle! Life's but a walking "\
             "shadow, a poor player, That struts and frets his hour upon the "\
             "stage, and then is heard no more. It is a tale told by an "\
             "idiot, full of sound and fury, Signifying nothing",
             "`My name is Ozymandias, King of Kings: Look on my works, ye "\
             "mighty, and despair!' Nothing beside remains. Round the decay "\
             "that colossal wreck, boundless and bare,"\
             "The lone and level sands stretch far away",
             "LINE #5", "LINE #6", "LINE #7",
             "LINE #8", "LINE #9", "LINE #10",
             "LINE #11","LINE #12","LINE #13",
             "LINE #14","LINE #15","LINE #16",
             "17", "18", "19"],
             "usermain_scr_r_pnl", True],
        ret_info    = None)})
    # 05-04-..-01T
    user_scr_panels["usermain_scr_m_pnl"].items["temp_db2"] = CurseItem(**{
        "container" : curse_container,
    "global_storage": global_storage,
    "parent"        : user_scr_panels["usermain_scr_m_pnl"],
    "parent_screen" : curseScreens["usermain_screen"],
    "size"          : (5, 3, 4, 18), # y, x, h, w
    "style"         : user_scr_panels["usermain_scr_m_pnl"].style,
    "label"         : "database 2",
    "selectable"    : True})
    # 05-04-..-02T
    user_scr_panels["usermain_scr_m_pnl"].items["temp_db3"] = CurseItem(**{
        "container" : curse_container,
    "global_storage": global_storage,
    "parent"        : user_scr_panels["usermain_scr_m_pnl"],
    "parent_screen" : curseScreens["usermain_screen"],
    "size"          : (6, 3, 4, 18), # y, x, h, w
    "style"         : user_scr_panels["usermain_scr_m_pnl"].style,
    "label"         : "database 3",
    "selectable"    : True})
    user_scr_panels["usermain_scr_m_pnl"].item_indexes = [
        "temp_db1",
        "temp_db2",
        "temp_db3"]
    user_scr_panels["usermain_scr_m_pnl"].item_count = len(
        user_scr_panels["usermain_scr_m_pnl"].item_indexes)

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def init_textboxes(curse_container):

    title_panels   = curse_container.screens["title_screen"].panels
    #["screens"]["title_screen"].panels
    test_panels    = curse_container.screens["test_screen"].panels
    #["screens"]["test_screen"].panels
    account_panels = curse_container.screens["account_screen"].panels
    #["screens"]["account_screen"].panels
    about_panels   = curse_container.screens["about_screen"].panels
    #["screens"]["about_screen"].panels
    login_panels   = curse_container.screens["login_screen"].panels
    #["screens"]["login_screen"].panels
    usermain_panels   = curse_container.screens["usermain_screen"].panels
    #["screens"]["usermain_screen"].panels

    curse_styles   = curse_container.styles #["styles"]
    
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
            size        = (1, 2, 6, 18),   
            style       = curse_styles["infobox2"],
            center      = True))
    
    # 05-02-00-..          y, x, h, w 
    usermain_panels["usermain_scr_u_info"].textbox   = CurseTextbox(**dict(
        parent      = usermain_panels["usermain_scr_u_info"],
        base_text   = "",
        size        = (1, 4, 3, 72),  
        style       = curse_styles["infobox1"]))
    # 05-05-00-..
    usermain_panels["usermain_scr_l_info"].textbox   = CurseTextbox(**dict(
        parent      = usermain_panels["usermain_scr_l_info"],
        base_text   = "",
        size        = (0, 1, 3, 78), 
        style       = curse_styles["infobox2"]))

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def load_targets(curse_container):
    """ assign item/panel infotars to object references named in infotar_str"""
    for screen_key in curse_container.screens:  #["screens"]:
        screen = curse_container.screens[screen_key]   #["screens"][screen_key]
        screen.user_strip = screen.panels[screen.user_strip_str]
        if screen.ftr_strip_str != None:
            screen.ftr_strip = screen.panels[screen.ftr_strip_str]
        else:       screen.ftr_strip = None
        for panel_key in screen.panels:
            panel = screen.panels[panel_key]
            if panel.infotar_str != None:
                panel.infotar = screen.getPanelByName(panel.infotar_str)
            for item_key in panel.items:
                item = panel.items[item_key]
                if item.infotar_str != None:
                    item.infotar = screen.panels[item.infotar_str]

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def init_act_msg_maps():
# key-action map:   ordinal converted keyboard input to action string
# action map    :   action string to message
#           key:    action string
#           value:  a "message" as defined below
#
# readMessage() :   message to command execution / function call
#    
    act_msg_maps = {
        "screen"        : {
                "forward"   : dict(  msg_status  = "unread", 
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
                    ret_info    = None),
                "user_scr"  : dict(  msg_status  = "unread", 
                    send_layer  = "screen", 
                    recv_layer  = "main", 
                    recv_name   = "main",   
                    on_recv     = "call_function", 
                    recv_act    = "changeScreen", 
                    recv_args   = ["usermain_screen"],
                    ret_info    = None),
                "test_scr"  : dict(  msg_status  = "unread", 
                    send_layer  = "screen", 
                    recv_layer  = "main", 
                    recv_name   = "main",   
                    on_recv     = "call_function", 
                    recv_act    = "changeScreen", 
                    recv_args   = ["test_screen"],
                    ret_info    = None)},
        "user_screen"   : {
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
                    ret_info    = None),
                "user_scr"  : dict(  msg_status  = "unread", 
                    send_layer  = "screen", 
                    recv_layer  = "main", 
                    recv_name   = "main",   
                    on_recv     = "call_function", 
                    recv_act    = "changeScreen", 
                    recv_args   = ["usermain_screen"],
                    ret_info    = None),
                "test_scr"  : dict(  msg_status  = "unread", 
                    send_layer  = "screen", 
                    recv_layer  = "main", 
                    recv_name   = "main",   
                    on_recv     = "call_function", 
                    recv_act    = "changeScreen", 
                    recv_args   = ["test_screen"],
                    ret_info    = None)},
        "login_screen"  : {
                "back"      : dict(  msg_status  = "unread", 
                    send_layer  = "screen", 
                    recv_layer  = "self", 
                    recv_name   = "self",   
                    on_recv     = "call_function", 
                    recv_act    = "prevSecondaryItem",
                    recv_args   = None,
                    ret_info    = None),
                "forward"   : dict(  msg_status  = "unread", 
                    send_layer  = "screen", 
                    recv_layer  = "self", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "nextsecondaryItem",
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
                    ret_info    = None),
                "user_scr"  : dict(  msg_status  = "unread", 
                    send_layer  = "screen", 
                    recv_layer  = "main", 
                    recv_name   = "main",   
                    on_recv     = "call_function", 
                    recv_act    = "changeScreen", 
                    recv_args   = ["usermain_screen"],
                    ret_info    = None),
                "test_scr"  : dict(  msg_status  = "unread", 
                    send_layer  = "screen", 
                    recv_layer  = "main", 
                    recv_name   = "main",   
                    on_recv     = "call_function", 
                    recv_act    = "changeScreen", 
                    recv_args   = ["test_screen"],
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
                "right"     : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "self", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "turnPage",
                    recv_args   = ["next", "infotar"],
                    ret_info    = None),
                "up"        : dict(  msg_status  = "unread", 
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
                "select"    : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "self", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "select",
                    recv_args   = None,
                    ret_info    = None)},
        "panel_msg_map2": {
                "left"        : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "self", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "prevItem",
                    recv_args   = None,
                    ret_info    = None),
                "right"      : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "self", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "nextItem",
                    recv_args   = None,
                    ret_info    = None),
                "up"        : dict(  msg_status  = "unread", 
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
                "select"    : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "self", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "selectItem",
                    recv_args   = None,
                    ret_info    = None),
                "cancel"    : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "screen", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "closeNestedPanel",
                    recv_args   = [False],
                    ret_info    = None)},
        "list_msg_map"  : {
                "left"        : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "panel", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "scrollLeft",
                    recv_args   = None,
                    ret_info    = None),
                "right"      : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "panel", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "scrollRight",
                    recv_args   = None,
                    ret_info    = None),
                "up"        : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "panel", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "prevListItem",
                    recv_args   = None,
                    ret_info    = None),
                "down"      : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "panel", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "nextListItem",
                    recv_args   = None,
                    ret_info    = None),
                "select"    : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "panel", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "selectItem",
                    recv_args   = None,
                    ret_info    = None),
                "cancel"    : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "screen", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "closeNestedPanel",
                    recv_args   = [False],
                    ret_info    = None)} }

    return act_msg_maps

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def init_funcs(curse_container):
    curseStyles         = curse_container.styles #["styles"]
    colors              = curseStyles["COLORS"]
    curseScreens        = curse_container.screens #["screens"]

    title_panels       = curseScreens["title_screen"].panels
    test_panels        = curseScreens["test_screen"].panels
    account_panels     = curseScreens["account_screen"].panels
    about_scr_panels   = curseScreens["about_screen"].panels
    login_panels       = curseScreens["login_screen"].panels
    user_panels        = curseScreens["usermain_screen"].panels

    
    #------------------ FUNCTION DEFINITIONS ----------------------------------
    # IFUNC_001
    def getEntry(self,out_panel_key, out_attr, val_str, val_range, modes,
                 out_storage,out_storage_key, out_infobox_parent_key,ftr=None):
        """ gets user input from passed UI component and stores it
        
        out_panel_key:   key of panel where user input is echo'd
        out_attr:        display attributes of echo'd output
        val_str:         validation string for input (see item.validate_char)
        modes:           boolean list for echo,password, and cleanup modes
        out_storage:     dictionary to store input in, if successful
        out_storage_key: key name for stored input
        out_infobox_parent_key: dictionary key to panel that will display 
            error messages or instructions for entry
        ftr:             (DEBUG) footer panel key used to display database name
        """
        panel =self.container.getPanelByName(out_panel_key)
        screen=panel.parent_screen
        entry =self.getUserString(
            val_str, out_attr, panel, (0,0), val_range, modes)
        if entry[0] == "OK_DONE":
            out_storage[out_storage_key] = copy.copy(entry[1])
            screen.setUserStripInfo()
            screen.drawUserStripInfo()
            #DEBUG
            if ftr != None:
                ftr_panel = self.container.getPanelByName(ftr)
                ftr_panel.win.hline(0,0,32,79)
                ftr_panel.win.addstr(0,1,entry[1])
                ftr_panel.refreshPanel()
        else:
            out_infobox=self.container.getTextboxByName(out_infobox_parent_key)
            self.showErrorMsg(entry[0], [ val_range[0] ], True, out_infobox)
            #if out_storage_key in out_storage: del out_storage[out_storage_key]
            #DEBUG
            if ftr != None:
                ftr_panel = self.container.getPanelByName(ftr)
                ftr_panel.win.hline(0,0,32,79)
                ftr_panel.refreshPanel()

    # IFUNC_002
    def getOption(self, optbox_key, out_storage, out_storage_key):
        panel =self.container.getPanelByName(optbox_key)
        # set the item to be the panel's "selected option"
        if not hasattr(panel, "opt_selected"):
            setattr(panel, "opt_selected", panel.focus_key)
        else:
            panel.opt_selected = panel.focus_key

        # defocus other items
        for i in panel.items:
            if i != panel.focus_key:
                panel.items[i].defocus()

        # store label
        screen=panel.parent_screen
        option = panel.focus_item.label
        out_storage[out_storage_key] = copy.copy(option)      
        #DEBUG
        screen.setUserStripInfo()
        screen.drawUserStripInfo()
  
    def setOption(self, parent_panel, out_storage, out_storage_key, go_back):
        out_storage[out_storage_key] = self.label
        screen=parent_panel.parent_screen
        #INSERT CODE TO SET SELECT STATUS
        if go_back == True:
            parent_panel.parent_screen.closeNestedPanel(True)
        screen.setUserStripInfo()
        screen.drawUserStripInfo()

    # IFUNC_003
    #def submitInfo(self, query_keys_pair, req_keys_pair, storage, s_keys, 
    #        db_funcs, infobox_parent_key):
    #    """ takes stored input and submits to database   
        
    #    query_keys <list>   : fields needed to compose database query string
    #    req_keys <list>     : if the element at a list index is None, then the
    #        relative query key VALUE is required, if it is not None, then that
    #        element is the default value for that query key
    #    storage <dict>      : where the input is stored
    #    storage_keys <str>  : keys to storage dictionary for values that will
    #        fill values for analogous query keys
    #    db_funcs<func>      : tuple for (mysql, postgresql) db IntrF functions
    #    infobox_parent_key  : used to get textbox that shows info/error msg
    #    """
    #    q_dict      = {}
    #    err         = False
    #    err_key     = None
    #    i_box = self.container.getTextboxByName(infobox_parent_key)

    #    lang = storage["log_lang"]

    #    # check if each key need for the query is in storage
    #    # if it's not, check if it's required
    #    # if it is required, abort submission and report error
    #    # if it isn't required, use default value and continue
            
    #    # lang should exist if you made it this far   
    #    lang = storage["log_lang"]
    #    if lang=="mySQL":        i = 0
    #    elif lang=="postgresql": i = 1
    #    """  
    #        makes a dictionary from the passed query keys and global storage
    #        values that is in turn given to the database interface function
    #    """
    #    for k in range(0, len(query_keys_pair[i])):
    #        # if there's not a key/value pair, is there a default value?
    #        if s_keys[i][k] not in storage:
    #            if req_keys_pair[i][k] != None:     
    #                q_dict[query_keys_pair[i][k]] = req_keys_pair[i][k]
    #            else: 
    #                return self.showErrorMsg("NOKEY",[s_keys[i][k]],True,i_box)
    #        else:   q_dict[query_keys_pair[i][k]] = storage[s_keys[i][k]]
    #    db_func = db_funcs[i]
    #    # ~ ~ ~ DB / UI INTERFACE CODE ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #    if db_func != None:
    #        if lang == "mySQL":
    #            """ CALL MYSQL QUERY """
    #            q_dict['query'] = "placeholder"
    #            q_res = db_func(q_dict)#, "SELECT * FROM COUNTRY LIMIT 3")
    #            if type(q_res) is str:  out_str = q_res
    #            else:  out_str = q_res['fail'].pgerror
    #        elif lang == "postgresql":
    #            """ CALL POSTGRESQL QUERY """
    #            try:
    #                results = db_func(q_dict)
    #                if isinstance(results, OperationalError):
    #                    out_str = results.pgerror
    #                else:
    #                    out_str = ""
    #                    results_keys = results.keys()
    #                    for r in range(0, len(results_keys)):
    #                        out_str+results_keys[r]+":"\
    #                            +results[results_keys[r]]+" "
    #            except OperationalError as e:     out_str = e.pgerror
    #    else:   out_str = "NO LANGUAGE SPECIFIED! HOW DID THIS HAPPEN?!"
    #    i_box.resetText(out_str)
    #    i_box.drawText()
    #    i_box.parent.win.refresh()

    def databaseLoginTest(self, infobox_pkey):
        gs = self.global_storage
        if "log_lang" in gs:
            lang = gs["log_lang"] # get qlang
            if lang == "mySQL" or lang == "postgresql":
                # get login arguments from global storage
                l_args = dict(
                        database = gs["log_db"],
                        user     = gs["log_name"],
                        host     = 'localhost',
                        password = gs["log_pw"])
                        
                # execute DB interface functions
                if lang=="mySQL":l_result=curseMysqlTemp.loginMysqlTest(l_args)
                else: l_result=cursesPostgresTemp.loginPostgresqlTest(l_args)

                if 'success' in l_result: status = { "status": "OK" }
                elif 'fail' in l_result: 
                    if lang == "mySQL":
                        status = {
                            "status":"ERR", 
                            "info": str(l_result['fail'])}
                    else:
                        status={"status":"ERR","info":l_result['fail'].pgerror}
            else: status = { "status": "ERR", "info": "bad language value" }
        else: status = { "status": "ERR", "info": "language field not set" }

        # draw results
        i_box = self.container.getTextboxByName(infobox_pkey)
        i_box.resetText(json.dumps(status["info"]))
        i_box.drawText()
        i_box.parent.win.refresh()

        # close connection
        if hasattr(gs, "connection"):
            gs["connection"].close()
        

    # IFUNC_004
    def loadResult(self, result_list, out_panel_key, focus_nested_panel=False):
        panel =self.container.getPanelByName(out_panel_key)
        #
        if hasattr(panel, "_inner_list"):
            setattr(panel,"_inner_list", list(result_list))
        else:         panel._inner_list = list(result_list)
        panel.loadList()
        if focus_nested_panel == True:
            self.parent_screen.openNestedPanel(out_panel_key)

    #------------------ FUNCTION ASSIGNMENT -----------------------------------
    
    # 00-..-..-..
    pass
    
    # 01-..-..-..
    pass
    
    # 02-05-..-00       IFUNC_001
    # 02-05-..-01       IFUNC_001
    # 02-05-..-02       IFUNC_001
    pass
    
    # 03-..-..-..
    pass
    
    # 04-03-..-00 IFUNC_001
    log_item1           = login_panels["login_scr_menu_pnl"].items["logname"]
    log_item1.getEntry  = MethodType(getEntry, log_item1, CurseItem)
    # 04-03-..-01 IFUNC_001
    log_item2           = login_panels["login_scr_menu_pnl"].items["logpw"]
    log_item2.getEntry  = MethodType(getEntry, log_item2, CurseItem)
    # 04-03-..-02 IFUNC_001
    log_item3           = login_panels["login_scr_menu_pnl"].items["logdb"]
    log_item3.getEntry  = MethodType(getEntry, log_item3, CurseItem)
    # 04-03-..-03 IFUNC_002
    log_item4           = login_panels["login_scr_lang_optbox"].items["OmySQL"]
    log_item4.setOption = MethodType(setOption, log_item4, CurseItem)
    log_item4b        = login_panels["login_scr_lang_optbox"].items["Opostgre"]
    log_item4b.setOption = MethodType(setOption, log_item4b, CurseItem)
    # 04-03-..-04 IFUNC_003
    log_item5   = login_panels["login_scr_menu_pnl"].items["logsubmit"]
    log_item5.databaseLoginTest=MethodType(databaseLoginTest,log_item5,CurseItem)
    
    # 05-04-..-00T IFUNC_004
    user_item1          = user_panels["usermain_scr_m_pnl"].items["temp_db1"]
    user_item1.loadResult = MethodType(loadResult, user_item1, CurseItem)

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def load_globals(curse_container):
    pass
    #curse_container.global_storage["log_name"] = ""
    #curse_container.global_storage["log_pw"]   = ""
    #curse_container.global_storage["log_db"]   = ""  
    #curse_container.global_storage["log_lang"] = ""
    pass
