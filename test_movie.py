#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pykeyboard import PyKeyboard
from pymouse import PyMouse
from time import sleep
import gtk
import wnck
import sys
from Xlib import X
from Xlib.display import Display

if 2 == sys.version_info.major:
    import ConfigParser as configparser
else:
    import configparser

defaultconponentxy = "conponentxy.ini"

k = PyKeyboard()
m = PyMouse()
waittime = 30

def parserxy(str):
    tempstr = str
    for i in ('(', ')', ','):
        tempstr = tempstr.replace(i, ' ')

    return tempstr.split()

class ConponentXY(object):
    def __init__(self):
        self.conponentxy = configparser.ConfigParser()
        self.conponentxy.read(defaultconponentxy)
        self.wmname = "深度影院"
        self.deepinmovie = "deepin-movie"
        self.base = "base"
        self.submenu = "submenu"
        self.submenu_set = "submenu_set"

    def setDeepinMovieBase(self, xy):
        print("base: "),
        print(xy)
        self.conponentxy.set(self.deepinmovie, self.base, xy)

    def getDeepinMovieXY(self, key):
        xystr = str(self.conponentxy.get(self.deepinmovie, key))
        xy = parserxy(xystr)

        if self.base != key:
            basexystr = str(self.conponentxy.get(self.deepinmovie, self.base))
            basexy = parserxy(basexystr)
            listxy = []
            listxy.append(int(xy[0]) + int(basexy[0]))
            listxy.append(int(xy[1]) + int(basexy[1]))
            return tuple(listxy)
        else:
            return tuple(xy)

    def clickDeepinMovie(self, conponent):
        xy = self.getDeepinMovieXY(conponent)
        print("click: " + str(xy))
        mouseClickL(xy[0], xy[1])

conponentxy = ConponentXY()

def keySingle(key):
    k.press_key(key)
    k.release_key(key)
    sleep(2)

def keyTypeStr(str):
    k.type_string(str)
    sleep(2)

def mouseClickL(x, y):
    m.move(x, y)
    m.move(x-1, y-1)
    m.move(x+1, y+1)
    m.move(x, y)
    sleep(2)
    m.click(x, y)
    sleep(2)

def saveDeepinMovieBase():
    screen = wnck.screen_get_default()
    while gtk.events_pending():
        gtk.main_iteration()

    for window in screen.get_windows():
        name = window.get_name()
        if conponentxy.wmname == name:
            xy = window.get_client_window_geometry()
            listxy = list(xy)
            print(xy)
            conponentxy.setDeepinMovieBase(tuple(listxy[0:2]))
            return True

    return False

class Waitter(object):
    def __init__(self, display):
        self.display = display
        self.root = self.display.screen().root
        self.root.change_attributes(event_mask = X.SubstructureNotifyMask)

    def loop(self):
        while True:
            ev = self.display.next_event()
            if ev.type == X.CreateNotify:
                pass

            if ev.type == X.MapNotify:
                if saveDeepinMovieBase():
                    break

keySingle(k.windows_l_key)
keyTypeStr(conponentxy.deepinmovie)
keySingle(k.enter_key)
Waitter(Display()).loop()

conponentxy.clickDeepinMovie(conponentxy.submenu)
conponentxy.clickDeepinMovie(conponentxy.submenu_set)
