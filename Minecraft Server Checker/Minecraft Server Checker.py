#Minecraft Server Checker
#Versão:1.0

from mcstatus import MinecraftServer
import os
import os.path
import ctypes
import time

ctypes.windll.kernel32.SetConsoleTitleW('Minecraft Server Checker')

print('=======================================================================')
ip = input('SERVER IP: ')
server = MinecraftServer.lookup(ip)
status = server.status()
print('PLAYERS ONLINE: ' + str(status.players.online) + ' / ' + str(status.players.max))
print('PING: ' + str(status.latency) + 'ms')
print('SERVER VERSION: ' + str(status.version.name).replace('Requires', ''))
print('')
print('Press "Enter" to close the program.')
print('=======================================================================')
input()
