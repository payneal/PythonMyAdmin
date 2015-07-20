import curses
import cursePanel

class curseItem(object):
    """description of class"""
    def __init__(self, **kwargs):
        self.id = kwargs["id"]                           
        self.name = kwargs["name"]

        self.parent = kwargs["parent"]

        self.y = kwargs["y"]
        self.x = kwargs["x"]

        self.lbltext = kwargs["lbltext"]

        self.infotext1 = kwargs["infotext1"]
        self.infotext1tar = kwargs["infotext1tar"]
        self.infotext2 = kwargs["infotext2"]
        self.infotext2tar = kwargs["infotext2tar"]

        self.onselect = kwargs["onselect"]

        self.style = self.parent.childstyle

    def onload(self):
        self.set_style()

    def focus(self):
        self.onfocus()

    def onfocus(self):
        pass
        
    def defocus(self):
        self.ondefocus()

    def ondefocus(self):
        pass

    def set_style(self, focus=False, s_obj=0):
        try:
            if s_obj == 0:
                s_obj = self.style
        except:
            s_obj = self.dftstyle
        
        if focus == False:
            ttl_atr = s_obj.ttl_atr
            ttl_clr = s_obj.ttl_clr
        else:
            ttl_atr = s_obj.fttl_atr
            ttl_clr = s_obj.fttl_clr            

        self.set_bg(bg_chtype)                
        self.draw_lbl(lbl_atr, lbl_clr)
