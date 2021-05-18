#Minecraft Server Checker
#Versão:1.3

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
import webbrowser
import ctypes
import time

#-------------------------------------------------------------------------------
#Minecraft Server Checker-------------------------------------------------------
class MinecraftServerChecker(QWidget):
    def __init__(self):
        super().__init__()
        gui = uic.loadUi('files/main.ui', self)

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
                error.setWindowTitle('Invalid Minecraft Server IP')
                error.setText("The Server IP wasn't a Minecraft Server IP.")
                error.exec_()

            except ConnectionRefusedError:
                reset()
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
#About--------------------------------------------------------------------------
        def about():
            about = QMessageBox()
            about.setWindowTitle('Created by OhRetro_')
            about.setText("Minecraft Version Checker v1.3\ndo you want do open the program's repository on github?")
            about.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            openlink = about.exec_()

            if openlink == QMessageBox.Yes:
                webbrowser.open('https://github.com/OhRetro/Minecraft-Server-Checker')
            else:
                pass

#-------------------------------------------------------------------------------
#Minecraft Server Checker-------------------------------------------------------
        gui.Check_button.clicked.connect(checkit)
        gui.MinecraftLogo_button.clicked.connect(about)

        gui.show()

#-------------------------------------------------------------------------------
#Run----------------------------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MinecraftServerChecker()
    app.exec()
