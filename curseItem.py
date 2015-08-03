import curses
import curses.ascii
import copy
#from cursePanel import CursePanel

class CurseItem(object):
    """ a thing 
    
    parent: the cursePanel that the curseItem is stored in
         y: y origin, relative to parent's yx coordinates
         x: x origin, relative to parent's yx coordinates
    height: 
    width :

    
    """
    def __init__(self, **kwargs):
        self.globals         = kwargs["globals"] 
        self.parent                 = kwargs["parent"]
        
        self.y                      = kwargs["size"][0]
        self.x                      = kwargs["size"][1]
        self.height                 = kwargs["size"][2]
        self.width                  = kwargs["size"][3]
                      
        self.label                  = kwargs["label"]

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
      
    def draw(self):
        """ draws item to screen in parent's window """
        if self.is_focused == False: 
            attr  = self.style.txt_atr | self.style.txt_clr
            battr = self.style.txt_bg_clr
        else:                      
            attr = self.style.ftxt_atr | self.style.ftxt_clr
            battr = self.style.ftxt_bg_clr         

        self.drawBgLine(self.parent.win, self.y, self.x, 32, self.width, battr)
        ### label bg code ********************************************
        #self.parent.win.attron(battr)
        ##for l in range (0, self.height):
        #self.parent.win.hline(self.y, self.x, 32, self.width)
        #self.parent.win.attroff(battr)
        ### **********************************************************

        self.parent.win.addstr(self.y, self.x, self.label, attr)

        self.parent.changed = True

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

    #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

    def readMessage(self, msg):
        """ checks if it is message recvr, executes msg contents if it is """

        if msg == None:                                                  return
        
        if msg["msg_status"] == "unread":
            if msg["recv_layer"] == "screen" or msg["recv_layer"] == "self":
                if msg["on_recv"] == "call_function":

                    func = getattr(self, msg["recv_act"])
                    if msg["recv_args"] == None:  
                        msg["ret_info"] = func()
                    else:        
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

    def getUserString(self, format_str, ch_attr, str_out_win, 
        info_out_panel, out_yx, min_len, max_len, echo_mode, pw_mode, cleanup):
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
        input_win       = self.globals["input_win"]
        info_out_txtbox = info_out_panel.textbox
        key_action_map  = self.parent.parent.key_action_map

        input_length    = 0
        input_error     = False

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
            status = self.checkChar(format_str, input_i, input_length, min_len)   
                      
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
            
            str_out_win.refresh() 

            if input_length == max_len:                      status = "OK_DONE"     
            if status != "OK":                                            break 

        if info_out_panel != None:
            if status != "OK_DONE":           info_out_txtbox.resetText(status)
            else:                         info_out_txtbox.resetText(output_str)

            info_out_txtbox.drawText()
            info_out_panel.win.refresh()

        if cleanup == True:
            str_out_win.hline(y, x, orig_bg_ch, max_len)
            str_out_win.refresh()

        return output_str
    
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
            status = self.validate(format_str, input_i)    
        return status

    # format string: [alpha][digit][whitespace][punctuation]
    def validate(self, format, input_i):
        
        if format[0] == False:
            if curses.ascii.isalpha(input_i) != False:
                return "ERR_ALPHA"
        if format[1] == False:
            if curses.ascii.isdigit(input_i) != False:
                return "ERR_DIGIT"
        if format[2] == False:
            if curses.ascii.isspace(input_i) != False:
                return "ERR_SPACE"
        if format[3] == False:
            if curses.ascii.ispunct(input_i) != False:
                return "ERR_PUNCT"         
        return "OK"