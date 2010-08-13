###################################################################################
#
# Bfbc2Mixedgames
# Plugin for B3 (www.bigbrotherbot.com)
# (c) 2010 www.xlr8or.com (mailto:xlr8or@xlr8or.com)
#
# This program is free software and licensed under the terms of
# the GNU General Public License (GPL), version 2.
#
# http://www.gnu.org/copyleft/gpl.html
###################################################################################

Bfbc2 Mixed GameTypes Plugin for B3
###################################################################################

This plugin works for BattleField Bad Company 2 only! 

This plugin will take control of your maplist. You will be able to create
a maplist in the plugin config containing multiple gametypes. Just look at the
config in this package to see how you can set the maprotation.

Requirements:
###################################################################################

- Bad Company 2 Gameserver
- B3 version 1.3.4 or higher


Installation:
###################################################################################

1. Unzip the contents of this package into your B3 folder. It will
place the .py file in b3/extplugins and the config file .xml in
your b3/extplugins/conf folder.

2. Open the .xml file with your favorit editor and modify the
rotation just like the example.

3. Open your B3.xml file (in b3/conf) and add the next line in the
<plugins> section of the file:

<plugin name="bfbc2mixedgames" config="@b3/extplugins/conf/bfbc2mixedgames.xml"/>


Changelog
###################################################################################
v1.0.0         : Initial release


###################################################################################
xlr8or - 13 aug 2010 - www.bigbrotherbot.net // www.xlr8or.com