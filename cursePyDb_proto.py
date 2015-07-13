import curses
import curses.panel

# abbreviation key:
# pnl = panel
# txt = text
# off = offset
# coords = coordinates

# main application code
def cursedPyDbApp(scr):
    stdscr = scr
    cbp = CursePyPanel(
        0, "title_panel", "title panel", None, 
        (0, 0), 
        (0, 1), 
        (10, 10), 
        0, 
        True)

    cbp.set_style()
    cbp.base_win.refresh()
    curses.doupdate()
    curses.napms(5000)
      
class CursePyPanel:
    def __init__(self):
        self.isinit = False

        # INIT ARGUMENT VARS
        #
        # pnl_id <int>:                unique int used for tracking pnl
        # pnl_name <string>:           unique name used for tracking pnl
        # title_txt <string>:          displayed title/header txt for pnl
        # par_pnl <CursePyPanel>:      pnl that spawned this pnl
        # off_coords <int, int>:       offset coords from parent
        # title_off_coords <int, int>: title txt coords rel to panel org
        # size <int, int>:             #rows / columns window is
        # depth <int>:                 # pnls deep from stdscr
        # visible <bool>:              is panel visible
        
    def  __init__( self, p_id, name, title, par_pnl, offset_coords,               
                    title_off_coords, size, depth, visible):

        self.isinit = True                      # CursePyPanel.isinit
        self.pnl_id = p_id                      # CursePyPanel.pnl_id
        self.pnl_name = name                    # CursePyPanel.pnl_name
        self.title_txt = title                  # CursePyPanel.title_txt
        self.par_pnl = par_pnl                  # CursePyPanel.par_pnl

        if par_pnl != None:
                                                # CursePyPanel.offset_coords
            self.offset_coords = ( 
                                par_pnl.offset_coords[0] + offset_coords[0],
                                par_pnl.offset_coords[1] + offset_coords[1])
                                                # CursePyPanel.base_win    
            self.base_win = par_pnl.derwin(
                                height, width, 
                                offset_coords[0], offset_coords[1])             
        else:
                                                # CursePyPanel.offset_coords
            self.offset_coords = ( offset_coords[0], offset_coords[1])     
                                                # CursePyPanel.base_win       
            self.base_win = curses.newwin(
                size[0], size[1], offset_coords[0], offset_coords[1])           
            
                                                # CursePyPanel.base_pnl
        self.base_pnl = curses.panel.new_panel(self.base_win)                
                                                # CursePyPanel.title_off_coords                       
        self.title_off_coords = title_off_coords      
                                                                     
        self.depth = depth                      # CursePyPanel.depth                                                 

        self.has_focus = False                  # CursePyPanel.has_focus                                                    
        if not visible == True:
            self.base_pnl.hide()

    # accessor for origin of CursePyPanel
    def get_scr_off(self):
        return self.base_win.getbegyx()
    
    # accessor for y,x dimensions of CursePyPanel
    def get_size(self):
        return self.base_win.getmaxyx()

    # mutator for style attributes of CursePyPanel
    def set_style(self):
        self.base_win.border(0)

class CursePyPanelStyleObj:
    def __init__(self):
        self.isinit = False

    def __init__(self, par_pnl, bkgd_chtype, brdr_chtypes, brdr_color, 
                 title_color, txt_color, sel_txt_color):
        self.par_pnl = par_pnl
        self.isinit = True
        self.bg_chtype = bkgd_chtype
        self.brdr_chtypes = list(brdr_chtypes)
        self.title_color = title_color
        self.txt_color = txt_color
        self.sel_txt_color = sel_txt_color

    def set_all_style(self):
        if self.isinit == True:
            self.par_pnl.base_win.bkgdset(self.bg_chtype)
            self.par_pnl.base_win.border(
                self.brdr_chtypes[0], self.brdr_chtypes[1], 
                self.brdr_chtypes[2], self.brdr_chtypes[3],
                self.brdr_chtypes[4], self.brdr_chtypes[5],
                self.brdr_chtypes[6], self.brdr_chtypes[7])
    

if __name__ == "__main__":
    # wrapper initializes curses screen settings and 
    # restores original terminal screen settings on error/close
    # wrapper is passed and calls an object 
    # that contains the main application's code
    curses.wrapper(cursedPyDbApp)