import curses

colors = None
borderSets = None
panelStyles = None

class CursePanelStyle(object):
    """
    The CursePanelStyle class is used to store sets of predefined display
    style variables for the CursePanel class. CursePanels refer to the global
    collection curseStyle.styles to access a CursePanelStyle object that 
    defines a particular style. "Style" means traits such as text color, window
    border appeareance, background color, etc... The CursePanelStyle class also 
    stores the style modification when the state of the referring object is
    changed (e.g. an item is selected/deselected)
    """ 
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
        self.txt_bg_clr    = kwargs["txt_clr"]

        self.fbg_chr    = kwargs["fbg_chr"]
        self.fbg_atr    = kwargs["fbg_atr"]
        self.fbg_clr    = kwargs["fbg_clr"]
        self.fbg_chtype = kwargs["fbg_chr"]|kwargs["fbg_atr"]|kwargs["fbg_clr"]

        self.fbr_chrs   = list(kwargs["fbr_chrs"])
        self.fbr_atr    = kwargs["fbr_atr"]
        self.fbr_clr    = kwargs["fbr_clr"]

        self.fttl_atr   = kwargs["fttl_atr"]
        self.fttl_clr   = kwargs["fttl_clr"]

        self.ftxt_atr    = kwargs["ftxt_atr"]
        self.ftxt_clr    = kwargs["ftxt_clr"] 
        self.ftxt_bg_clr    = kwargs["ftxt_clr"]

def init_color_pairs():
    global colors                                                 #  FG  /  BG
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)   # black/black
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)    # blue /black
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)    # cyan /black
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)   # green/black
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # mgnta/black
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)     # red  /black
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # yllw /black

    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLUE)    # black/blue
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_CYAN)    # black/cyan
    curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_GREEN)  # black/green
    curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_MAGENTA)# black/mgnta
    curses.init_pair(12, curses.COLOR_BLACK, curses.COLOR_RED)    # black/red
    curses.init_pair(13, curses.COLOR_BLACK, curses.COLOR_YELLOW) # black/yllw

    curses.init_pair(14, curses.COLOR_WHITE, curses.COLOR_BLACK)  # white/black

    curses.init_pair(15, curses.COLOR_CYAN, curses.COLOR_BLUE)    # cyan /blue
    curses.init_pair(16, curses.COLOR_BLUE, curses.COLOR_CYAN)    # cyan /blue

    colors = {  "DFT": curses.color_pair(0),
                "BLK": curses.color_pair(1),   "BLU": curses.color_pair(2),
                "CYN": curses.color_pair(3),   "GRN": curses.color_pair(4),
                "MGA": curses.color_pair(5),   "RED": curses.color_pair(6),
                "YLW": curses.color_pair(7),   
                                               "RBLU": curses.color_pair(8), 
                "RCYN": curses.color_pair(9),  "RGRN": curses.color_pair(10), 
                "RMGA": curses.color_pair(11), "RRED": curses.color_pair(12),
                "RYLW": curses.color_pair(13),
                                               "WHT": curses.color_pair(14),
                "CYNBLU": curses.color_pair(15),
                "RCYNBLU": curses.color_pair(16)}

def init_style():
    global borderSets
    global colors
    global panel_styles   

    x = ord("x")
    hsh = ord("#")
    dsh = ord("-")
    vln = ord("|")
    sp = ord(" ")
    pls = ord("+")
    cln = ord(":")
    dot = ord(".")
    at = ord("@")
    NWcrner = u"\u250C"
    SWcrner = u"\u2514"
    SEcrner = u"\u2518"
    NEcrner = u"\u2510"
    vuline = u"\u2502"
    huline = u"\u2500"

   
    borderSets = {
        "all_hash" : [ hsh for i in range (0, 8) ],
        "all_space" : [ sp for i in range (0, 8) ],
        "all_x" : [ x for i in range (0, 8) ],
        "side_hash_top_dash" : [ hsh, hsh, dsh, dsh, hsh, hsh, hsh, hsh ],
        "w_s_hash_n_dash_e_vline" : [ hsh, vln, dsh, hsh, hsh, dsh, hsh, vln],
        "w_e_vline_nw_ne_sw_se_pls_n_s_dsh": [vln,vln,dsh,dsh,pls,pls,pls,pls],
        "unicode_box": [vuline, vuline, huline, huline, 
                        NWcrner, NEcrner, SWcrner, SEcrner],
        "no_border" : [-1]}

    #self.init_color_pairs()

    panel_styles = {}

    panel_styles["default"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["WHT"],

        "br_chrs"       : [0],
        "br_atr"        : 0,
        "br_clr"        : colors["WHT"],

        "ttl_atr"       : 0,
        "ttl_clr"       : colors["WHT"],
        "txt_bg_clr"    : None,

        "txt_atr"       : 0,
        "txt_clr"       : colors["WHT"],

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["WHT"],

        "fbr_chrs"      : [0],
        "fbr_atr"       : 0,
        "fbr_clr"       : colors["BLU"],

        "fttl_atr"      : 0,
        "fttl_clr"      : colors["WHT"],

        "ftxt_atr"      : None,
        "ftxt_clr"      : None,
        "ftxt_bg_clr"   : None
    })
    panel_styles["style1"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["BLU"],

        "br_chrs"       : list(borderSets["side_hash_top_dash"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLU"],

        "ttl_atr"       : 0,
        "ttl_clr"       : colors["WHT"],

        "txt_atr"       : 0,
        "txt_clr"       : colors["WHT"],
        "txt_bg_clr"    : None,

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["CYN"],

        "fbr_chrs"      : list(borderSets["side_hash_top_dash"]),
        "fbr_atr"       : curses.A_BOLD,
        "fbr_clr"       : colors["CYN"],

        "fttl_atr"      : curses.A_BOLD,
        "fttl_clr"      : colors["YLW"],

        "ftxt_atr"      : None,
        "ftxt_clr"      : None,
        "ftxt_bg_clr"   : None
    })
    panel_styles["user_strip"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["RGRN"],

        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLK"],

        "ttl_atr"       : curses.A_BOLD,#
        "ttl_clr"       : colors["RGRN"],

        "txt_atr"       : curses.A_BOLD,#
        "txt_clr"       : colors["BLU"],
        "txt_bg_clr"    : colors["BLU"],

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["RYLW"],

        "fbr_chrs"      : list(borderSets["no_border"]),
        "fbr_atr"       : 0,
        "fbr_clr"       : colors["BLK"],

        "fttl_atr"      : 0,
        "fttl_clr"      : colors["RGRN"],

        "ftxt_atr"      : None,
        "ftxt_clr"      : None,
        "ftxt_bg_clr"   : None
    })
    panel_styles["title_panel"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["CYN"],

        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLK"],

        "ttl_atr"       : 0,
        "ttl_clr"       : colors["CYN"],

        "txt_atr"       : curses.A_BOLD,
        "txt_clr"       : colors["CYN"],
        "txt_bg_clr"    : colors["CYN"],

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["GRN"],

        "fbr_chrs"      : list(borderSets["no_border"]),
        "fbr_atr"       : 0,
        "fbr_clr"       : colors["BLK"],

        "fttl_atr"      : 0,
        "fttl_clr"      : colors["GRN"],

        "ftxt_atr"      : 0,
        "ftxt_clr"      : colors["YLW"],
        "ftxt_bg_clr"   : colors["GRN"]
    })
    panel_styles["title_menu"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["CYN"],

        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLK"],

        "ttl_atr"       : 0,
        "ttl_clr"       : colors["CYN"],

        "txt_atr"       : curses.A_BOLD,
        "txt_clr"       : colors["YLW"],
        "txt_bg_clr"    : colors["YLW"],

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["GRN"],

        "fbr_chrs"      : list(borderSets["no_border"]),
        "fbr_atr"       : 0,
        "fbr_clr"       : colors["BLK"],

        "fttl_atr"      : 0,
        "fttl_clr"      : colors["GRN"],

        "ftxt_atr"      : 0,
        "ftxt_clr"      : colors["RYLW"],
        "ftxt_bg_clr"   : colors["RYLW"]
    })
    panel_styles["title_infobox"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["CYN"],

        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLK"],

        "ttl_atr"       : 0,
        "ttl_clr"       : colors["CYN"],

        "txt_atr"       : curses.A_BOLD,
        "txt_clr"       : colors["CYN"],
        "txt_bg_clr"    : colors["CYN"],

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["GRN"],

        "fbr_chrs"      : list(borderSets["no_border"]),
        "fbr_atr"       : 0,
        "fbr_clr"       : colors["BLK"],

        "fttl_atr"      : 0,
        "fttl_clr"      : colors["GRN"],

        "ftxt_atr"      : 0,
        "ftxt_clr"      : colors["RYLW"],
        "ftxt_bg_clr"   : colors["RYLW"]
    })
    panel_styles["infobox1"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["CYN"],

        "br_chrs"       : list(borderSets["all_hash"]),
        "br_atr"        : curses.A_BOLD,
        "br_clr"        : colors["BLU"],

        "ttl_atr"       : 0,
        "ttl_clr"       : colors["WHT"],

        "txt_atr"       : 0,
        "txt_clr"       : colors["CYN"],
        "txt_bg_clr"    : None,

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["CYN"],

        "fbr_chrs"      : list(borderSets["all_hash"]),
        "fbr_atr"       : curses.A_BOLD,
        "fbr_clr"       : colors["CYN"],

        "fttl_atr"      : curses.A_BOLD,
        "fttl_clr"      : colors["YLW"],

        "ftxt_atr"      : None,
        "ftxt_clr"      : None,
        "ftxt_bg_clr"   : None
    })
    panel_styles["middlepanes"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["BLU"],

        "br_chrs"       : list(borderSets["all_hash"]),
        "br_atr"        : curses.A_BOLD,
        "br_clr"        : colors["BLU"],

        "ttl_atr"       : curses.A_BOLD,
        "ttl_clr"       : colors["WHT"],

        "txt_atr"       : curses.A_BOLD,
        "txt_clr"       : colors["CYN"],
        "txt_bg_clr"    : colors["BLK"], 

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["CYN"],

        "fbr_chrs"      : list(borderSets["all_hash"]),
        "fbr_atr"       : curses.A_BOLD,
        "fbr_clr"       : colors["CYN"],

        "fttl_atr"      : curses.A_BOLD,
        "fttl_clr"      : colors["YLW"],

        "ftxt_atr"      : curses.A_BOLD,
        "ftxt_clr"      : colors["RCYN"],
        "ftxt_bg_clr"   : colors["RCYN"], 
    })
    panel_styles["infobox2"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["RBLU"],

        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLK"],

        "ttl_atr"       : curses.A_BOLD,
        "ttl_clr"       : colors["WHT"],

        "txt_atr"       : curses.A_BOLD,
        "txt_clr"       : colors["CYNBLU"],
        "txt_bg_clr"    : None,

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["RBLU"],

        "fbr_chrs"      : list(borderSets["no_border"]),
        "fbr_atr"       : 0,
        "fbr_clr"       : colors["BLK"],

        "fttl_atr"      : curses.A_BOLD,
        "fttl_clr"      : colors["CYN"],

        "ftxt_atr"      : None,
        "ftxt_clr"      : None,
        "ftxt_bg_clr"   : None
    })
    panel_styles["input_strip"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["RMGA"],

        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLK"],

        "ttl_atr"       : curses.A_BOLD,
        "ttl_clr"       : colors["RMGA"],

        "txt_atr"       : 0,
        "txt_clr"       : colors["WHT"],
        "txt_bg_clr"    : None,

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["RBLU"],

        "fbr_chrs"      : list(borderSets["no_border"]),
        "fbr_atr"       : 0,
        "fbr_clr"       : colors["BLK"],

        "fttl_atr"      : curses.A_BOLD,
        "fttl_clr"      : colors["CYN"],

        "ftxt_atr"      : curses.A_BOLD,
        "ftxt_clr"      : 0,
        "ftxt_bg_clr"   : colors["RMGA"],
    })
    panel_styles["input_strip2"] = CursePanelStyle({
        "bg_chr"        : dsh,
        "bg_atr"        : 0,
        "bg_clr"        : colors["BLU"],

        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLK"],

        "ttl_atr"       : 0,
        "ttl_clr"       : colors["BLK"],

        "txt_atr"       : 0,
        "txt_clr"       : colors["BLK"],
        "txt_bg_clr"    : colors["BLK"],

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["RRED"],

        "fbr_chrs"      : list(borderSets["no_border"]),
        "fbr_atr"       : 0,
        "fbr_clr"       : colors["BLK"],

        "fttl_atr"      : curses.A_BOLD,
        "fttl_clr"      : colors["CYN"],

        "ftxt_atr"      : curses.A_BOLD,
        "ftxt_clr"      : colors["RRED"],
        "ftxt_bg_clr"   : colors["RRED"],
    })
    panel_styles["dashscrbg"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["BLU"],

        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLK"],

        "ttl_atr"       : curses.A_BOLD,
        "ttl_clr"       : colors["RMGA"],

        "txt_atr"       : curses.A_BOLD,
        "txt_clr"       : colors["BLU"],
        "txt_bg_clr"    : None,

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["RBLU"],

        "fbr_chrs"      : list(borderSets["no_border"]),
        "fbr_atr"       : 0,
        "fbr_clr"       : colors["BLK"],

        "fttl_atr"      : curses.A_BOLD,
        "fttl_clr"      : colors["CYN"],

        "ftxt_atr"      : 0,
        "ftxt_clr"      : 0,
        "ftxt_bg_clr"   : colors["BLU"]
    })
    panel_styles["middlepanes2"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["BLU"],

        "br_chrs"       : list(borderSets["all_hash"]),
        "br_atr"        : curses.A_BOLD,
        "br_clr"        : colors["BLU"],

        "ttl_atr"       : 0,
        "ttl_clr"       : colors["WHT"],

        "txt_atr"       : curses.A_BOLD,
        "txt_clr"       : colors["CYN"],
        "txt_bg_clr"        : colors["BLK"], 

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["CYN"],

        "fbr_chrs"      : list(borderSets["all_hash"]),
        "fbr_atr"       : curses.A_BOLD,
        "fbr_clr"       : colors["CYN"],

        "fttl_atr"      : curses.A_BOLD,
        "fttl_clr"      : colors["YLW"],

        "ftxt_atr"      : curses.A_BOLD,
        "ftxt_clr"      : colors["RYLW"],
        "ftxt_bg_clr"   : colors["RYLW"], 
    })
    panel_styles["at_scrbg"] = CursePanelStyle({
        "bg_chr"        : at,
        "bg_atr"        : curses.A_DIM,
        "bg_clr"        : colors["BLU"],

        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLK"],

        "ttl_atr"       : curses.A_BOLD,
        "ttl_clr"       : colors["RMGA"],

        "txt_atr"       : curses.A_BOLD,
        "txt_clr"       : colors["BLU"],
        "txt_bg_clr"    : None,

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["RBLU"],

        "fbr_chrs"      : list(borderSets["no_border"]),
        "fbr_atr"       : 0,
        "fbr_clr"       : colors["BLK"],

        "fttl_atr"      : curses.A_BOLD,
        "fttl_clr"      : colors["CYN"],

        "ftxt_atr"      : 0,
        "ftxt_clr"      : 0,
        "ftxt_bg_clr"   : colors["BLU"]
    })
    return panel_styles