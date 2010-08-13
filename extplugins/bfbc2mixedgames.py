#
# Plugin for BigBrotherBot(B3) (www.bigbrotherbot.com)
# Copyright (C) 2010 www.xlr8or.com
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
__author__  = 'xlr8or'

import b3
import b3.events

#--------------------------------------------------------------------------------------------------
class Bfbc2MixedgamesPlugin(b3.plugin.Plugin):
    _rotation = []
    _rotLength = 0
    _curMapId = -1

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
        _nextMapId = self._curMapId + 1
        if _nextMapId >= len(self._rotation):
            # mapcycle complete, start at first map again
            _nextMapId = 0

        # self._rotation = [['SQDM', 'mp_008', '2'], ['CONQUEST', 'mp_002', '1']]
        # next paragraph is a workaround to get the proper current round number. This will be fixed in B3 version 1.3.4
        # that's when we can change to the commented code, saves a serverInfo() request. 
        """
        self.debug('CurRoundNr: %s, MaxRoundNrs: %s' %(self.console.game.rounds, self.console.game.g_maxrounds))
        if self.console.game.rounds < self.console.game.g_maxrounds:
            # not yet reached the set number of rounds
            self.debug('Not setting next map, rounds not completed.')
            return None
        """
        data = self.console.getServerInfo() 
        _curRound = data[5]
        _maxRounds = data[6]
        self.debug('CurRoundNr: %s, MaxRoundNrs: %s' %(_curRound, _maxRounds))
        if _curRound < _maxRounds:
            # not yet reached the set number of rounds
            self.debug('Not setting next map, rounds not completed.')
            return None

        # prepare the next map
        _nextGameType = self._rotation[_nextMapId][0]
        _nextMap = 'Levels/' + str(self._rotation[_nextMapId][1])
        if not self._rotation[_nextMapId][2]:
            _nextNrRounds = 2
        else:
            _nextNrRounds = self._rotation[_nextMapId][2]
        # send the changes to the server
        self.debug('Next Map: GameType: %s, Map: %s, Rounds: %s' %(_nextGameType, _nextMap, _nextNrRounds))
        self._changeMode(_nextGameType)
        self.console.write(('mapList.clear', ))
        self.console.write(('mapList.append', _nextMap, _nextNrRounds))
        self.console.write(('mapList.save', ))
        self._curMapId = _nextMapId


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
