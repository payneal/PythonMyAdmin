#!/usr/bin/env python
import curses

scr = curses.initscr()
scr.keypad(0)
curses.noecho()

scr.addstr("hello world")
scr.refresh()
scr.getch()

curses.endwin()

