#!/usr/bin/python3
#Minecraft Server Checker
_version = ["2.1.3", "Stable"]

#Imports
try:
    from mcstatus import JavaServer
    from oreto_utils import PyQt
    from PyQt5 import uic
    from PyQt5.QtWidgets import QApplication, QWidget
    
    Icon = PyQt.Icon
    Button = PyQt.Button

except ImportError as missing_package:
    print(missing_package)
    exit(1)

finally:
    from sys import argv as sys_argv
    from socket import gaierror as InvalidMinecraftServerIp
    from socket import timeout as NoResponse
    from webbrowser import open as wb_open

#Minecraft Server Checker
class MinecraftServerChecker(QWidget):
    def __init__(self):
        super().__init__()
        gui = uic.loadUi("./main.ui", self)
        gui.Version_text.setText(f"v{_version[0]} {_version[1]}")
        
        format_code = ["§4", "§c", "§6", "§e", "§2", "§a", "§b", "§3", "§1", "§9", "§5", "§7", "§8", "§d", "§f", "§0", "§k", "§l", "§m", "§n", "§o", "§r"]

        #Check Server
        def check_server():
            try:
                if server_ip := gui.ServerIP_display.text():
                    PyQt.set_text(gui, Check_button="Refresh")

                    server = JavaServer.lookup(server_ip)
                    status = server.status()
                    
                    status_desc = str(status.description)
                    for _ in format_code:
                        status_desc = str(status_desc).replace(_, "")
                    status_desc = status_desc.replace("  ", "")

                    PyQt.set_text(
                        gui,
                        Check_button="Refresh",
                        Status_display="Online",
                        Players_display=f"{status.players.online}/{status.players.max}",
                        Ping_display=f"{round(status.latency)} ms",
                        ServerSoftware_display=str(status.version.name),
                        ServerMOTD_display=status_desc)

                else:
                    reset()
                    PyQt.display_message(
                        title="Server IP field Empty", 
                        message="The Server IP field is empty",
                        icon=Icon.Information)

            #No Response
            except NoResponse:
                reset()
                PyQt.set_text(
                    gui, 
                    Check_button="Refresh",
                    Status_display="Offline")

            #Invalid IP Address
            except InvalidMinecraftServerIp:
                reset()
                PyQt.display_message(
                    title="Invalid Minecraft Server IP",
                    message="The Server IP wasn't a Minecraft Server IP or was Invalid.",
                    icon=Icon.Information)

            #Connection Refused
            except ConnectionRefusedError:
                reset()
                PyQt.display_message(
                    title="Connection Refused",
                    message="The connection have been refused by the server.",
                    icon=Icon.Information)

            #Others
            except Exception as error:
                reset()
                PyQt.display_message(title="Error",
                                     message="An error has occurred",
                                     detailed_message=str(error),
                                     icon=Icon.Warning)

        #Reset
        def reset():
            PyQt.set_text(
                gui,
                Check_button="Check",
                Status_display="",
                Players_display="",
                Ping_display="",
                ServerSoftware_display="",
                ServerMOTD_display="")

        gui.Check_button.clicked.connect(check_server)
        gui.MinecraftLogo_button.clicked.connect(self.about)

        gui.show()

    #About
    def about(self):
        chosen_response = PyQt.display_message(
            title="Created by OhRetro",
            message=f"Minecraft Version Checker v{_version[0]} {_version[1]}\nDo you want to open the program's repository on github?",
            icon=Icon.Question,
            buttons= (Button.Yes | Button.No))

        if chosen_response == Button.Yes:
            wb_open("https://github.com/OhRetro/Minecraft-Server-Checker")

if __name__ == "__main__":
    try:
        app = QApplication(sys_argv)
        window = MinecraftServerChecker()
        app.exec()
        
    except Exception as error:
        PyQt.display_message(title="Error", 
                             message="An error has occurred", 
                             informative_message="Something went wrong", 
                             detailed_message=str(error), 
                             icon=Icon.Critical)