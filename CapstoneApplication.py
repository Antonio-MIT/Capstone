import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QListWidget, QStackedWidget, QLabel, 
    QStatusBar
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hydrogen Line Tracker")
        self.setMinimumSize(1200, 700)

        # --- Main Layout ---
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # --- Sidebar ---
        self.sidebar = QListWidget()
        self.sidebar.addItems([
            "Dashboard",
            "Tracking",
            "Observation Windows",
            "Logs",
            "Settings"
        ])
        self.sidebar.setFixedWidth(200)
        self.sidebar.currentRowChanged.connect(self.switch_panel)

        # --- Central Panels ---
        self.stack = QStackedWidget()
        self.stack.addWidget(self.make_panel("Dashboard"))
        self.stack.addWidget(self.make_panel("Tracking"))
        self.stack.addWidget(self.make_panel("Observation Windows"))
        self.stack.addWidget(self.make_panel("Logs"))
        self.stack.addWidget(self.make_panel("Settings"))

        # Add to layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

        # --- Status Bar ---
        status = QStatusBar()
        status.showMessage("Ready")
        self.setStatusBar(status)

        self.setCentralWidget(main_widget)

    def make_panel(self, name):
        """Creates a placeholder panel."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel(f"{name} Panel")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return widget

    def switch_panel(self, index):
        self.stack.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
