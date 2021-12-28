#Minecraft Server Checker
_version = "3.0"

try:
    from mcstatus import MinecraftServer
    from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
    from PyQt5 import uic
    from socket import gaierror as InvalidMinecraftServerIp, timeout as NoResponse
    import sys
    import webbrowser
    
except ImportError as missing_package:
    missing_package = str(missing_package).replace("No module named ", "")
    print(f"{missing_package} is missing.\nPlease install {missing_package}.\n")
    exit(0)

#-------------------------------------------------------------------------------
#Minecraft Server Checker-------------------------------------------------------
class MinecraftServerChecker(QWidget):
    def __init__(self):
        super().__init__()
        gui = uic.loadUi("files/main.ui", self)
        gui.Version_text.setText(f"v{_version}")

        #Check It Up
        def check_it_up():
            try:
                server_ip = gui.ServerIP_display.text()

                if not server_ip:
                    reset()
                    error_message = QMessageBox()
                    error_message.setWindowTitle("Server IP Empty")
                    error_message.setText("The Server IP field was empty.")
                    error_message.exec_()
                    return

                else:
                    gui.Check_button.setText("Refresh")
                    server = MinecraftServer.lookup(server_ip)
                    status = server.status()
                    gui.Status_display.setText("Online")
                    gui.Players_display.setText(f"{status.players.online}/{status.players.max}")
                    gui.Ping_display.setText(f"{round(status.latency)} ms")
                    gui.ServerSoftware_display.setText(str(status.version.name))
                    gui.ServerMOTD_display.setText(str(status.description))

            except NoResponse:
                reset()
                gui.Check_button.setText("Refresh")
                gui.Status_display.setText("Offline")

            except InvalidMinecraftServerIp:
                reset()
                error_message = QMessageBox()
                error_message.setWindowTitle("Invalid Minecraft Server IP")
                error_message.setText("The Server IP wasn't a Minecraft Server IP.")
                error_message.exec_()
                return

            except ConnectionRefusedError:
                reset()
                error_message = QMessageBox()
                error_message.setWindowTitle("Connection Refused")
                error_message.setText("The connection have been refused by the server.")
                error_message.exec_()
                return

        #Reset
        def reset():
            gui.Check_button.setText("Check")
            gui.Status_display.setText("")
            gui.Players_display.setText("")
            gui.Ping_display.setText("")
            gui.ServerSoftware_display.setText("")
            gui.ServerMOTD_display.setText("")

        #About
        def about():
            about = QMessageBox()
            about.setWindowTitle("Created by OhRetro_")
            about.setText(f"Minecraft Version Checker v{_version}\nDo you want to open the program's repository on github?")
            about.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            openlink = about.exec_()

            if openlink == QMessageBox.Yes:
                webbrowser.open("https://github.com/OhRetro/Minecraft-Server-Checker")

        gui.Check_button.clicked.connect(check_it_up)
        gui.MinecraftLogo_button.clicked.connect(about)

        gui.show()

#-------------------------------------------------------------------------------
#Run----------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinecraftServerChecker()
    app.exec()
