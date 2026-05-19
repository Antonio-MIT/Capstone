from PySide6.QtWidgets import (QSizePolicy,QWidget, QVBoxLayout, QFormLayout, QLineEdit,QPushButton, QLabel,QComboBox)
from PySide6.QtCore import Qt
from ENGINE.Tracker import TrackingEngine
import traceback

class TrackingPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


        # Create `tracking engine` with your observer location
        # API.WEATHER.GOV: "We are testing including a more traditional API Key system on certain endpoints.
        # This is due to a large change in the weather.gov site. The API remains open and free to use and
        # there are no limits imposed based on the X-Api-Key string.
        self.engine = TrackingEngine(
            latitude=37.983810,
            longitude=23.727539,
            elevation_m=0,
            # weather_api_key=None
        )

        layout = QVBoxLayout()
        self.setLayout(layout)
        
        #Weather GUI integreation. NOTE: Relies on `tracking engine` to run.
        #weather = self.engine.weather.get_current_weather()
        #self.weatherLabel.setText(f"{weather['weather'][0]['description']}, {weather['main']['temp']}°C")
        # Modified to satisfy JSON structure from WEATHER.GOV
        #forecast = self.engine.weather.get_current_weather()
        #period = forecast["properties"]["periods"][0]
        #description = period["shortForecast"]
        #temp = period["temperature"]
        #self.weatherLabel.setText(f"{description}, {temp}°")

# 1. Create label
        #Weather UI setup
        self.object_select = QComboBox()
        layout.addWidget(self.object_select)
        self.object_select.currentIndexChanged.connect(self.on_object_selected)

# 3. THEN update it with real weather data




        self.object_select.addItem("Select Object...", None)
        self.object_select.addItem("Polaris (α UMi)", (2.5303, 89.2641))
        self.object_select.addItem("M31 – Andromeda Galaxy", (0.712, 41.269))
        self.object_select.addItem("M42 – Orion Nebula", (5.591, -5.391))
        self.object_select.addItem("M13 - Hercules Globular Cluster", (16.695,36.467))
        self.object_select.addItem("M57 - Ring Nebula", (18.885,33.03))
        self.object_select.addItem("Vega -  (α Lyrae)", (18.615,38.783))

        #self.object_select.currentIndexChanged.connect(self.on_object_selected)
        self.weatherLabel = QLabel("Loading weather...")
        self.weatherLabel.setAlignment(Qt.AlignCenter)
        self.weatherLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout.addWidget(self.weatherLabel)



        weather = self.engine.weather.get_current_weather()
        print("DEBUG weather JSON:", weather)

        description = weather["weather"][0]["description"]
        temp = weather["main"]["temp"]

        self.weatherLabel.setText(f"{description}, {temp}°C")



        # Main layout
        #layout = QVBoxLayout()
        # Input and Output fields
        form = QFormLayout()
        self.ra_input = QLineEdit()
        self.dec_input = QLineEdit()
        self.beam_input = QLineEdit()

        form.addRow("RA (hours):", self.ra_input)
        form.addRow("Dec (degrees):", self.dec_input)
        form.addRow("Beamwidth (deg):", self.beam_input)
        layout.addLayout(form)

        self.ra_input.setPlaceholderText("e.g., 2.5303 (hours)")
        self.dec_input.setPlaceholderText("e.g., 89.2641 (degrees)")
        self.beam_input.setPlaceholderText("e.g., 10 (degrees)")


        #layout.addLayout(form)

        # Compute button
        self.compute_btn = QPushButton("Compute Tracking Window")
        self.compute_btn.clicked.connect(self.compute_tracking)
        layout.addWidget(self.compute_btn)


        # Output labels
        self.weatherLabel.setAlignment(Qt.AlignCenter)
        self.weatherLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.enter_label = QLabel("Enter: ---")
        self.transit_label = QLabel("Transit: ---")
        self.exit_label = QLabel("Exit: ---")
        self.duration_label = QLabel("Duration: ---")

        # Removed statement, should be called earlier.
        #self.layout.addWidget(self.weatherLabel)

        layout.addWidget(self.enter_label)
        layout.addWidget(self.transit_label)
        layout.addWidget(self.exit_label)
        layout.addWidget(self.duration_label)

        layout.addStretch()
        self.setLayout(layout)

    def on_object_selected(self, index):
        print("DEBUG: object selected index =", index)
        data = self.object_select.itemData(index)
        print("DEBUG: object data =", data)
        if data is None:
            return
        ra, dec = data
        self.ra_input.setText(str(ra))
        self.dec_input.setText(str(dec))



    def compute_tracking(self):
        print("1) Compute button clicked")   # DEBUG

        try:
            ra = float(self.ra_input.text())
            dec = float(self.dec_input.text())
            beam = float(self.beam_input.text())

            #convert RA from degress to hours
            if ra > 24:
                ra = ra/15.0

            print("RA input=",ra)
            print("Dec input=",dec)
            print("Beam input=",beam)

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
            traceback.print_exc()
