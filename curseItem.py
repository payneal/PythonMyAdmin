import copy
import curses
import curses.ascii

class CurseItem(object):
    """ a thing 
    
    parentPanel: the cursePanel that the curseItem is stored in
         y: y origin, relative to parentPanel's yx coordinates
         x: x origin, relative to parentPanel's yx coordinates
    height: 
    width :
    
    """

    def __init__(self, **kwargs):
        self.container              = kwargs["container"]
        self.global_storage         = kwargs["global_storage"] 
        self.parent_screen          = kwargs["parent_screen"]
        self.parent_panel           = kwargs["parent"]
        self.item_storage           = {}
        
        self.err_flag               = False
        
        self.y                      = kwargs["size"][0]
        self.x                      = kwargs["size"][1]
        self.height                 = kwargs["size"][2]
        self.width                  = kwargs["size"][3]
                      
        self.label                  = kwargs["label"]
        self.base_label             = copy.copy(self.label)

        if "header" in kwargs       : self.header      = True
        else                        : self.header      = False

        if "info" in kwargs         : self.info        = kwargs["info"]
        else                        : self.info        = None

        if "infotar" in kwargs      : self.infotar_str = kwargs["infotar"] 
        else                        : self.infotar_str = None
        self.infotar = None 

        if "focusable" in kwargs    : self.focusable   = kwargs["focusable"]
        else                        : self.focusable   = True
        self.is_focused = False

        if "_on_select" in kwargs   : self._on_select   = kwargs["_on_select"]
        else                        : self._on_select   = None
        if "selectable" in kwargs   : self.selectable   = kwargs["selectable"]
        else                        : self.selectable   = False
        self.is_selected = False

        if "active" in kwargs       : self.is_active = kwargs["active"]
        else: self.is_active = True

        if "hotkey" in kwargs:
            self.hotkey = kwargs["hotkey"]

        # _focus_key is key to panel that will be focused when the item is
        if "_focus_key" in kwargs   : self._focus_key = kwargs["_focus_key"]

        self.style               = kwargs["style"]

    #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
      
    def load(self):
        self.label = copy.copy(self.base_label)
        if hasattr(self, "_on_load"):
            if self._on_load["action"] == "call_function":
                func = getattr(self, _on_load["action_name"])
                func(*_on_load["action_args"])

    def draw(self):
        """ draws item to screen in parent's window """
        if self.is_active == True:
            if self.is_focused == False: 
                attr  = self.style.txt_atr | self.style.txt_clr
                bttr = self.style.txt_bg_clr
            else:                      
                attr = self.style.ftxt_atr | self.style.ftxt_clr
                bttr = self.style.ftxt_bg_clr
        else:
            attr  = self.style.itxt_atr | self.style.itxt_clr
            bttr = self.style.itxt_bg_clr         

        try:
            self.drawBgLine(self.parent_panel.win,self.y,self.x,32,
                            self.width,bttr)
            self.parent_panel.win.addstr(self.y, self.x, self.label, attr)
        except: 
            # there is a bug in the python curses library where if
            # addch or addstr is used at the lower right edge of 
            # the window, the cursor moves off the screen and 
            # raises an error; this is unintended behavior
            pass

        if hasattr(self, "hotkey"):
            if self.is_active == True:
                try:
                    self.parent_panel.win.addch(
                        self.y ,
                        self.x + self.hotkey["labl_index"],
                        self.hotkey["h_key"],
                        self.hotkey["attr"] | curses.A_BOLD)
                except: pass

        self.parent_panel.changed = True

    def focus(self):
        """ sets item focus, redraws item and any infotex to screen """
        self.is_focused = True
        if hasattr(self, "_focus_key"):
            self.parent_screen.getPanelByName(self._focus_key).focus()
        self.draw()
        self.setInfo()

    def activate(self):
        self.is_active = True
        if hasattr(self, "_focus_key"):
            self.parent_screen.getPanelByName(self._focus_key).activate()
        self.draw()
        self.setInfo()
          
    def defocus(self):
        """ clears item focus, redraws item and removes infotex from screen """
        self.is_focused = False
        if hasattr(self, "_focus_key"):
            self.parent_screen.getPanelByName(self._focus_key).defocus()
        self.draw()
        self.setInfo(True)
   
    def deactivate(self):
        self.is_active = False
        if hasattr(self, "_focus_key"):
            self.parent_screen.getPanelByName(self._focus_key).deactivate()
        self.draw()
        self.setInfo(True)

    def select(self):
        """ function called when curseItem is selected
       
        message structure 
        {
            msg_status      <string>  : has message be read yet
            send_layer      <string>  : where did the message originate
            recv_layer      <string>  : what layer in object hierarchy gets msg
            recv_layer      <string>  : name of object to receive message
            on_recv         <string>  : what to do in response to message
                    "call_function"   : "recv_act" will be a function name
            recv_act        <string>  : name of function/command
            recv_args       <list<?>> : arguments for function
            ret_info        <string>  : function return value or misc information
        }

        selected item checks if it is supposed to make func call, if so,
        it calls the function, stores the return value, and flags the
        message dict that the func has been called and objects higher
        in the family tree do not need to check the message 

        """

        if self._on_select == None:    return None
        message = { "msg_status"  : "unread", 
                    "send_layer"  : self._on_select["send_layer"], 
                    "recv_layer"  : self._on_select["recv_layer"], 
                    "recv_name"   : self._on_select["recv_name"],   
                    "on_recv"     : self._on_select["on_recv"], 
                    "recv_act"    : self._on_select["recv_act"], 
                    "recv_args"   : self._on_select["recv_args"] }
        if "replace_msg" in self._on_select: message["replace_msg"] = True
        
        return self.readMessage(message)

    def redrawLabel(self, text=None):
        if text==None:
            text = copy.copy(self.base_label)
        self.label = copy.copy(text)
        self.draw()
        self.parent_panel.win.refresh()

    #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

    def readMessage(self, msg):
        """ checks if it is message recvr, executes msg contents if it is """
        if msg == None:  return
        
        if msg["msg_status"] == "unread":
            if msg["recv_layer"] == "item" or msg["recv_layer"] == "self":
                if msg["on_recv"] == "call_function":
                    if hasattr(self, msg["recv_act"]):

                        func = getattr(self, msg["recv_act"])
                        if msg["recv_args"] == None:   msg["ret_info"] = func()
                        else:         msg["ret_info"] = func(*msg["recv_args"])

                        msg["msg_status"] = "read"
                        if "replace_msg" in msg:
                            if msg["ret_info"] != None:
                                msg_new = copy.deepcopy(msg["ret_info"])
                                msg = msg_new
        return msg

    def changeInfo(self, text):
        """ change current info to new info and draw to screen """
        if self.infotar != None:
            self.info = copy.copy(text)
            self.setInfo()

    def setInfo(self, hide=False):
        """ clear or set infobox data, then draws to screen """   
        if self.infotar != None:
            if hide == False:              self.infotar.resetTextbox(self.info)
            else:                                   self.infotar.resetTextbox()
            self.infotar.drawTextbox()

##################################################################################
    ### HERE THAR BEE DRAGYNS !!! BEWARRR vvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def getUserString(self,val_str,ch_attr,out_pnl,out_offset,val_range,modes):
        """ gets a string of entered characters from user   
          
        format_str :    a string that indicates what chr types can be input;
            string should be in the following form using 1 for ok or 0 for not

                    "[alpha][digit][whitespace][punctuation]"

            e.g. only alpha,digit chars are ok: "1100"
            e.g.                 only punct ok: "0001"
                     
        ch_attr:         graphic text attributes to give echo'd input text
        str_out_win:     window where echo'd output is shown
        info_out_txtbox: where error/info messages are shown regarding input
        out_yx:          y,x coords in str_out_win output is echo'd, relative
                         to str_out_win's origin
        min_len:         minimum # of characters that must be entered
        max_len:         maximum # of characters that can be entered
        echo_mode:       boolean for whether to echo input to screen or not
        pw_mode:         boolean for whether to echo input as "@" or as input
        cleanup:         boolean for whether to remove echo'd input when done

        """
        in_win          = self.global_storage["input_win"]
        out_win         = out_pnl.win

        y               = out_offset[0]
        x               = out_offset[1]
        min_len         = val_range[0]
        max_len         = val_range[1]  # max possible length of input string
        max_strip_len   = val_range[2]  # max length of input strip
        draw_indices    = [0,1]         # string index start, end, length
        max_counter     = max_len
        echo_mode       = modes[0]
        pw_mode         = modes[1]
        cleanup_mode    = modes[2]
      
        pre_bg_ch       = ord("-")
        self.drawBgLine(out_win, y, x, 32, max_strip_len + 1, ch_attr)
        in_bg_ch        = out_win.inch(y, x)
        out_win.refresh()

        in_len          = 0
        out_str         = ""
        status          = "NA"

        while True:
            in_i = in_win.getch()  # GET INPUT CHAR                                     
            status = self.checkChar(val_str, in_i, in_len, min_len) # CHECK CHR  
            if status == "IGNORE":continue
            if status == "OK":                            
                out_str += chr(in_i)                       # UPDATE OUTPUT STR
                if echo_mode == True:                      # DRAW KEY TO WIN
                    self.drawOStr(out_win, out_str, y, x, draw_indices, 
                        pw_mode, ch_attr)
                in_len += 1
                max_counter -= 1
                if draw_indices[1] < max_len:
                    draw_indices[1] = draw_indices[1] + 1
                if in_len >= max_strip_len:
                    draw_indices[0] = draw_indices[0] + 1                                              
                        
            elif status == "DELETE":
                if in_len > 0:
                    in_len -= 1                   
                    max_counter += 1
                    draw_indices[1] = draw_indices[1] - 1 
                    if draw_indices[0] > 0:
                        draw_indices[0] = draw_indices[0] - 1
                        self.drawOStr(out_win, out_str, y, x, draw_indices, 
                            pw_mode, ch_attr)
                        if draw_indices[0] == 0:
                            out_win.addch(y, x + in_len, in_bg_ch)
                    else:
                        out_win.addch(y, x + in_len, in_bg_ch)
                    out_str = out_str[:-1]
                status = "OK"      
           
            out_win.refresh()                              # REFRESH AFTER DRAW

            if in_len == max_len:        status = "OK_DONE"                      
            if status != "OK":                        break
        
        if cleanup_mode == True or status != "OK_DONE":
            out_win.hline(y, x, pre_bg_ch, max_strip_len + 1)
            out_win.refresh()
        else:
            out_win.hline(y, x, pre_bg_ch, max_strip_len + 1)
            if pw_mode == False:
                if len(out_str) <= max_strip_len:
                    out_win.addstr(y,x, out_str,
                        out_pnl.style.txt_clr | out_pnl.style.txt_atr)
                else:
                    out_win.addstr(y,x, out_str[0:max_strip_len],
                        out_pnl.style.txt_clr | out_pnl.style.txt_atr)
                    try:
                        out_win.addstr(y,x+max_strip_len-2, "...",
                            out_pnl.style.txt_clr | out_pnl.style.txt_atr)
                    except: 
                        # there is a bug in the python curses library where if
                        # addch or addstr is used at the lower right edge of 
                        # the window, the cursor moves off the screen and 
                        # raises an error; this is unintended behavior
                        pass
            else:
                for i in range(0, len(out_str)):
                    out_win.addch(y, x + i, ord("@"), 
                        out_pnl.style.txt_clr | out_pnl.style.txt_atr)
            out_win.refresh()

        return (status, out_str)
    
    def drawOStr(self, win, str, y, x, draw_indices, pw, attr):
        start_index = draw_indices[0]
        end_index = draw_indices[1]
        x_pos = copy.copy(x)
        for c in range (start_index, end_index):
            ch = ord(str[c])
            if pw == False:     win.addch(y, x_pos, ch | attr)
            else:               win.addch(y, x_pos, ord("@") | attr)
            x_pos += 1
            
    def drawBgLine(self, win, y, x, ch, len, battr):
        try:
            win.attron(battr)
            win.hline(y, x, ch, len)
            win.attroff(battr)
        except: win.attroff(battr)
        
    def checkChar(self, format_str, input_i, in_len, min_len):
        if input_i == ord("\n"): 
            if in_len >= min_len:                        status = "OK_DONE"
            else:                                        status = "ERR_MIN"
        elif input_i == curses.KEY_DC:                   status = "DELETE"
        elif input_i == curses.KEY_BACKSPACE:            status = "DELETE"
        elif input_i > 255:                              status = "IGNORE"
        elif input_i < 0:                                status = "IGNORE"
        else:             status = self.validate_char(format_str, input_i)    
        return status

    # format string: [alpha][digit][whitespace][punctuation]
    def validate_char(self, format, input_i):     
        if format[0] == "0":
            if curses.ascii.isalpha(input_i) != False:
                return "ERR_ALPHA"
        if format[1] == "0":
            if curses.ascii.isdigit(input_i) != False:
                return "ERR_DIGIT"
        if format[2] == "0":
            if curses.ascii.isspace(input_i) != False:
                return "ERR_SPACE"
        if format[3] == "0":
            if curses.ascii.ispunct(input_i) != False:
                return "ERR_PUNCT"         
        return "OK"
    
    def showErrorMsg(self, status, sargs, change_flag, err_txtbox):
        if status == "ERR_MIN":
            msg = "Input must be at least "+str(sargs[0])+" characters or longer!"
        elif status == "ERR_ALPHA":
            msg = "Input cannot contain alphabetic characters!"
        elif status == "ERR_DIGIT":    
            msg = "Input cannot contain numeric characters!"
        elif status == "ERR_SPACE":
            msg = "Input cannot contain whitespace characters!"
        elif status == "ERR_PUNCT":
            msg = "Input cannot contain punctuation characters!"
        elif status == "NOKEY":
            msg = "Missing entry \'"+sargs[0]+"\' from submission!"
        else:
            msg = "Undefined error!"

        if status == "OK_DONE":
            if change_flag == True:
                self.err_flag = False
        else:
            if change_flag == True:
                self.err_flag = True  
            err_txtbox.resetText(msg)
            err_txtbox.drawText()
            err_txtbox.parent.win.refresh()
#
#   curses.napms(x) : sleeps for x milliseconds