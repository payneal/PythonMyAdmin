﻿import curses

colors = None
borderSets = None
panelStyles = None

class CursePanelStyle(object):
    """ The CursePanelStyle class is used to store sets of predefined display
    style variables for the CursePanel class. CursePanels refer to the global
    collection curseStyle.styles to access a CursePanelStyle object that 
    defines a particular style. "Style" means traits such as text color, window
    border appeareance, background color, etc... The CursePanelStyle class also 
    stores the style modification when the state of the referring object is
    changed (e.g. an item is selected/deselected)""" 
    def __init__(self, kwargs):
        self.bg_chr     = kwargs["bg_chr"]
        self.bg_atr     = kwargs["bg_atr"]
        self.bg_clr     = kwargs["bg_clr"]
        self.bg_chtype  = kwargs["bg_chr"]|kwargs["bg_atr"]|kwargs["bg_clr"]

        self.br_chrs    = list(kwargs["br_chrs"])
        self.br_atr     = kwargs["br_atr"]
        self.br_clr     = kwargs["br_clr"]

        self.ttl_atr    = kwargs["ttl_atr"]
        self.ttl_clr    = kwargs["ttl_clr"]

        self.txt_atr    = kwargs["txt_atr"]
        self.txt_clr    = kwargs["txt_clr"] 

        self.fbg_chr    = kwargs["fbg_chr"]
        self.fbg_atr    = kwargs["fbg_atr"]
        self.fbg_clr    = kwargs["fbg_clr"]
        self.fbg_chtype = kwargs["fbg_chr"]|kwargs["fbg_atr"]|kwargs["fbg_clr"]

        self.fbr_chrs   = list(kwargs["fbr_chrs"])
        self.fbr_atr    = kwargs["fbr_atr"]
        self.fbr_clr    = kwargs["fbr_clr"]

        self.fttl_atr   = kwargs["fttl_atr"]
        self.fttl_clr   = kwargs["fttl_clr"]

def init_color_pairs():
    global colors
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)  # black / black
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)   # blue  / black
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # cyan  / black
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)  # green / black
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)# mgnta / black
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)    # red   / black
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK) # yllw  / black

    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLUE)   # blue  / black
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_CYAN)   # cyan  / black
    curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_GREEN)  # green / black
    curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_MAGENTA)# mgnta / black
    curses.init_pair(12, curses.COLOR_BLACK, curses.COLOR_RED)    # red   / black
    curses.init_pair(13, curses.COLOR_BLACK, curses.COLOR_YELLOW) # yllw  / black
    curses.init_pair(14, curses.COLOR_WHITE, curses.COLOR_BLACK) # yllw  / black

    colors = {  "DFT": curses.color_pair(0),
                "BLK": curses.color_pair(1),   "BLU": curses.color_pair(2),
                "CYN": curses.color_pair(3),   "GRN": curses.color_pair(4),
                "MGA": curses.color_pair(5),   "RED": curses.color_pair(6),
                "YLW": curses.color_pair(7),   "WHT": curses.color_pair(14),
                                               "RBLU": curses.color_pair(8), 
                "RCYN": curses.color_pair(9),  "RGRN": curses.color_pair(10), 
                "RMGA": curses.color_pair(11), "RRED": curses.color_pair(12),
                "RYLW": curses.color_pair(13)}

def init_style():
    global borderSets
    #global locCode
    global colors
    global panelStyles
    
    # attrset->border?
    # attron->border?
    #x = ord("x".encode(locCode))
    #hsh = ord("#".encode(locCode))
    #dsh = ord("-".encode(locCode))
    #vln = ord("|".encode(locCode))
    #sp = ord(" ".encode(locCode))
    #pls = ord("+".encode(locCode))

    x = ord("x")
    hsh = ord("#")
    dsh = ord("-")
    vln = ord("|")
    sp = ord(" ")
    pls = ord("+")
   
    borderSets = {
        "all_hash" : [ hsh for i in range (0, 8) ],
        "all_space" : [ sp for i in range (0, 8) ],
        "all_x" : [ x for i in range (0, 8) ],
        "side_hash_top_dash" : [ hsh, hsh, dsh, dsh, hsh, hsh, hsh, hsh ],
        "w_s_hash_n_dash_e_vline" : [ hsh, vln, dsh, hsh, hsh, dsh, hsh, vln],
        "w_e_vline_nw_ne_sw_se_pls_n_s_dsh": [vln,vln,dsh,dsh,pls,pls,pls,pls],
        "no_border" : [-1]}

    panelStyles = {}
    panelStyles["default"] = CursePanelStyle({
        "bg_chr" : sp,
        "bg_atr" : 0,
        "bg_clr" : colors["WHT"],

        "br_chrs": [0],
        "br_atr" : 0,
        "br_clr" : colors["WHT"],

        "ttl_atr" : 0,
        "ttl_clr" : colors["WHT"],

        "txt_atr" : 0,
        "txt_clr" : colors["WHT"],

        "fbg_chr" : sp,
        "fbg_atr" : 0,
        "fbg_clr" : colors["WHT"],

        "fbr_chrs": [0],
        "fbr_atr" : 0,
        "fbr_clr" : colors["BLU"],

        "fttl_atr" : 0,
        "fttl_clr" : colors["WHT"]
    })

    panelStyles["style1"] = CursePanelStyle({
        "bg_chr" : sp,
        "bg_atr" : 0,
        "bg_clr" : colors["BLU"],

        "br_chrs": list(borderSets["side_hash_top_dash"]),
        "br_atr" : 0,
        "br_clr" : colors["BLU"],

        "ttl_atr" : 0,
        "ttl_clr" : colors["WHT"],

        "txt_atr" : 0,
        "txt_clr" : colors["WHT"],

        "fbg_chr" : sp,
        "fbg_atr" : 0,
        "fbg_clr" : colors["CYN"],

        "fbr_chrs": list(borderSets["side_hash_top_dash"]),
        "fbr_atr" : curses.A_BOLD,
        "fbr_clr" : colors["CYN"],

        "fttl_atr" : curses.A_BOLD,
        "fttl_clr" : colors["YLW"]
    })

    panelStyles["style2"] = CursePanelStyle({
        "bg_chr" : sp,
        "bg_atr" : 0,
        "bg_clr" : colors["BLU"],

        "br_chrs": list(borderSets["w_e_vline_nw_ne_sw_se_pls_n_s_dsh"]),
        "br_atr" : curses.A_BOLD,
        "br_clr" : colors["BLU"],

        "ttl_atr" : 0,
        "ttl_clr" : colors["WHT"],

        "txt_atr" : 0,
        "txt_clr" : colors["BLU"],

        "fbg_chr" : sp,
        "fbg_atr" : 0,
        "fbg_clr" : colors["CYN"],

        "fbr_chrs": list(borderSets["w_e_vline_nw_ne_sw_se_pls_n_s_dsh"]),
        "fbr_atr" : curses.A_BOLD,
        "fbr_clr" : colors["CYN"],

        "fttl_atr" : curses.A_BOLD,
        "fttl_clr" : colors["YLW"]
    })

    panelStyles["usr_strip"] = CursePanelStyle({
        "bg_chr" : sp,
        "bg_atr" : 0,
        "bg_clr" : colors["RGRN"],

        "br_chrs": list(borderSets["no_border"]),
        "br_atr" : 0,
        "br_clr" : colors["BLK"],

        "ttl_atr" : 0,
        "ttl_clr" : colors["RGRN"],

        "txt_atr" : 0,
        "txt_clr" : colors["WHT"],

        "fbg_chr" : sp,
        "fbg_atr" : 0,
        "fbg_clr" : colors["RGRN"],

        "fbr_chrs": list(borderSets["no_border"]),
        "fbr_atr" : 0,
        "fbr_clr" : colors["BLK"],

        "fttl_atr" : 0,
        "fttl_clr" : colors["RGRN"]
    })

    panelStyles["infobox2"] = CursePanelStyle({
        "bg_chr" : sp,
        "bg_atr" : 0,
        "bg_clr" : colors["RBLU"],

        "br_chrs": list(borderSets["no_border"]),
        "br_atr" : 0,
        "br_clr" : colors["BLK"],

        "ttl_atr" : curses.A_BOLD,
        "ttl_clr" : colors["CYN"],

        "txt_atr" : 0,
        "txt_clr" : colors["WHT"],

        "fbg_chr" : sp,
        "fbg_atr" : 0,
        "fbg_clr" : colors["RBLU"],

        "fbr_chrs": list(borderSets["no_border"]),
        "fbr_atr" : 0,
        "fbr_clr" : colors["BLK"],

        "fttl_atr" : curses.A_BOLD,
        "fttl_clr" : colors["CYN"]
    })

class CurseItemStyle(object):
    def __init__(self, kwargs):
        pass