from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from TrackerUI import TrackingPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        print("MainWindow initialized")

        # Create a central widget + layout
        central = QWidget()
        layout = QVBoxLayout()
        central.setLayout(layout)
        self.setCentralWidget(central)

        # --- TEST BUTTON ---
        self.test_btn = QPushButton("Test GUI → Logic")
        self.test_btn.clicked.connect(self.test_logic)
        layout.addWidget(self.test_btn)

        # --- TRACKING PANEL ---
        self.tracking_panel = TrackingPanel()
        layout.addWidget(self.tracking_panel)

        print("TrackingPanel added to layout")

    def test_logic(self):
        print("Test button clicked — GUI is working!")
