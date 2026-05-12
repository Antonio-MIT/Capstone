from skyfield.api import load, wgs84, Star
import numpy as np
import os

print("Tracker.py loaded from:", os.path.abspath(__file__))

class TrackingEngine:
    def __init__(self, latitude, longitude, elevation_m=0):
        self.ts = load.timescale()
        self.ephemeris = load('de421.bsp')

        # Skyfield expects degrees here — this produces a GeographicPosition
        self.location = wgs84.latlon(latitude, longitude, elevation_m)

        print("DEBUG: type(self.location) =", type(self.location))

    def compute_altaz(self, ra_hours, dec_degrees, time):
        target = Star(ra_hours=ra_hours, dec_degrees=dec_degrees)

        # CRITICAL: Convert GeographicPosition → Topos by adding Earth
        observer = self.ephemeris['earth'] + self.location

        # Now .at(time) returns a ToposPosition, which supports .observe()
        astrometric = observer.at(time).observe(target)

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

        # Enter
        for i in range(1, len(inside)):
            if inside[i] and not inside[i-1]:
                events["enter"] = times[i].utc_iso()
                break

        # Exit
        for i in range(1, len(inside)):
            if not inside[i] and inside[i-1]:
                events["exit"] = times[i].utc_iso()
                break

        # Transit (max altitude)
        max_idx = np.argmax(alt_array)
        events["transit"] = times[max_idx].utc_iso()

        # Duration (simple placeholder)
        if events["enter"] and events["exit"]:
            dt1=times[max_idx].utc_datetime()
            dt0=times[0].utc_datetime()
            delta = dt1-dt0
            events["duration_minutes"] = int(delta.total_seconds() / 60)

        return events
