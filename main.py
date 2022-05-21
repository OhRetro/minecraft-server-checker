#Minecraft Server Checker
_version = ["2.1.3", "Stable", 213]

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
    from requests import json as re_json

#Minecraft Server Checker
class MinecraftServerChecker(QWidget):
    def __init__(self):
        super().__init__()
        gui = uic.loadUi("./main.ui", self)
        gui.Version_text.setText(f"v{_version[0]}")
        
        format_code = ["§4", "§c", "§6", "§e", "§2", "§a", "§b", "§3", "§1", "§9", "§5", "§7", "§8", "§d", "§f", "§0", "§k", "§l", "§m", "§n", "§o", "§r"]

        #Check Server
        def check_server():
            try:
                if server_ip := gui.ServerIP_display.text():
                    PyQt.settext(gui, Check_button="Refresh")

                    server = JavaServer.lookup(server_ip)
                    status = server.status()
                    
                    status_desc = str(status.description)
                    for _ in format_code:
                        status_desc = str(status_desc).replace(_, "")
                    status_desc = status_desc.replace("  ", "")

                    PyQt.settext(
                        gui,
                        Check_button="Refresh",
                        Status_display="Online",
                        Players_display=f"{status.players.online}/{status.players.max}",
                        Ping_display=f"{round(status.latency)} ms",
                        ServerSoftware_display=str(status.version.name),
                        ServerMOTD_display=status_desc)

                else:
                    reset()
                    PyQt.displaymessage(
                        title="Server IP field Empty", 
                        message="The Server IP field is empty",
                        icon=Icon.Information)

            #No Response
            except NoResponse:
                reset()
                PyQt.settext(
                    gui, 
                    Check_button="Refresh",
                    Status_display="Offline")

            #Invalid IP Address
            except InvalidMinecraftServerIp:
                reset()
                PyQt.displaymessage(
                    title="Invalid Minecraft Server IP",
                    message="The Server IP wasn't a Minecraft Server IP or was Invalid.",
                    icon=Icon.Information)

            #Connection Refused
            except ConnectionRefusedError:
                reset()
                PyQt.displaymessage(
                    title="Connection Refused",
                    message="The connection have been refused by the server.",
                    icon=Icon.Information)

            #Others
            except Exception as error:
                reset()
                PyQt.displaymessage(title="Error",
                                     message="An error has occurred",
                                     detailed_message=str(error),
                                     icon=Icon.Warning)

        #Reset
        def reset():
            PyQt.settext(
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
        self.checkupdates()

    #About
    def about(self):
        response = PyQt.displaymessage(
            title="Created by OhRetro",
            message=f"Minecraft Version Checker v{_version[0]} | {_version[1]} | Version Code: {_version[2]}", 
            informative_message="Do you want to open the program's repository on github?",
            icon=Icon.Question,
            buttons= (Button.Yes | Button.No))

        if response == Button.Yes:
            wb_open("https://github.com/OhRetro/Minecraft-Server-Checker")

    #Check for updates
    def checkupdates(self):
        latest_version =  int(re_json("https://api.github.com/repos/OhRetro/Minecraft-Server-Checker/releases/latest")["tag_name"].replace("v", "").replace(".", ""))
        
        if _version[2] < latest_version:
            response = PyQt.displaymessage(
                title="Update Available",
                message="An update is available, do you want to download it?",
                informative_message="You can download it from the program's repository on github.",
                icon=Icon.Information,
                buttons= (Button.Yes | Button.No))

            if response == Button.Yes:
                wb_open("https://github.com/OhRetro/Minecraft-Server-Checker/releases/latest")
        
        
if __name__ == "__main__":
    try:
        app = QApplication(sys_argv)
        window = MinecraftServerChecker()
        app.exec()
        
    except Exception as error:
        PyQt.displaymessage(title="Error", 
                             message="An error has occurred", 
                             informative_message="Something went wrong", 
                             detailed_message=str(error), 
                             icon=Icon.Critical)