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
        self.bg_chr         = kwargs["bg_chr"]
        self.bg_atr         = kwargs["bg_atr"]
        self.bg_clr         = kwargs["bg_clr"]
        self.bg_chtype      = self.bg_chr | self.bg_atr | self.bg_clr
        self.br_chrs        = list(kwargs["br_chrs"])
        self.br_atr         = kwargs["br_atr"]
        self.br_clr         = kwargs["br_clr"]
        self.ttl_atr        = kwargs["ttl_atr"]
        self.ttl_clr        = kwargs["ttl_clr"]
        self.txt_atr        = kwargs["txt_atr"]
        self.txt_clr        = kwargs["txt_clr"] 
        self.txt_bg_clr     = kwargs["txt_clr"]

        self.fbg_chr        = kwargs["fbg_chr"]
        self.fbg_atr        = kwargs["fbg_atr"]
        self.fbg_clr        = kwargs["fbg_clr"]
        self.fbg_chtype     = self.fbg_chr | self.fbg_atr | self.fbg_clr
        self.fbr_chrs       = list(kwargs["fbr_chrs"])
        self.fbr_atr        = kwargs["fbr_atr"]
        self.fbr_clr        = kwargs["fbr_clr"]
        self.fttl_atr       = kwargs["fttl_atr"]
        self.fttl_clr       = kwargs["fttl_clr"]
        self.ftxt_atr       = kwargs["ftxt_atr"]
        self.ftxt_clr       = kwargs["ftxt_clr"] 
        self.ftxt_bg_clr    = kwargs["ftxt_clr"]

        self.ibg_chr        = kwargs["ibg_chr"]
        self.ibg_atr        = kwargs["ibg_atr"]
        self.ibg_clr        = kwargs["ibg_clr"]
        self.ibg_chtype     = kwargs["ibg_chr"]|kwargs["ibg_atr"]|kwargs["ibg_clr"]
        self.ibr_chrs       = list(kwargs["ibr_chrs"])
        self.ibr_atr        = kwargs["ibr_atr"]
        self.ibr_clr        = kwargs["ibr_clr"]
        self.ittl_atr       = kwargs["ittl_atr"]
        self.ittl_clr       = kwargs["ittl_clr"]
        self.itxt_atr       = kwargs["itxt_atr"]
        self.itxt_clr       = kwargs["itxt_clr"] 
        self.itxt_bg_clr    = kwargs["itxt_clr"]

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
    curses.init_pair(16, curses.COLOR_BLUE, curses.COLOR_CYAN)    # blue /cyan

    curses.init_pair(17, curses.COLOR_BLACK, curses.COLOR_WHITE)  # white/black
    curses.init_pair(18, curses.COLOR_BLUE, curses.COLOR_YELLOW)    # blue/yllw
    curses.init_pair(19, curses.COLOR_WHITE, curses.COLOR_BLUE)     # red/yllw
    curses.init_pair(20, curses.COLOR_MAGENTA, curses.COLOR_BLUE) # blue/yllw
    curses.init_pair(21, curses.COLOR_RED, curses.COLOR_BLUE) # blue/yllw

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
                "RCYNBLU": curses.color_pair(16),
                                                "RWHT": curses.color_pair(17),
                "BLUYLW": curses.color_pair(18),
                "REDYLW": curses.color_pair(19),
                "MGAYLW": curses.color_pair(20),"REDBLU": curses.color_pair(21)}

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
        "all_at" : [ at for i in range (0, 8) ],
        "all_cln" : [ cln for i in range (0, 8) ],
        "side_hash_top_dash" : [ hsh, hsh, dsh, dsh, hsh, hsh, hsh, hsh ],
        "w_s_hash_n_dash_e_vline" : [ hsh, vln, dsh, hsh, hsh, dsh, hsh, vln],
        "w_e_vline_nw_ne_sw_se_pls_n_s_dsh": [vln,vln,dsh,dsh,pls,pls,pls,pls],
        "unicode_box": [vuline, vuline, huline, huline, 
                        NWcrner, NEcrner, SWcrner, SEcrner],
        "no_border" : [-1]}

    #self.init_color_pairs()

    panel_styles = {}
    panel_styles["COLORS"] = colors
    panel_styles["default"] = CursePanelStyle({
        #normal						
        "bg_chr"	:	sp	,	#	background	character
        "bg_atr"	:	0	,	#	background	attribute
        "bg_clr"	:	colors["BLU"]	,	#	background	color
        "br_chrs"	:	[0]	,	#	border	characters
        "br_atr"	:	0	,	#	border	attribute
        "br_clr"	:	colors["RED"]	,	#	border	color
        "ttl_atr"	:	0	,	#	title	attribute
        "ttl_clr"	:	colors["RED"]	,	#	title	color
        "txt_atr"	:	0	,	#	text	attribute
        "txt_clr"	:	colors["RED"]	,	#	text	color
        "txt_bg_clr"	:	colors["RED"]	,	#	text	background color
        #focused						
        "fbg_chr"	:	sp	,	#	background	character
        "fbg_atr"	:	0	,	#	background	attribute
        "fbg_clr"	:	colors["RED"]	,	#	background	color
        "fbr_chrs"	:	[0]	,	#	border	characters
        "fbr_atr"	:	0	,	#	border	attribute
        "fbr_clr"	:	colors["BLU"]	,	#	border	color
        "fttl_atr"	:	0	,	#	title	attribute
        "fttl_clr"	:	colors["RED"]	,	#	title	color
        "ftxt_atr"	:	0	,	#	text	attribute
        "ftxt_clr"	:	colors["RED"]	,	#	text	color
        "ftxt_bg_clr"	:	colors["RED"]	,	#	text	background color
        #inactive						
        "ibg_chr"	:	sp	,	#	background	character
        "ibg_atr"	:	0	,	#	background	attribute
        "ibg_clr"	:	colors["RED"]	,	#	background	color
        "ibr_chrs"	:	[0]	,	#	border	characters
        "ibr_atr"	:	0	,	#	border	attribute
        "ibr_clr"	:	colors["RED"]	,	#	border	color
        "ittl_atr"	:	0	,	#	title	attribute
        "ittl_clr"	:	colors["RED"]	,	#	title	color
        "itxt_atr"	:	0	,	#	text	attribute
        "itxt_clr"	:	colors["RED"]	,	#	text	color
        "itxt_bg_clr"	:	colors["RED"]		#	text	background color

    })
    panel_styles["style1"] = CursePanelStyle({
        #normal			
        "bg_chr"	:	sp	,
        "bg_atr"	:	0	,
        "bg_clr"	:	colors["BLU"]	,
        "br_chrs"	:	list(borderSets["side_hash_top_dash"]),
        "br_atr"	:	0	,
        "br_clr"	:	colors["BLU"]	,
        "ttl_atr"	:	0	,
        "ttl_clr"	:	colors["RED"]	,
        "txt_atr"	:	0	,
        "txt_clr"	:	colors["RED"]	,
        "txt_bg_clr"	:	colors["RED"]	,
        #focused			
        "fbg_chr"	:	sp	,
        "fbg_atr"	:	0	,
        "fbg_clr"	:	colors["CYN"]	,
        "fbr_chrs"	:	list(borderSets["side_hash_top_dash"])	,
        "fbr_atr"	:	curses.A_BOLD	,
        "fbr_clr"	:	colors["CYN"]	,
        "fttl_atr"	:	curses.A_BOLD	,
        "fttl_clr"	:	colors["YLW"]	,
        "ftxt_atr"	:	0	,
        "ftxt_clr"	:	colors["RED"]	,
        "ftxt_bg_clr"	:	colors["RED"]	,
        #inactive			
        "ibg_chr"	:	sp	,
        "ibg_atr"	:	0	,
        "ibg_clr"	:	colors["RED"]	,
        "ibr_chrs"	:	[0]	,
        "ibr_atr"	:	0	,
        "ibr_clr"	:	colors["RED"]	,
        "ittl_atr"	:	0	,
        "ittl_clr"	:	colors["RED"]	,
        "itxt_atr"	:	0	,
        "itxt_clr"	:	colors["RED"]	,
        "itxt_bg_clr"	:	colors["RED"]	
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
        "ftxt_bg_clr"   : None,
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
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
        "txt_atr"       : 0,#curses.A_BOLD,
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
        "ftxt_bg_clr"   : colors["GRN"],
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
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
        "txt_atr"       : 0,#curses.A_BOLD,
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
        "ftxt_atr"      : curses.A_BOLD,
        "ftxt_clr"      : colors["RYLW"],
        "ftxt_bg_clr"   : colors["RYLW"],
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
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
        "ftxt_bg_clr"   : colors["RYLW"],
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
    })
    panel_styles["infobox1"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["CYN"],
        "br_chrs"       : list(borderSets["all_hash"]),
        "br_atr"        : curses.A_BOLD,
        "br_clr"        : colors["BLU"],
        "ttl_atr"       : 0,
        "ttl_clr"       : colors["RED"],
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
        "ftxt_bg_clr"   : None,
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
    })
    panel_styles["middlepanes"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["BLU"],
        "br_chrs"       : list(borderSets["all_hash"]),
        "br_atr"        : curses.A_BOLD,
        "br_clr"        : colors["BLU"],
        "ttl_atr"       : curses.A_BOLD,
        "ttl_clr"       : colors["GRN"],
        "txt_atr"       : 0, #curses.A_BOLD,
        "txt_clr"       : colors["YLW"],
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
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	 
    })
    panel_styles["infobox2"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : curses.A_BOLD,
        "bg_clr"        : colors["CYNBLU"],
        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLK"],
        "ttl_atr"       : curses.A_BOLD,
        "ttl_clr"       : colors["CYNBLU"],
        "txt_atr"       : curses.A_BOLD,
        "txt_clr"       : colors["CYNBLU"],
        "txt_bg_clr"    : None,

        "fbg_chr"       : sp,
        "fbg_atr"       : curses.A_BOLD,
        "fbg_clr"       : colors["CYNBLU"],
        "fbr_chrs"      : list(borderSets["no_border"]),
        "fbr_atr"       :curses.A_BOLD,
        "fbr_clr"       : colors["BLK"],
        "fttl_atr"      : curses.A_BOLD,
        "fttl_clr"      : colors["CYNBLU"],
        "ftxt_atr"      : None,
        "ftxt_clr"      : None,
        "ftxt_bg_clr"   : None,
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
    })
    panel_styles["input_strip"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : curses.A_BOLD,
        "bg_clr"        : colors["RBLU"],
        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLK"],
        "ttl_atr"       : curses.A_BOLD,
        "ttl_clr"       : colors["RBLU"],
        "txt_atr"       : curses.A_BOLD,
        "txt_clr"       : colors["RED"],
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
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
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
        "txt_clr"       : colors["GRN"],
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
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
    })
    panel_styles["input_strip3"] = CursePanelStyle({
        "bg_chr"        : dsh,
        "bg_atr"        : 0,
        "bg_clr"        : colors["RED"],
        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLU"],
        "ttl_atr"       : 0,
        "ttl_clr"       : colors["GRN"],
        "txt_atr"       : 0,
        "txt_clr"       : colors["GRN"],
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
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
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
        "ftxt_bg_clr"   : colors["BLU"],
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
    })
    panel_styles["dashscrbg2"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["BLU"],
        "br_chrs"       : list(borderSets["all_hash"]),
        "br_atr"        : curses.A_BOLD,
        "br_clr"        : colors["BLU"],
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
        "ftxt_bg_clr"   : colors["BLU"],
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
    })
    panel_styles["colonscrbg2"] = CursePanelStyle({
        "bg_chr"        : cln,
        "bg_atr"        : curses.A_BOLD,
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
        "ftxt_bg_clr"   : colors["BLU"],
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
    })
    panel_styles["middlepanes2"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["BLU"],
        "br_chrs"       : list(borderSets["all_hash"]),
        "br_atr"        : curses.A_BOLD,
        "br_clr"        : colors["BLU"],
        "ttl_atr"       : 0,
        "ttl_clr"       : colors["RED"],
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
        "ftxt_clr"      : colors["RYLW"],
        "ftxt_bg_clr"   : colors["RYLW"],
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	 
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
        "ftxt_bg_clr"   : colors["BLU"],
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
    })
    panel_styles["dot_scrbg"] = CursePanelStyle({
        "bg_chr"        : dot,
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
        "ftxt_bg_clr"   : colors["BLU"],
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
    })
    panel_styles["middlepanes3"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["BLU"],
        "br_chrs"       : list(borderSets["all_hash"]),
        "br_atr"        : curses.A_BOLD,
        "br_clr"        : colors["CYN"],
        "ttl_atr"       : curses.A_BOLD,
        "ttl_clr"       : colors["GRN"],
        "txt_atr"       : curses.A_BOLD,
        "txt_clr"       : colors["CYN"],
        "txt_bg_clr"        : colors["BLK"],
        #focus 
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
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	 
    })


    panel_styles["login_entry"] = CursePanelStyle({
        "bg_chr"        : dsh,
        "bg_atr"        : 0,
        "bg_clr"        : colors["RED"],
        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLU"],
        "ttl_atr"       : 0,
        "ttl_clr"       : colors["GRN"],
        "txt_atr"       : 0,
        "txt_clr"       : colors["GRN"],
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
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
    })
    panel_styles["login_entry_OK"] = CursePanelStyle({
        "bg_chr"        : dsh,
        "bg_atr"        : 0,
        "bg_clr"        : colors["BLU"],
        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLU"],
        "ttl_atr"       : 0,
        "ttl_clr"       : colors["GRN"],
        "txt_atr"       : 0,
        "txt_clr"       : colors["GRN"],
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
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
    })
    panel_styles["login_optionbox"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["RED"],
        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLU"],
        "ttl_atr"       : 0,
        "ttl_clr"       : colors["GRN"],
        "txt_atr"       : 0,
        "txt_clr"       : colors["GRN"],
        "txt_bg_clr"    : colors["BLK"],

        "fbg_chr"       : sp,
        "fbg_atr"       : 0,
        "fbg_clr"       : colors["RED"],
        "fbr_chrs"      : list(borderSets["no_border"]),
        "fbr_atr"       : 0,
        "fbr_clr"       : colors["RGRN"],
        "fttl_atr"      : curses.A_BOLD,
        "fttl_clr"      : colors["RGRN"],
        "ftxt_atr"      : curses.A_BOLD,
        "ftxt_clr"      : colors["RGRN"],
        "ftxt_bg_clr"   : colors["RGRN"],
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
    })

    panel_styles["usermain_listbox"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : 0,
        "bg_clr"        : colors["GRN"],
        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : 0,
        "br_clr"        : colors["BLK"],
        "ttl_atr"       : curses.A_BOLD,
        "ttl_clr"       : colors["GRN"],
        "txt_atr"       : curses.A_BOLD,
        "txt_clr"       : colors["GRN"],
        "txt_bg_clr"    : None,

        "fbg_chr"       : sp,
        "fbg_atr"       : curses.A_BOLD,
        "fbg_clr"       : colors["GRN"],
        "fbr_chrs"      : list(borderSets["no_border"]),
        "fbr_atr"       : 0,
        "fbr_clr"       : colors["BLK"],
        "fttl_atr"      : curses.A_BOLD,
        "fttl_clr"      : colors["CYN"],
        "ftxt_atr"      : curses.A_BOLD,
        "ftxt_clr"      : colors["RED"],
        "ftxt_bg_clr"   : colors["RMGA"],
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["RED"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["RED"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["RED"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["RED"],
        "itxt_bg_clr"	: colors["RED"]	
    })

    tmp_attr = curses.A_BOLD
    panel_styles["key_menu"] = CursePanelStyle({
        "bg_chr"        : sp,
        "bg_atr"        : tmp_attr,
        "bg_clr"        : colors["REDYLW"],
        "br_chrs"       : list(borderSets["no_border"]),
        "br_atr"        : tmp_attr,
        "br_clr"        : colors["BLK"],
        "ttl_atr"       : tmp_attr,
        "ttl_clr"       : colors["REDYLW"],
        "txt_atr"       : tmp_attr,
        "txt_clr"       : colors["REDYLW"],
        "txt_bg_clr"    : colors["REDYLW"],

        "fbg_chr"       : sp,
        "fbg_atr"       : tmp_attr,
        "fbg_clr"       : colors["REDYLW"],
        "fbr_chrs"      : list(borderSets["no_border"]),
        "fbr_atr"       : tmp_attr,
        "fbr_clr"       : colors["BLK"],
        "fttl_atr"      : tmp_attr,
        "fttl_clr"      : colors["REDYLW"],
        "ftxt_atr"      : tmp_attr,
        "ftxt_clr"      : colors["REDYLW"],
        "ftxt_bg_clr"   : colors["REDYLW"],
        #inactive			
        "ibg_chr"	    : sp,
        "ibg_atr"	    : 0,
        "ibg_clr"	    : colors["REDBLU"],
        "ibr_chrs"	    : list(borderSets["no_border"]),
        "ibr_atr"	    : 0,
        "ibr_clr"	    : colors["REDBLU"],
        "ittl_atr"	    : 0,
        "ittl_clr"	    : colors["REDBLU"],
        "itxt_atr"	    : 0,
        "itxt_clr"	    : colors["REDBLU"],
        "itxt_bg_clr"	: colors["REDBLU"]	
    })
    return panel_styles