#
# Plugin for BigBrotherBot(B3) (www.bigbrotherbot.com)
# Copyright (C) 2005 www.xlr8or.com
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA    02110-1301    USA
#
# Changelog:
#

__version__ = '1.0.0'
__author__    = 'xlr8or'

import b3
import b3.events

#--------------------------------------------------------------------------------------------------
class Bfbc2MixedgamesPlugin(b3.plugin.Plugin):
    _rotation = []
    _rotLength = 0
    _curMapId = 0

    def onStartup(self):
        """\
        Initialize plugin settings
        """
        # Register our events
        self.verbose('Registering events')
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)
        self.rotateMap()
        self.debug('Started')


    def onLoadConfig(self):
        # load our settings
        self.verbose('Loading config')
        # load the rotation from file
        _r = self.config.get('settings', 'rotation').split(',')
        for i in _r:
            self._rotation.append(i.strip().split())
        self.verbose('Loaded Rotation: %s' % self._rotation)


    def onEvent(self, event):
        """\
        Handle intercepted events
        """
        if event.type == b3.events.EVT_GAME_ROUND_START:
            self.rotateMap()
        else:
            self.dumpEvent(event)

    def dumpEvent(self, event):
        self.debug('bfbc2mixedgames.dumpEvent -- Type %s, Client %s, Target %s, Data %s',
            event.type, event.client, event.target, event.data)

#--------------------------------------------------------------------------------------------------

    def rotateMap(self):
        if self._curMapId >= len(self._rotation):
            # mapcycle complete, start at first map again
            self._curMapId = 0

        # self._rotation = [['sqdm', 'map1', '2'], ['dm', 'mapdm', '1']]
        if self._rotation[self._curMapId][2] < self.console.game.g_maxrounds:
            # not yet reached the set number of rounds
            return None

        # prepare the next map
        _nextMapId = self._curMapId + 1
        _nextGameType = self._rotation[_nextMapId][0]
        _nextMap = 'Levels/' + str(self._rotation[_nextMapId][1])
        _nextNrRounds = self._rotation[_nextMapId][2]
        if not _nextNrRounds:
            _nextNrRounds = 2
        # send the changes to the server
        self.debug('Rotating Map, setting GameType: %s, Map: %s, Rounds: %s' %(_nextGameType, _nextMap, _nextNrRounds))
        self._changeMode(_nextGameType)
        self.console.write(('mapList.clear', ))
        self.console.write(('mapList.append', _nextMap, _nextNrRounds))


    def _changeMode(self, mode=None):
        if mode is None:
            self.error('mode cannot be None')
        elif mode not in ('CONQUEST', 'RUSH', 'SQDM', 'SQRUSH'):
            self.error('invalid game mode %s' % mode)
        else:
            try:
                self.console.write(('admin.setPlaylist', mode))
            except Bfbc2CommandFailedError, err:
                self.error('Failed to change game mode. Server replied with: %s' % err)

#--------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    print '\nThis is version '+__version__+' by '+__author__+' for BigBrotherBot.\n'
