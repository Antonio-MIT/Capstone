import sys
from PySide6.QtWidgets import QApplication
from TrackerUI import TrackingPanel
from GUI import MainWindow   # your main window class

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
