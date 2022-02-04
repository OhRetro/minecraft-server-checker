#!/usr/bin/python3
#Minecraft Server Checker
_version = "2.1.1"

#Imports
try:
    from mcstatus import MinecraftServer
    from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
    from PyQt5 import uic
    import webbrowser
    
except ImportError as missing_package:
    missing_package = str(missing_package).replace("No module named ", "")
    print(f"{missing_package} is missing.\nPlease install {missing_package}.\n")
    exit(0)

finally:
    from socket import gaierror as InvalidMinecraftServerIp, timeout as NoResponse
    import sys

#Minecraft server Checker
class MinecraftServerChecker(QWidget):
    def __init__(self):
        super().__init__()
        gui = uic.loadUi("./main.ui", self)
        gui.Version_text.setText(f"v{_version}")

        #Check Server
        def check_server():
            try:
                if server_ip := gui.ServerIP_display.text():
                    set_gui_text("Refresh")
                    
                    server = MinecraftServer.lookup(server_ip)
                    status = server.status()
                    
                    set_gui_text(check_button="Refresh",
                                 status="Online",
                                 players=f"{status.players.online}/{status.players.max}",
                                 ping=f"{round(status.latency)} ms",
                                 server_software=str(status.version.name),
                                 server_motd=str(status.description)
                                 )

                else:
                    reset()
                    display_message("Server IP field Empty", "The Server IP field is empty")

            #No Response
            except NoResponse:
                reset()
                set_gui_text("Refresh", "Offline")

            #Invalid IP Address
            except InvalidMinecraftServerIp:
                reset()
                display_message("Invalid Minecraft Server IP", "The Server IP wasn't a Minecraft Server IP or was Invalid.")

            #Connection Refused
            except ConnectionRefusedError:
                reset()
                display_message("Connection Refused", "The connection have been refused by the server.")
                
        #Reset
        def reset():
            set_gui_text("Check")
            
        #Display Message
        def display_message(title:str, message:str, standard_buttons=None):
            display = QMessageBox()
            display.setWindowTitle(title)
            display.setText(message)

            if standard_buttons != None:
                display.setStandardButtons(standard_buttons)
                return display.exec_()
            else:   
                display.exec_()
                return

        #Set GUI Text
        def set_gui_text(check_button="", status="", players="", ping="", server_software="", server_motd=""):
            gui.Check_button.setText(check_button)
            gui.Status_display.setText(status)
            gui.Players_display.setText(players)
            gui.Ping_display.setText(ping)
            gui.ServerSoftware_display.setText(server_software)
            gui.ServerMOTD_display.setText(server_motd)

        #About
        def about():
            chosen_response = display_message("Created by OhRetro", 
                                              f"Minecraft Version Checker v{_version}\nDo you want to open the program's repository on github?", 
                                              QMessageBox.Yes | QMessageBox.No)

            if chosen_response == QMessageBox.Yes:
                webbrowser.open("https://github.com/OhRetro/Minecraft-Server-Checker")

        gui.Check_button.clicked.connect(check_server)
        gui.MinecraftLogo_button.clicked.connect(about)

        gui.show()

#Run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinecraftServerChecker()
    app.exec()
