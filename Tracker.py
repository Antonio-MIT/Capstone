from skyfield.api import load, wgs84, Star
from datetime import timedelta
import numpy as np

class TrackingEngine:
    def __init__(self, latitude, longitude, elevation_m=0):
        self.ts = load.timescale()
        self.ephemeris = load('de421.bsp')  # JPL ephemeris
        self.location = wgs84.latlon(latitude, longitude, elevation_m)

    def compute_altaz(self, ra_hours, dec_degrees, time):
        target = Star(ra_hours=ra_hours, dec_degrees=dec_degrees)
        astrometric = self.location.at(time).observe(target)
        alt, az, distance = astrometric.apparent().altaz()
        return alt.degrees, az.degrees

    def sweep_day(self, ra_hours, dec_degrees, beamwidth_deg, step_minutes=1):
        now = self.ts.now()
        times = now + np.linspace(0, 24, int(24*60/step_minutes)) / 24.0

        alt_list = []
        for t in times:
            alt, az = self.compute_altaz(ra_hours, dec_degrees, t)
            alt_list.append(alt)

        alt_array = np.array(alt_list)
        inside = alt_array > (beamwidth_deg / 2)

        events = {
            "enter": None,
            "transit": None,
            "exit": None,
            "duration_minutes": 0
        }

        # Detect enter
        for i in range(1, len(inside)):
            if inside[i] and not inside[i-1]:
                events["enter"] = times[i].utc_iso()
                break

        # Detect exit
        for i in range(1, len(inside)):
            if not inside[i] and inside[i-1]:
                events["exit"] = times[i].utc_iso()
                break

        # Detect transit (max altitude)
        max_idx = np.argmax(alt_array)
        events["transit"] = times[max_idx].utc_iso()

        # Duration
        if events["enter"] and events["exit"]:
            t1 = times[max_idx]
            t2 = times[max_idx]
            events["duration_minutes"] = int((times[max_idx] - times[0]).seconds / 60)

        return events
