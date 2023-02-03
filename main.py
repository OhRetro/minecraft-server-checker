from sys import argv as sys_argv
from socket import gaierror as InvalidMinecraftServerIp
from socket import timeout as NoResponse
from webbrowser import open as wb_open
from traceback import format_exc as tb_format_exc
from time import sleep as t_sleep
from threading import Thread as th_Thread

try:
    from rich import print
    from mcstatus import JavaServer
    from PyQt5 import uic
    from PyQt5.QtWidgets import QApplication, QWidget
    from pyqt5_utils import displaymessage as oup_displaymessage, settext as oup_settext
    from pyqt5_utils import bindbutton as oup_bindbutton, Icon as oup_Icon, Button as oup_Button

except ImportError:
    print(tb_format_exc())
    print("[!] Please try running \"pip install -r requirements.txt\"")
    exit(1)

version = "2.2.1"
format_code = ["§4", "§c", "§6", "§e", "§2", "§a", "§b", "§3", "§1", "§9", "§5", "§7", "§8", "§d", "§f", "§0", "§k", "§l", "§m", "§n", "§o", "§r", "§"]

class MCServerChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.gui = uic.loadUi("./main.ui", self)
        oup_settext(
            self.gui,
            Version_TEXT=f"v{version}")

        self.autoupdate_thread = self.generate_thread()
        self.autoupdate_thread.daemon = True
        self.thread_running = False
        
        oup_bindbutton(self.gui, "Check_BUTTON", self.checkserver)
        oup_bindbutton(self.gui, "About_BUTTON", self.about)        

        self.gui.show()
            
    #Generate a new thread for autoping
    def generate_thread(self):
        return th_Thread(target=self.autoupdate)

    #Auto Update
    def autoupdate(self):
        global format_code
        oup_settext(
            self.gui,
            Players_TEXT="Players: (AUTO-UPDATING)",
            Ping_TEXT="Ping: (AUTO-UPDATING)",
            MOTD_TEXT="MOTD: (AUTO-UPDATING)",
            )
        try:
            for _ in range(9999999):
                if not self.thread_running: 
                    break
                server = JavaServer.lookup(self.server_ip)
                status = server.status()

                status_desc = str(status.description)
                for _ in format_code:
                    status_desc = str(status_desc).replace(_, "")
                status_desc = status_desc.replace("  ", "")

                oup_settext(
                    self.gui,
                    Players_DISPLAY=f"{status.players.online}/{status.players.max}",
                    Ping_DISPLAY=f"{round(status.latency)} ms",
                    MOTD_DISPLAY=status_desc)
                    
                t_sleep(1)
                
        except TimeoutError:
            oup_displaymessage(
                title="Timeout Error", 
                message="A Timeout Error Occured, It's happened because of the server's latency.\nNo need to worry, it's not your fault.",
                informative="\"Auto Update\" has been deactivated.\nYou can activate it again by clicking the \"Auto Update\" button.", 
                detailed=tb_format_exc(), 
                icon=oup_Icon["Critical"],
                buttons=(oup_Button["Ok"]),
                windowicon="./mc_icon.png"
                )
            self.gui.AutoUpdate_TOGGLE.setChecked(False)
            self.thread_running = False
            
        except Exception:
            print(tb_format_exc())
            oup_displaymessage(
                title="Something went wrong", 
                message="Something else went wrong.",
                informative="\"Auto Update\" has been deactivated.\nYou can activate it again by clicking the \"Auto Update\" button.", 
                detailed=tb_format_exc(),
                icon=oup_Icon["Critical"],
                buttons=(oup_Button["Ok"]),
                windowicon="./mc_icon.png"
                )
            self.gui.AutoUpdate_TOGGLE.setChecked(False)
            self.thread_running = False
            
        oup_settext(
            self.gui,
            Players_TEXT="Players:",
            Ping_TEXT="Ping:",
            MOTD_TEXT="MOTD:",
            )
                    
    #Check Server
    def checkserver(self):
        autoupdate_enabled = self.gui.AutoUpdate_TOGGLE.isChecked()
        try:
            self.server_ip = self.gui.IP_DISPLAY.text()
            
            if not self.server_ip:
                self.reset()
                oup_displaymessage(
                    title="Server IP field Empty", 
                    message="The Server IP field is empty",
                    icon=oup_Icon["Information"],
                    windowicon="./mc_icon.png")
                
            oup_settext(self.gui, Check_BUTTON="Refresh")

            server = JavaServer.lookup(self.server_ip)
            status = server.status()
            
            status_desc = status.description.replace("  ", "")
            for _ in format_code:
                status_desc = status_desc.replace(_, "")

            oup_settext(
                self.gui,
                Check_BUTTON="Refresh",
                Status_DISPLAY="Online",
                Players_DISPLAY=f"{status.players.online}/{status.players.max}",
                Ping_DISPLAY=f"{round(status.latency)} ms",
                Software_DISPLAY=str(status.version.name),
                MOTD_DISPLAY=status_desc)
            
            if autoupdate_enabled and not self.thread_running:
                self.thread_running = True
                self.autoupdate_thread.start()
                
            elif not autoupdate_enabled and self.thread_running:
                self.thread_running = False
                self.autoupdate_thread.join(0.5)
                self.autoupdate_thread = self.generate_thread()
                self.autoupdate_thread.daemon = True

        #No Response
        except NoResponse:
            self.reset()
            oup_settext(
                self.gui, 
                Check_BUTTON="Refresh",
                Status_DISPLAY="Offline")

        #Invalid IP Address
        except InvalidMinecraftServerIp:
            self.reset()
            oup_displaymessage(
                title="Invalid Minecraft Server IP",
                message="The Server IP wasn't a Minecraft Server IP or was Invalid.",
                icon=oup_Icon["Information"],
                windowicon="./mc_icon.png")

        #Connection Refused
        except ConnectionRefusedError:
            self.reset()
            oup_displaymessage(
                title="Connection Refused",
                message="The connection have been refused by the server.",
                icon=oup_Icon["Information"],
                windowicon="./mc_icon.png")

        #Others
        except Exception as error:
            self.reset()
            oup_displaymessage(
                title="Error",
                message="An error has occurred; Click on the 'Show Details' button to see more details.",
                informative=f"\"{error}\"",
                detailed=tb_format_exc(),
                icon=oup_Icon["Warning"],
                windowicon="./mc_icon.png")
        
    #Reset
    def reset(self):
        oup_settext(
            self.gui,
            Check_BUTTON="Check",
            Status_DISPLAY="",
            Players_DISPLAY="",
            Ping_DISPLAY="",
            Software_DISPLAY="",
            MOTD_DISPLAY="")
            
    #About
    def about(self):
        response = oup_displaymessage(
            title="About Minecraft Server Checker",
            message=f"Minecraft Server Checker v{version}; Created by OhRetro", 
            informative="Do you want to open the program's repository on github?",
            icon=oup_Icon["Question"],
            buttons= (oup_Button["Yes"] | oup_Button["No"]),
            windowicon="./mc_icon.png",
            )

        if response == oup_Button["Yes"]:
            wb_open("https://github.com/OhRetro/Minecraft-Server-Checker")
            
if __name__ == "__main__":
    try:
        app = QApplication(sys_argv)
        window = MCServerChecker()
        app.exec()
        exit(0)
        
    except Exception:
        print(tb_format_exc())
        exit(2)
