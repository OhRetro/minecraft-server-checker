#!/usr/bin/python3
#Minecraft Server Checker
_version = "2.1.2"

#Imports
try:
    import webbrowser
    from mcstatus import MinecraftServer
    from oreto_utils import PyQt
    from PyQt5 import uic
    from PyQt5.QtWidgets import QApplication, QWidget
    
    Icon = PyQt.Icon
    Button = PyQt.Button

except ImportError as missing_package:
    missing_package = str(missing_package).replace("No module named ", "")
    print(f"{missing_package} is missing.\nPlease install {missing_package}.\n")
    exit(0)

finally:
    import sys
    from socket import gaierror as InvalidMinecraftServerIp
    from socket import timeout as NoResponse

#Minecraft Server Checker
class MinecraftServerChecker(QWidget):
    def __init__(self):
        super().__init__()
        gui = uic.loadUi("./main.ui", self)
        gui.Version_text.setText(f"v{_version}")

        #Check Server
        def check_server():
            try:
                if server_ip := gui.ServerIP_display.text():
                    PyQt.set_text(gui, Check_button="Refresh")

                    server = MinecraftServer.lookup(server_ip)
                    status = server.status()

                    PyQt.set_text(
                        gui,
                        Check_button="Refresh",
                        Status_display="Online",
                        Players_display=f"{status.players.online}/{status.players.max}",
                        Ping_display=f"{round(status.latency)} ms",
                        ServerSoftware_display=str(status.version.name),
                        ServerMOTD_display=str(status.description))

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
                PyQt.display_message("Error", "An error has occurred", detailed_message=str(error), icon=Icon.Warning)

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
            message=f"Minecraft Version Checker v{_version}\nDo you want to open the program's repository on github?",
            icon=Icon.Question,
            buttons= (Button.Yes | Button.No))

        if chosen_response == Button.Yes:
            webbrowser.open("https://github.com/OhRetro/Minecraft-Server-Checker")

#Run
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MinecraftServerChecker() 
        
    except Exception as error:
        PyQt.display_message("Error", "An error has occurred", "Something went wrong", str(error), Icon.Critical)

    finally:
        app.exec()