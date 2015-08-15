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

#import psycopg2 
import json
import decimal
#import cursesPostgresTemp
#import curseMysqlTemp

import MySQLdb
import MySQLdb.cursors

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
#---------------|title_scr_footer--------|-|--------------00-02-..-..
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
    viewDB_msg_map      = curse_container.act_msg_maps["viewDB_screen"]
    viewTbl_msg_map      = curse_container.act_msg_maps["viewTbl_screen"]
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
    "ftr_strip"         : "title_scr_footer"})
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
    "ftr_strip"         : "about_scr_footer"})
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
    "ftr_strip"         : "login_scr_footer"})
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
    "act_msg_map"       : viewDB_msg_map,
    "default_focus_key" : "viewDB_scr_out_pnl",
    "can_panel_change"  : False,
    "style"             : curseStyles["dashscrbg"],
    "ftr_strip"         : "viewDB_scr_footer",
    "_load_once"        : True,
    "_on_load"          : dict(  
        action       = "call_function", 
        action_name  = "runQueryOnLoad", 
        action_args  = 
        [                     
            (
                { # argument strings for makeQuery
                    "sel_xp"  :
                        "a.table_name,a.table_rows,a.create_time,"\
                        "a.update_time,a.engine",
                    "tbl_refs":  
                        "information_schema.tables AS a",
                    "w_cond"  : 
                        "a.table_schema = '!'",
                    "limit"   : "400"
                },
                { # variables that need to be fetched from global storage at rt
                    "w_cond": ["log_db"]
                },
                # panel we'll output the query
                "viewDB_scr_out_pnl",
                # the order in which we want the returned columns
                [
                    "table_name","table_rows","create_time",
                    "update_time","engine"
                ]
            )
        ])})
        
    curseScreens["viewTbl_screen"]= CurseScreen(**{
    "global_storage"    : global_storage,
    "screens"           : curseScreens,
    "user_strip"        : "viewTbl_scr_ustrip",
    "key_action_map"    : key_action_map,
    "act_msg_map"       : viewTbl_msg_map,
    "default_focus_key" : "viewTbl_tbl_pnl",
    "can_panel_change"  : True,
    "style"             : curseStyles["dashscrbg"],
    "ftr_strip"         : "viewTbl_scr_footer",
    "_load_once"        : True,
    "_on_load"          : dict(  
        action       = "call_function", 
        action_name  = "runQueryOnLoad", 
        action_args  = 
        [        
            (
                #0
                {
                    "sel_xp"  :
                        "a.column_name,a.ordinal_position,a.data_type,"\
                        "a.column_default,a.is_nullable,"\
                        "a.character_maximum_length,"\
                        "a.column_type,a.column_key,a.privileges",
                    "tbl_refs":  
                        "information_schema.columns AS a",
                    "w_cond"  : 
                        "a.table_name = '!' AND a.table_schema = '!' ",
                    "limit"   : "400"
                },
                #1
                { # variables that need to be fetched from global storage at rt
                    "w_cond": ["view_tbl", "log_db"]
                },
                #2
                "viewTbl_meta_pnl",
                #3
                [
                    "column_name","ordinal_position","data_type",
                    "column_default","is_nullable",
                    "character_maximum_length","column_type", 
                    "column_key", "privileges"
                ]
            ),
            (
                #0
                {
                    "sel_xp"  : " * ",
                    "tbl_refs": " ! ",
                    "limit"   : "400"
                },
                #1
                { # variables that need to be fetched from global storage at rt
                    "tbl_refs" : ["view_tbl"]
                },
                #2
                "viewTbl_tbl_pnl",
            )      
        ])})
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
    viewTbl_screen  = curseScreens["viewTbl_screen"] 
    mngDBS_screen   = curseScreens["manageDB_screen"]  
    cfgAcct_screen  = curseScreens["cfg_acct_screen"]    

    panel_msg_map = curse_container.act_msg_maps["panel_msg_map2"]
    list_msg_map = curse_container.act_msg_maps["list_msg_map"]
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
    title_screen.panels["title_scr_footer"]                 = CursePanel(**{
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
        "title_scr_footer"]
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
        "Press Z to return to Title Screen, if you dare...".center(80), 0, 0)})
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
    "style"         : curseStyles["infobox2"]})
                                
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
    "_default_focus_item_key" : "db_tables"})
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
    user_screen.panels["user_scr_footer"]                  = CursePanel(**{
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

    viewDB_screen.panels["viewDB_scr_u_info"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : viewDB_screen,    
    "size"          : (1, 0, 6, 80),
    "style"         : curseStyles["infobox1"]})

    # 06-02-..-..
    viewDB_screen.panels["viewDB_scr_menu_pnl"]            = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : viewDB_screen,
    #"title"         : ("VIEW DATABASE".center(18), 2, 1),
    "act_msg_map"   : panel_msg_map,
    "size"          : (8, 0, 1, 80 ),
    "style"         : curseStyles["key_menu"]})

    viewDB_screen.panels["viewDB_scr_out_pnl"]             = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : viewDB_screen,
    #"title"         : (-1, -1, ""),
    "act_msg_map"   : list_msg_map,
    "size"          : (10, 0, 11, 80 ),
    "style"         : curseStyles["usermain_listbox"],   
    "focusable"     : True,
    "is_pad"        : True,
    "psize"         : (500, 500)})

    viewDB_screen.panels["viewDB_scr_footer"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : viewDB_screen,
    "size"          : (23, 0, 1, 80),
    "style"         : curseStyles["infobox2"]})

    # panels are updated/ drawn in the order below- this affects
    # overlapping panels so pay attention to this!
    viewDB_screen.panel_indexes = [
        "viewDB_scr_bg",    
        "viewDB_scr_ustrip",
        "viewDB_scr_menu_pnl",
        "viewDB_scr_u_info",
        "viewDB_scr_out_pnl",
        "viewDB_scr_footer"]
    viewDB_screen.panel_count = len(viewDB_screen.panel_indexes)

    # 06-00-..-..      y, x, h, w
    viewTbl_screen.panels["viewTbl_scr_bg"]                 = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : viewTbl_screen,
    "size"          : (0, 0, 24, 80),
    "style"         : curseStyles["title_panel"]})
    # 06-01-..-.. 
    viewTbl_screen.panels["viewTbl_scr_ustrip"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : viewTbl_screen,
    "size"          : (0, 0, 1, 80),
    "style"         : curseStyles["user_strip"]})
    viewTbl_screen.panels["viewTbl_meta_pnl"]                = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : viewTbl_screen,
    "act_msg_map"   : list_msg_map,
    "size"          : (1, 0, 8, 80 ),
    "style"         : curseStyles["usermain_listbox"],   
    "focusable"     : True,
    "is_pad"        : True,
    "psize"         : (500, 500)})
    # 06-02-..-..
    viewTbl_screen.panels["viewTbl_scr_menu_pnl"]            = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : viewTbl_screen,
    #"title"         : ("VIEW DATABASE".center(18), 2, 1),
    "act_msg_map"   : panel_msg_map,
    "size"          : (10, 0, 1, 80 ),
    "style"         : curseStyles["key_menu"]})
    viewTbl_screen.panels["viewTbl_tbl_pnl"]                = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : viewTbl_screen,
    "act_msg_map"   : list_msg_map,
    "size"          : (11, 0, 11, 80 ),
    "style"         : curseStyles["usermain_listbox"],   
    "focusable"     : True,
    "is_pad"        : True,
    "psize"         : (500, 500)})
    viewTbl_screen.panels["viewTbl_scr_footer"]              = CursePanel(**{
    "global_storage": global_storage,
    "parent"        : viewTbl_screen,
    "size"          : (23, 0, 1, 80),
    "style"         : curseStyles["infobox2"]})
    viewTbl_screen.panel_indexes = [
        "viewTbl_scr_bg",    
        "viewTbl_scr_ustrip",
        "viewTbl_meta_pnl",
        "viewTbl_tbl_pnl",
        "viewTbl_scr_menu_pnl",
        "viewTbl_scr_footer"]
    viewTbl_screen.panel_count = len(viewTbl_screen.panel_indexes)

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
    viewDB_scr_panels   = curseScreens["viewDB_screen"].panels

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
    "label"         : "(X) create account".center(20),
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
    title_panels["title_scr_panel"].items["db_main"] = CurseItem(**{ 
    "container"     : curse_container,
    "global_storage": global_storage,
    "parent"        : title_panels["title_scr_panel"],
    "parent_screen" : curseScreens["title_screen"],
    "size"          : (17, 30, 1, 20), # y, x, h, w
    "style"         : curseStyles["title_menu"],
    "label"         : "(X) database portal".center(20),
    "active"        : False,
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
        "db_main", 
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
        recv_act    = "dbLoginToViewDB",
        recv_args   = ["viewDB_screen", "login_scr_infobox",
                       "redirecting to database management screen"],
        ret_info    = None,
        replace_msg = True)})
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
    "info"          : "login database uses mySQL- "\
                      " press SPACE to make selection",
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
    "info"          : "(          INACTIVE          ) "\
                      "login database uses postgresql- "\
                      " press SPACE to make selection",
    "infotar"       : "login_scr_infobox"})
    #"_on_select"    : dict(  msg_status  = "unread", 
    #    send_layer  = "item",
    #    recv_layer  = "self", 
    #    recv_name   = "self",   
    #    on_recv     = "call_function", 
    #    recv_act    = "setOption",
    #    recv_args   = [
    #                    login_scr_panels["login_scr_lang_optbox"],
    #                    global_storage, 
    #                    "log_lang",
    #                    True ],
        #recv_act    = "getOption",
        #recv_args   = ["login_scr_lang_optbox", global_storage, "log_lang"],
    #    ret_info    = None)    })
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
    user_scr_panels["user_scr_menu_pnl"].items["db_tables"]=CurseItem(**{
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
    user_scr_panels["user_scr_menu_pnl"].items["db_meta"]= CurseItem(**{
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
    user_scr_panels["user_scr_menu_pnl"].items["raw_query"]=CurseItem(**{
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
        "db_tables", 
        "db_meta",
        "raw_query",
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

    h_attr = colors["MGAYLW"] | curses.A_BOLD
    viewDB_scr_panels["viewDB_scr_menu_pnl"].items["view_tbl"]= CurseItem(**{
    "container" : curse_container,
    "global_storage": global_storage,
    "parent"        : viewDB_scr_panels["viewDB_scr_menu_pnl"],
    "parent_screen" : curseScreens["viewDB_screen"],
    "size"          : (0,5, 1, 10), # y, x, h, w
    "style"         : viewDB_scr_panels["viewDB_scr_menu_pnl"].style,
    "label"         : "view table",
    "hotkey"       : {"h_key": ord("T"), "labl_index": 5, "attr":h_attr},
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "self", 
        recv_name   = "self",   
        on_recv     = "call_function", 
        recv_act    = "viewDbToViewTbl",
        recv_args   = ["viewDB_scr_out_pnl"],
        ret_info    = None,
        replace_msg = True)})

    viewDB_scr_panels["viewDB_scr_menu_pnl"].items["drop_tbl"]= CurseItem(**{
    "container" : curse_container,
    "global_storage": global_storage,
    "parent"        : viewDB_scr_panels["viewDB_scr_menu_pnl"],
    "parent_screen" : curseScreens["viewDB_screen"],
    "size"          : (0, 23, 1, 10), # y, x, h, w
    "style"         : viewDB_scr_panels["viewDB_scr_menu_pnl"].style,
    "label"         : "(X) drop table",
    "hotkey"       : {"h_key": ord("D"), "labl_index":0 , "attr":h_attr},
    "active"        : False,
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "main", 
        recv_name   = "main",   
        on_recv     = "call_function", 
        recv_act    = "changeScreen",
        recv_args   = ["manageDB_screen"],
        ret_info    = None)})

    viewDB_scr_panels["viewDB_scr_menu_pnl"].items["new_tbl"]= CurseItem(**{
    "container" : curse_container,
    "global_storage": global_storage,
    "parent"        : viewDB_scr_panels["viewDB_scr_menu_pnl"],
    "parent_screen" : curseScreens["viewDB_screen"],
    "size"          : (0, 43, 1, 10), # y, x, h, w
    "style"         : viewDB_scr_panels["viewDB_scr_menu_pnl"].style,
    "label"         : "(X) add table",
    "hotkey"       : {"h_key": ord("A"), "labl_index": 0, "attr":h_attr},
    "active"        : False,
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "main", 
        recv_name   = "main",   
        on_recv     = "call_function", 
        recv_act    = "changeScreen",
        recv_args   = ["manageDB_screen"],
        ret_info    = None)})

    viewDB_scr_panels["viewDB_scr_menu_pnl"].items["r_qry"]= CurseItem(**{
    "container" : curse_container,
    "global_storage": global_storage,
    "parent"        : viewDB_scr_panels["viewDB_scr_menu_pnl"],
    "parent_screen" : curseScreens["viewDB_screen"],
    "size"          : (0, 61, 1, 10), # y, x, h, w
    "style"         : viewDB_scr_panels["viewDB_scr_menu_pnl"].style,
    "label"         : "(X) raw query",
    "hotkey"       : {"h_key": ord("Y"), "labl_index": 8, "attr":h_attr},
    "active"        : False,
    "_on_select"    : dict(  msg_status  = "unread", 
        send_layer  = "item", 
        recv_layer  = "main", 
        recv_name   = "main",   
        on_recv     = "call_function", 
        recv_act    = "changeScreen",
        recv_args   = ["manageDB_screen"],
        ret_info    = None)})

    viewDB_scr_panels["viewDB_scr_menu_pnl"].item_indexes = [
        "view_tbl",
        "drop_tbl",
        "new_tbl",
        "r_qry"]
    viewDB_scr_panels["viewDB_scr_menu_pnl"].item_count = len(
        viewDB_scr_panels["viewDB_scr_menu_pnl"].item_indexes)

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def init_textboxes(curse_container):

    title_panels      = curse_container.screens["title_screen"].panels
    test_panels       = curse_container.screens["test_screen"].panels
    account_panels    = curse_container.screens["account_screen"].panels
    about_panels      = curse_container.screens["about_screen"].panels
    login_panels      = curse_container.screens["login_screen"].panels
    usermain_panels   = curse_container.screens["usermain_screen"].panels
    viewDB_panels     = curse_container.screens["viewDB_screen"].panels
    viewTbl_panels    = curse_container.screens["viewTbl_screen"].panels
    curse_styles      = curse_container.styles
    
    # 00-01-00-..          y, x, h, w  
    title_panels["title_scr_panel"].textbox          = CurseTextbox(**dict(
    parent      = title_panels["title_scr_panel"],
    base_text    = asciiart.titlestr5,
    size        = (3, 9, 10, 63), 
    style       = curse_styles["title_panel"]))
    # 00-02-00-..
    title_panels["title_scr_footer"].textbox      = CurseTextbox(**dict(
            parent      = title_panels["title_scr_footer"],
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

    # 05-02-00-..          y, x, h, w 
    viewDB_panels["viewDB_scr_u_info"].textbox   = CurseTextbox(**dict(
        parent      = viewDB_panels["viewDB_scr_u_info"],
        base_text   = "Welcome your database METADATA page!"\
                      "Press a highlighted key from the option menu links to "\
                      " jump to a subpage- the currently selected table from "\
                      "below will be used as the subject, where relevant. ",
        size        = (1, 2, 4, 77),  
        style       = curse_styles["infobox1"]))

    viewDB_panels["viewDB_scr_footer"].textbox      = CurseTextbox(**dict(
        parent      = viewDB_panels["viewDB_scr_footer"],
        base_text    = "Use arrow keys to scroll table , "\
                        "Press 'v' to return to title screen",
        size        =  (0, 6, 1, 74),
        style       = curse_styles["infobox2"]))

    viewTbl_panels["viewTbl_scr_menu_pnl"].textbox      = CurseTextbox(**dict(
        parent      = viewTbl_panels["viewTbl_scr_menu_pnl"],
        base_text   =  "Above: table metadata (no nav atm)     "\
                        "Below: Up to first 400 rows of table",
        size        =  (0, 1, 1, 78),
        style       = curse_styles["infobox2"]))

    viewTbl_panels["viewTbl_scr_footer"].textbox      = CurseTextbox(**dict(
        parent      = viewTbl_panels["viewTbl_scr_footer"],
        base_text    = "Use arrow keys to scroll table , "\
                        "Press 'v' to return to main database screen",
        size        =  (0, 1, 1, 78),
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
                "quit"      : dict(  msg_status  = "unread", 
                    send_layer  = "screen", 
                    recv_layer  = "main", 
                    recv_name   = "main",   
                    on_recv     = "call_function", 
                    recv_act    = "quitCurses",
                    recv_args   = None,
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
                    recv_args   = ["title_screen"],
                    ret_info    = None)},
        "viewDB_screen" : {
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
                    recv_args   = ["title_screen"],
                    ret_info    = None),
                "HOTKEY_t"  :  dict(  msg_status  = "unread", 
                    send_layer  = "screen", 
                    recv_layer  = "self", 
                    recv_name   = "self",   
                    on_recv     = "call_function", 
                    recv_act    = "directItemSelect", 
                    recv_args   = ["view_tbl"],
                    ret_info    = None,
                    replace_msg = True)},
        "viewTbl_screen" : {
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
                    recv_args   = ["viewDB_screen"],
                    ret_info    = None)},
                #"forward"   : dict(  msg_status  = "unread", 
                #    send_layer  = "screen", 
                #    recv_layer  = "self", 
                #    recv_name   = "self",   
                #    on_recv     = "call_function",  
                #    recv_act    = "nextPanel",
                #    recv_args   = None,
                #    ret_info    = None)},
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
                "left"      : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "self", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "prevItem",
                    recv_args   = None,
                    ret_info    = None),
                "right"     : dict(  msg_status  = "unread", 
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
                "left"      : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "panel", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "scrollLeft",
                    recv_args   = None,
                    ret_info    = None),
                "right"     : dict(  msg_status  = "unread", 
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
                    ret_info    = None)},
        "query_list_msg_map"  : {
                "left"      : dict(  msg_status  = "unread", 
                    send_layer  = "panel", 
                    recv_layer  = "panel", 
                    recv_name   = "self",   
                    on_recv     = "call_function",  
                    recv_act    = "scrollLeft",
                    recv_args   = None,
                    ret_info    = None),
                "right"     : dict(  msg_status  = "unread", 
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
                    ret_info    = None)}}

    return act_msg_maps

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def init_funcs(curse_container):
    curseStyles         = curse_container.styles #["styles"]
    colors              = curseStyles["COLORS"]


    
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

#/\/ LOGIN SCREEN DATABASE LOGIN FUNCS /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

    def dbLoginToViewDB(self, redirect_skey, infobox_pkey, redirect_str):
        infobox = self.container.getTextboxByName(infobox_pkey)
        result = dbLoginConnect(self.global_storage, infobox)
        if result["status"] != "OK":    return None
        else: 
            self.global_storage["db_cxn"] = result['cxn']
            return { 
            "msg_status"  : "unread", 
            "send_layer"  : "item", 
            "recv_layer"  : "main", 
            "recv_name"   : "main",   
            "on_recv"     : "call_function", 
            "recv_act"    : "changeScreen", 
            "recv_args"   : [redirect_skey, 3000, infobox_pkey, redirect_str]}
    
    # gets login arguments from global storage
    def dbLoginConnect(gl_stor, infobox):
        if "log_lang" in gl_stor:
            lang = gl_stor["log_lang"] # get qlang
            if lang == "mySQL" or lang == "postgresql":
                # get login arguments from global storage
                l_args = dict(
                        database = gl_stor["log_db"],
                        user     = gl_stor["log_name"],
                        host     = 'localhost',
                        password = gl_stor["log_pw"])
                     
                # execute DB interface functions
                if lang=="mySQL": c_status = login(l_args)
                else: c_status={"status":"ERR",  "er_info":"postgresql disabled"}                  
            else: c_status = { "status": "ERR", "er_info": "bad language value" }
        else: c_status = { "status": "ERR", "er_info": "language field not set" }

        # draw results
        if "er_info" in c_status: 
            infobox.refresh(c_status["er_info"][1])
            #infobox.refresh(json.dumps(c_status["er_info"]))
        return c_status

    # establishes actual connection and returns status, connection tuple
    def login(login_dict):
        con = None
        try:
            con = MySQLdb.connect(
                user   = login_dict["user"],
                passwd = login_dict["password"],
                host   = login_dict["host"],
                db     = login_dict["database"],
                cursorclass=MySQLdb.cursors.DictCursor)
            status = {"status":"OK", "cxn":con}
        except MySQLdb.Error as err:
            if con!= None:      con.rollback()
            status = {"status": "ERR", "er_info": err}
        return status

#/\/ VIEWDB SCREEN LOAD FUNC \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/

    def viewDbToViewTbl(self, q_list_pkey):
        panel = self.parent_screen.panels[q_list_pkey]
        tbl_name = panel._q_dict[panel.cur_index - 1]['table_name']
        self.global_storage["view_tbl"] = copy.copy(tbl_name)
        return { 
        "msg_status"  : "unread", 
        "send_layer"  : "item", 
        "recv_layer"  : "main", 
        "recv_name"   : "main",   
        "on_recv"     : "call_function", 
        "recv_act"    : "changeScreen", 
        "recv_args"   : ["viewTbl_screen"]}

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\\/\/\/\/\/\/\/\/\/\/\/\/

    def runQueryOnLoad(self, q_arg_set):
        set_count = len(q_arg_set)
        for qs in range(0, set_count):
            arg_count = len(q_arg_set[qs])
            q_args                        = q_arg_set[qs][0]
            q_val_keys                    = q_arg_set[qs][1]
            load_pkey                     = q_arg_set[qs][2]
            col_order                     = None
            open_nest                     = False
            if arg_count > 3: col_order     = q_arg_set[qs][3]
            if arg_count > 4: open_nest     = q_arg_set[qs][4]
            
            # get connection and output panel
            con = self.global_storage['db_cxn']
            load_panel = self.panels[load_pkey]

            # get variables for q_str
            q_args = getQueryArgVals(self.global_storage, q_args, q_val_keys)
        
            # make query string
            q_str = makeQuery(q_args)

            # send query to DB
            q_res = queryDatabase(con, q_str)

            # check query result
            if q_res["status"]=="ERR":   
                load_panel.setInnerText( 1 ,1, q_res["data"] )
                load_panel.refresh()
                q_res_list=[]
            else:       q_res_list = dictResToListRes(q_res["data"], col_order)

            #qry_data = runQueryOnLoad(con, q_args, load_panel, col_ordr)
            if len(q_res_list) > 0:
                loadListResult(q_res_list, self, load_panel, load_pkey, 
                    q_res["data"], open_nest)

    def dictToList(dictionary, key_order):
        d_list = []      
        key_len = len(key_order)
        for i in range(0, key_len):
            d_list.append( copy.deepcopy( str( dictionary[key_order[i]] )))
        return d_list

    def dictResToListRes(dict_result, key_order=None):
        l_list = []
        if key_order == None:                 key_order =list(dict_result[0].keys())
        l_list.append(list(key_order)) 

        for row in dict_result:   l_list.append(dictToList(row, key_order))
        return l_list

    def loadListResult(result_list,out_screen, out_panel, out_panel_key,
            result_dict, focus_nested_panel=False):

        if not hasattr(out_panel, "_inner_list"):
            setattr(out_panel,"_inner_list", list(result_list))
        else:         
            out_panel._inner_list = []
            out_panel._inner_list = list(result_list)

        if not hasattr(out_panel, "_q_dict"):
            setattr(out_panel,"_q_dict", copy.deepcopy(result_dict))
        else:         
            out_panel._q_dict = {}
            out_panel._q_dict = copy.deepcopy(result_dict)

        out_panel.loadList()

        if focus_nested_panel == True:
            out_panel.parent_screen.openNestedPanel(out_panel_key)


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

    def getQueryArgVals(globals, q_args, q_val_keys):
        """ 
        replaces all ! from query argument strings in q_args with values
        from global storage using keys in q_val_keys 
        """
        for q_vkey in q_val_keys:      
            q_arg    = q_args[q_vkey]      # single argument string with 1+ @
            q_vals   = q_val_keys[q_vkey]  # list of values to get for args
            num_vals = len(q_vals)
            for v in range(0, num_vals):
                #q_args[q_vkey] = q_arg.replace("!", globals[q_vals[v]], 1)
                q_arg = q_arg.replace("!", globals[q_vals[v]], 1)
            q_args[q_vkey] = q_arg
        return q_args

    def makeQuery(q_args):
        q_str       =   "SELECT "    + q_args["sel_xp"]
        if "tbl_refs"   in q_args:
            q_str   += (" FROM "     + q_args["tbl_refs"])
        if "w_cond"     in q_args:
            q_str   += (" WHERE "    + q_args["w_cond"])           
        if "w_grp"      in q_args:
            q_str   += (" GROUP BY " + q_args["w_grp"])
        if "h_cond"     in q_args:
            q_str   += (" HAVING "   + q_args["h_cond"])  
        if "order"      in q_args:
            q_str   += (" ORDER BY " + q_args["order"])
        if "limit"      in q_args:
            q_str   += (" LIMIT "    + q_args["limit"])
        return q_str
         
    def queryDatabase(connection, query):
        q_result = {}
        curs = connection.cursor()
        try:
            curs.execute(query)
            q_result["data"]   = curs.fetchall()
            q_result["status"] = "OK"
        except MySQLdb.Error as err:
            connection.rollback()
            q_result["data"]   = err
            q_result["status"] = "ERR"
        curs.close()
        return q_result


    #------------------ FUNCTION ASSIGNMENT -----------------------------------
    curseScreens        = curse_container.screens #["screens"]

    vdb_screen         = curseScreens["viewDB_screen"]
    vtbl_screen        = curseScreens["viewTbl_screen"]

    title_panels       = curseScreens["title_screen"].panels
    test_panels        = curseScreens["test_screen"].panels
    account_panels     = curseScreens["account_screen"].panels
    about_scr_panels   = curseScreens["about_screen"].panels
    login_panels       = curseScreens["login_screen"].panels
    user_panels        = curseScreens["usermain_screen"].panels    
    vdb_panels         = curseScreens["viewDB_screen"].panels    


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
    log_item5.dbLoginToViewDB=  MethodType(dbLoginToViewDB,log_item5,CurseItem)
    #log_item5.dbLoginConnect=MethodType(dbLoginConnect,log_item5,CurseItem)
    

    vdb_screen.runQueryOnLoad=MethodType(runQueryOnLoad, vdb_screen, CurseScreen)

    vdb_item1  = vdb_panels["viewDB_scr_menu_pnl"].items["view_tbl"]
    vdb_item1.viewDbToViewTbl=  MethodType(viewDbToViewTbl,vdb_item1,CurseItem)


    vtbl_screen.runQueryOnLoad=MethodType(runQueryOnLoad, vtbl_screen, CurseScreen)
    
    # 05-04-..-00T IFUNC_004
    user_item1          = user_panels["usermain_scr_m_pnl"].items["temp_db1"]
    user_item1.loadListResult = MethodType(loadListResult, user_item1, CurseItem)

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

def load_globals(curse_container):
    pass
    #curse_container.global_storage["log_name"] = "JerryBoney"
    #curse_container.global_storage["log_pw"]   = "alaspooryorrick"
    #curse_container.global_storage["log_db"]   = "world"  
    #curse_container.global_storage["log_lang"] = "mySQL"
