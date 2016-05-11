#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pykeyboard import PyKeyboard
from pymouse import PyMouse
from time import sleep
import gtk
import wnck
import sys
import unittest
from Xlib import X
from Xlib.display import Display
from movieconfig import *

if 2 == sys.version_info.major:
    import ConfigParser as configparser
else:
    import configparser

defaultconponentxy = "conponentxy.ini"

k = PyKeyboard()
m = PyMouse()
waittime = 30
debug = True

def log(str):
    if True == debug:
        print(str)

def parserxy(str):
    tempstr = str
    for i in ('(', ')', ','):
        tempstr = tempstr.replace(i, ' ')

    return tempstr.split()

class ConponentXY(object):
    def __init__(self):
        self.conponentxy = configparser.ConfigParser()
        self.conponentxy.read(defaultconponentxy)

        # 深度影院窗口名称
        self.wmname = "深度影院"
        # 设置窗口名称
        self.setting_wmname = "Deepin Movie"

        # 深度影院窗口坐标
        self.deepinmovie = "deepin-movie"

        # 设置窗口坐标
        self.deepinmoviesetting = "deepin-movie-setting"

        # 通用属性名称
        self.base = "base"

        # 深度影院下拉菜单名称
        self.submenu = "submenu"

        # 深度影院下拉菜单中的名称
        self.submenu_set = "submenu_set"

        # setting -> player
        self.submenu_set_player = "player"
        self.submenu_set_player_fullscreenOnOpenFile = "fullscreenOnOpenFile"

    def setDeepinMovieBase(self, xy):
        log("base: "),
        log(xy)
        self.conponentxy.set(self.deepinmovie, self.base, xy)

    def setDeepinMovieSettingBase(self, xy):
        log("setting base:"),
        log(xy)
        self.conponentxy.set(self.deepinmoviesetting, self.base, xy)

    def getDeepinMovieXY(self, key):
        xystr = str(self.conponentxy.get(self.deepinmovie, key))
        xy = parserxy(xystr)

        if self.base != key:
            basexystr = str(self.conponentxy.get(self.deepinmovie, self.base))
            basexy = parserxy(basexystr)
            listxy = []
            listxy.append(int(basexy[0]) + int(basexy[2]) - int(xy[0]))
            listxy.append(int(basexy[1]) + int(xy[1]))
            return tuple(listxy)
        else:
            return tuple(xy)

    def getDeepinMovieSettingXY(self, key):
        xystr = str(self.conponentxy.get(self.deepinmoviesetting, key))
        xy = parserxy(xystr)

        if self.base != key:
            basexystr = str(self.conponentxy.get(self.deepinmoviesetting, self.base))
            basexy = parserxy(basexystr)
            listxy = []
            listxy.append(int(basexy[0]) + int(xy[0]))
            listxy.append(int(basexy[1]) + int(xy[1]))
            return tuple(listxy)
        else:
            return tuple(xy)

    def clickDeepinMovie(self, conponent):
        xy = self.getDeepinMovieXY(conponent)
        log("click: " + str(xy))
        mouseClickL(xy[0], xy[1])

    def clickDeepinMovieSetting(self, conponent):
        xy = self.getDeepinMovieSettingXY(conponent)
        log("click: " + str(xy))
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
            log(xy)
            conponentxy.setDeepinMovieBase(tuple(listxy[0:4]))
            return True

    return False

def saveDeepinMovieSettingBase():
    screen = wnck.screen_get_default()
    while gtk.events_pending():
        gtk.main_iteration()

    for window in screen.get_windows():
        name = window.get_name()
        if conponentxy.setting_wmname == name:
            xy = window.get_client_window_geometry()
            listxy = list(xy)
            log(xy)
            conponentxy.setDeepinMovieSettingBase(tuple(listxy[0:4]))
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
                log("MapNotify")
                if saveDeepinMovieBase():
                    break

keySingle(k.windows_l_key)
keyTypeStr(conponentxy.deepinmovie)
keySingle(k.enter_key)
Waitter(Display()).loop()

conponentxy.clickDeepinMovie(conponentxy.submenu)
conponentxy.clickDeepinMovie(conponentxy.submenu_set)
saveDeepinMovieSettingBase()

conponentxy.clickDeepinMovieSetting(conponentxy.submenu_set_player)
conponentxy.clickDeepinMovieSetting(conponentxy.submenu_set_player_fullscreenOnOpenFile)

class testDeepinMovie(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.movieconfig = movieConfig()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSettingfullscreenOnOpenFile(self):
        v = self.movieconfig.getPlayer(self.movieconfig.player_fullscreenOnOpenFile)
        self.assertEqual(stringtobool(v), True)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(testDeepinMovie("testSettingfullscreenOnOpenFile"))
    return suite

if __name__ == "__main__":
    unittest.main(defaultTest = 'suite')


