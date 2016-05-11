#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
if 2 == sys.version_info.major:
    import ConfigParser as configparser
else:
    import configparser

def stringtobool(str):
    if 'False' == str:
        return False
    elif 'True' == str:
        return True
    else:
        return None

class movieConfig(object):
    def __init__(self):
        self.defaultpath = os.path.expanduser("~/.config/deepin-movie/config.ini")
        self.params_config = configparser.ConfigParser()
        self.params_config.read(self.defaultpath)

        # Player
        self.player_volume = "volume"
        self.player_muted  = "muted"
        self.player_fullscreenOnOpenFile = "fullscreenOnOpenFile"

        # HotkeysPlay
        self.hotkeysplay_hotkeyEnabled = "hotkeyEnabled"
        self.hotkeysplay_togglePlay    = "togglePlay"
    
        # default value
        self.default_player_fullscreenOnOpenFile = False

    def getPlayer(self, key):
        section = "Player"
        self.params_config.read(self.defaultpath)
        return self.params_config.get(section, key)

    def getHotkeysPlay(self, key):
        section = "HotkeysPlay"
        self.params_config.read(self.defaultpath)
        return self.params_config.get(section, key)


