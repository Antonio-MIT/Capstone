import sys
#import PySide6
from PySide6.QtWidgets import QApplication
#from GUI import MainWindow
#import importlib
#import Tracker
#importlib.reload(Tracker)

from UI.GUI import MainWindow

##DEBUG
#print("PYTHON IMPORTED TRACKER FROM:", Tracker.__file__)
#print("PYTHON SEARCH PATH:", sys.path)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
