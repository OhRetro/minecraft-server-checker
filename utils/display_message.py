from utils.pyqt5 import displaymessage as oup_displaymessage
from utils.pyqt5 import Icon as oup_Icon, Button as oup_Button

def critical_auto_update(title:str, message:str, detailed:str):
    oup_displaymessage(
        title=title, 
        message=message,
        informative="\"Auto Update\" has been deactivated.\nYou can activate it again by clicking the \"Auto Update\" button.", 
        detailed=detailed, 
        icon=oup_Icon["Critical"],
        buttons=(oup_Button["Ok"]),
        windowicon="./mc_icon.png"
    )