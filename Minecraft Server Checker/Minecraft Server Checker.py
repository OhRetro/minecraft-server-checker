#Minecraft Server Checker
#Versão:1.2

from mcstatus import MinecraftServer
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QTextEdit, QLineEdit, QAction, QMessageBox
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime
from socket import *
import socket
import random, sys
import os
import os.path
import ctypes
import time

#-------------------------------------------------------------------------------
#Minecraft Server Checker-------------------------------------------------------
class MinecraftServerChecker(QWidget):
    def __init__(self):
        super().__init__()
        gui = uic.loadUi('files/main.ui', self)

        pixmap = QPixmap('files/Minecraft.png')
        gui.MinecraftLogo.setPixmap(pixmap)
        gui.MinecraftLogo.setScaledContents(True)

#-------------------------------------------------------------------------------
#CheckIt------------------------------------------------------------------------
        def checkit():
            try:
                ip = gui.ServerIP_display.text()

                if not ip:
                    reset()
                    error = QMessageBox()
                    error.setWindowTitle('Server IP Empty')
                    error.setText('The Server IP field was empty.')
                    error.exec_()
                    return

                gui.Check_button.setText('Refresh')
                server = MinecraftServer.lookup(ip)
                status = server.status()
                gui.Status_display.setText('Online')
                gui.Players_display.setText(str(status.players.online) + ' / ' + str(status.players.max))
                gui.Ping_display.setText(str(status.latency) + 'ms')
                gui.ServerSoftware_display.setText(str(status.version.name))
                gui.ServerMOTD_display.setText(str(status.description))

            #IP ERROR-----------------------------------------------------------
            except socket.timeout:
                reset()
                gui.Check_button.setText('Refresh')
                gui.Status_display.setText('Offline')

            except socket.gaierror:
                reset()
                error = QMessageBox()
                error.setWindowTitle('Invalid IP')
                error.setText('The Server IP was invalid.')
                error.exec_()

            except ConnectionRefusedError:
                reset()
                if 'localhost' in ip:
                    error = QMessageBox()
                    error.setWindowTitle('Cannot connect to localhost')
                    error.setText("You can't connect to localhost.")
                    error.exec_()

                else:
                    error = QMessageBox()
                    error.setWindowTitle('Connection Refused')
                    error.setText('The connection have been refused by the server.')
                    error.exec_()

#-------------------------------------------------------------------------------
#Reset--------------------------------------------------------------------------
        def reset():
            gui.Check_button.setText('Check')
            gui.Status_display.setText('')
            gui.Players_display.setText('')
            gui.Ping_display.setText('')
            gui.ServerSoftware_display.setText('')
            gui.ServerMOTD_display.setText('')

#-------------------------------------------------------------------------------
#Minecraft Server Checker-------------------------------------------------------
        gui.Check_button.clicked.connect(checkit)

        gui.show()

#-------------------------------------------------------------------------------
#Run----------------------------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MinecraftServerChecker()
    app.exec()
