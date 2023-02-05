#PyQt5

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

__all__ = ["displaymessage", "bindbutton", "settext", "gettext", "getelements"]

Icon = {
    "Question": QMessageBox.Question, 
    "Information": QMessageBox.Information, 
    "Warning": QMessageBox.Warning, 
    "Critical": QMessageBox.Critical,}
    
Button = {
    "Ok": QMessageBox.Ok,
    "No": QMessageBox.No,
    "Yes": QMessageBox.Yes,
    "Cancel": QMessageBox.Cancel,
    "Close": QMessageBox.Close,
    "Abort": QMessageBox.Abort, 
    "Open": QMessageBox.Open, 
    "Ignore": QMessageBox.Ignore, 
    "Save": QMessageBox.Save, 
    "Retry": QMessageBox.Retry, 
    "Apply": QMessageBox.Apply, 
    "Help": QMessageBox.Help, 
    "Reset": QMessageBox.Reset, 
    "SaveAll": QMessageBox.SaveAll, 
    "YesToAll": QMessageBox.YesToAll, 
    "NoToAll": QMessageBox.NoToAll,}
    
#Display Message
def displaymessage(title:str, message:str, informative:str=None, detailed:str=None, icon:Icon=None, buttons:Button=None, windowicon=None) -> None:
    """
    It displays a message box with the given parameters.\n
    It can only be called inside a running QApplication.
    """
    display = QMessageBox()
    display.setWindowTitle(title)
    display.setText(message)
    if informative is not None: display.setInformativeText(informative)
    if detailed is not None: display.setDetailedText(detailed)
    if icon is not None: display.setIcon(icon)
    if buttons is not None: display.setStandardButtons(buttons)
    if windowicon is not None: display.setWindowIcon(QIcon(windowicon))
    return display.exec_()
    
def bindbutton(gui, button:str, function) -> None:
    getattr(gui, button).clicked.connect(function)

#Set Gui Element Text
def settext(gui, **element) -> None:
    for _ in element:  
        getattr(gui, _).setText(str(element[_]))
        
#Get Gui Element Text
def gettext(gui, element) -> str:
    return getattr(gui, element).text()

#Get Gui Elements
def getelements(gui) -> list:
    return [element.objectName() for element in gui.children()]