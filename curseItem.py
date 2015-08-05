import curses
import curses.ascii
import copy
#from cursePanel import CursePanel

class CurseItem(object):
    """ a thing 
    
    parentPanel: the cursePanel that the curseItem is stored in
         y: y origin, relative to parentPanel's yx coordinates
         x: x origin, relative to parentPanel's yx coordinates
    height: 
    width :
    
    """

    def __init__(self, **kwargs):
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
        if self.is_focused == False: 
            attr  = self.style.txt_atr | self.style.txt_clr
            battr = self.style.txt_bg_clr
        else:                      
            attr = self.style.ftxt_atr | self.style.ftxt_clr
            battr = self.style.ftxt_bg_clr         

        self.drawBgLine(self.parent_panel.win, self.y, self.x, 32, self.width, battr)
        self.parent_panel.win.addstr(self.y, self.x, self.label, attr)

        self.parent_panel.changed = True

    def focus(self):
        """ sets item focus, redraws item and any infotex to screen """
        self.is_focused = True
        self.draw()
        self.setInfo()
          
    def defocus(self):
        """ clears item focus, redraws item and removes infotex from screen """
        self.is_focused = False
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

        if self._on_select == None:                                  return None
        message = { "msg_status"  : "unread", 
                    "send_layer"  : self._on_select["send_layer"], 
                    "recv_layer"  : self._on_select["recv_layer"], 
                    "recv_name"   : self._on_select["recv_name"],   
                    "on_recv"     : self._on_select["on_recv"], 
                    "recv_act"    : self._on_select["recv_act"], 
                    "recv_args"   : self._on_select["recv_args"] }
        
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

        if msg == None:                                                  return
        
        if msg["msg_status"] == "unread":
            if msg["recv_layer"] == "screen" or msg["recv_layer"] == "self":
                if msg["on_recv"] == "call_function":

                    func = getattr(self, msg["recv_act"])
                    #if msg["recv_args"] == None:  
                    #    msg["ret_info"] = func()
                    #else:        
                    msg["ret_info"] = func(*msg["recv_args"])

                    msg["msg_status"] = "read"

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

    def getUserString(self, format_str, ch_attr, str_out_pnl, 
        out_yx, min_len, max_len, echo_mode, pw_mode, cleanup):
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
        input_win       = self.global_storage["input_win"]
        str_out_win     = str_out_pnl.win
        input_length    = 0
        output_str      = ""
        y = out_yx[0]
        x = out_yx[1]

        orig_bg_ch      = str_out_win.inch(y, x)
        orig_cursor_pos = str_out_win.getyx()

        status = "NA"

        self.drawBgLine(str_out_win, y, x, 32, max_len, ch_attr)
        input_bg_ch     = str_out_win.inch(y, x)

        str_out_win.refresh()
        while True:
            input_i = input_win.getch()                        # GET INPUT CHAR                             
            status = self.checkChar(
                format_str, input_i, input_length, min_len)  # CHECK INPUT CHAR
                      
            if status == "OK":                            
                output_str += chr(input_i)                  # UPDATE OUTPUT STR
                if echo_mode == True:                         # DRAW KEY TO WIN
                    if pw_mode == True:        
                        str_out_win.addch(y, x + input_length,ord("@")|ch_attr)
                    else:                      
                        str_out_win.addch(y, x + input_length, input_i|ch_attr)
                input_length += 1
                
            elif status == "DELETE":
                if input_length > 0:
                    input_length -= 1
                    str_out_win.addch(y, x + input_length, input_bg_ch)
                status = "OK"
            
            str_out_win.refresh()                          # REFRESH AFTER DRAW

            if input_length == max_len: 
                status = "OK_DONE"                      
            if status != "OK":                       
                break
        # loop end ---------------------
        if cleanup == True or status != "OK_DONE":
            str_out_win.hline(y, x, orig_bg_ch, max_len)
            str_out_win.refresh()
        else:
            str_out_win.hline(y, x, orig_bg_ch, max_len)
            if pw_mode == False:
                str_out_win.addstr(y, x, output_str, 
                    str_out_pnl.style.txt_clr | str_out_pnl.style.txt_atr)
            else:
                for i in range(0, len(output_str)):
                    str_out_win.addch(y, x + i, ord("@"), 
                        str_out_pnl.style.txt_clr | str_out_pnl.style.txt_atr)
            str_out_win.refresh()

        return (status, output_str)
    
    def drawBgLine(self, win, y, x, ch, len, battr):
        win.attron(battr)
        win.hline(y, x, ch, len)
        win.attroff(battr)
        
    def checkChar(self, format_str, input_i, in_len, min_len):
        if input_i == ord("\n"): 
            if in_len >= min_len:                        status = "OK_DONE"
            else:                                        status = "ERR_MIN"
        elif input_i == curses.KEY_DC:                   status = "DELETE"
        else: # VALIDATE INPUT  
            status = self.validate_char(format_str, input_i)    
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

        if status == "OK_DONE":
            if change_flag == True:
                self.err_flag = False
        else:
            if change_flag == True:
                self.err_flag = True  
            err_txtbox.resetText(msg)
            err_txtbox.drawText()
            err_txtbox.parent.win.refresh()
