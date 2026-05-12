from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QLabel
)
from PySide6.QtCore import Qt

from Tracker import TrackingEngine


class TrackingPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create tracking engine with your observer location
        self.engine = TrackingEngine(
            latitude=37.983810,
            longitude=23.727539,
            elevation_m=0
        )

        # Main layout
        layout = QVBoxLayout()
        form = QFormLayout()

        # Input fields
        self.ra_input = QLineEdit()
        self.dec_input = QLineEdit()
        self.beam_input = QLineEdit()

        form.addRow("RA (hours):", self.ra_input)
        form.addRow("Dec (degrees):", self.dec_input)
        form.addRow("Beamwidth (deg):", self.beam_input)

        layout.addLayout(form)

        # Compute button
        self.compute_btn = QPushButton("Compute Tracking Window")
        self.compute_btn.clicked.connect(self.compute_tracking)
        layout.addWidget(self.compute_btn)

        # Output labels
        self.enter_label = QLabel("Enter: ---")
        self.transit_label = QLabel("Transit: ---")
        self.exit_label = QLabel("Exit: ---")
        self.duration_label = QLabel("Duration: ---")

        layout.addWidget(self.enter_label)
        layout.addWidget(self.transit_label)
        layout.addWidget(self.exit_label)
        layout.addWidget(self.duration_label)

        layout.addStretch()
        self.setLayout(layout)

    def compute_tracking(self):
        print("1) Compute button clicked")   # DEBUG

        try:
            ra = float(self.ra_input.text())
            dec = float(self.dec_input.text())
            beam = float(self.beam_input.text())

            print("2) Parsed inputs:", ra, dec, beam)  # DEBUG

            result = self.engine.sweep_day(
                ra_hours=ra,
                dec_degrees=dec,
                beamwidth_deg=beam
            )

            print("3) Engine result:", result)  # DEBUG

            # Update UI labels
            self.enter_label.setText(f"Enter: {result['enter']}")
            self.transit_label.setText(f"Transit: {result['transit']}")
            self.exit_label.setText(f"Exit: {result['exit']}")
            self.duration_label.setText(f"Duration: {result['duration_minutes']} min")

            print("4) UI labels updated")  # DEBUG

        except Exception as e:
            print("ERROR in compute_tracking:", e)
