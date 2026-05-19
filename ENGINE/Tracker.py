import os
import json
import numpy
from datetime import timedelta
from skyfield.api import load, Star, Angle,Topos,wgs84
from ENGINE.Weather import WeatherEngine
from skyfield.api import N, W, wgs84

#CONST for TrackingEngine
# TEST ABC
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'DATA', 'de421.bsp')
DATA_PATH = os.path.abspath(DATA_PATH)

#from datetime import datetime, timedelta
#from DATA import de421 #loads ephemeris
#Loading ephemeris
#planets = load('DATA/de421.bsp')
#earth = planets['earth']
#sun = planets['sun']
# Loading timescale
#ts = load.timescale()

# Must be in the class
#import inspect
#print(">>> TRACKINGENGINE LOADED FROM:", inspect.getfile(self.__class__))

# Remove weather_api_key=None from TrackingEngine
class TrackingEngine:
    #  Future: Ensure path to .json is stored in an environment variable
    def __init__(self, latitude, longitude, elevation_m=0,weather_api_key=None):
        import inspect
        print(">>>> TRACKINGENGINE LOADED FROM:", inspect.getfile(self.__class__))
        #print(">>> TRACKINGENGINE LOADED FROM:", inspect.getfile(self.__class__))
        with open("/capstone_config/weather_config.json") as f:
            config = json.load(f)
        api_key = config["openweather_api_key"]
        #if weather_api_key is not None:
        from ENGINE.Weather import WeatherEngine

        self.ts = load.timescale()
        #self.ephemeris = load('DATA/de421.bsp') PATHING ISSUE
        self.ephemeris = load(DATA_PATH)

        # Correct observer (Topos) CRITICAL - Must ensure that the default geocentric position has been set to a topograhpic position with LAT and LONG
        # self.location = Topos(latitude_degrees=latitude,longitude_degrees=longitude) REDEFINING THE OBSERVER
        # self.location = wgs84.latlon(latitude, longitude, elevation_m) CORRECT OBSERVER SIGNATURE
        # UPDATING...
        earth = self.ephemeris['earth']
        self.location = earth + wgs84.latlon(latitude, longitude)

        #self.location = wgs84.latlon(37.9838, 23.7275, 0)

        self.weather = WeatherEngine(api_key,latitude, longitude)

        # Weather.py integration
        # Removing API key integreation.
        #    from ENGINE.Weather import WeatherEngine
        #    self.weather = WeatherEngine(latitude, longitude)
        #else:
        #    self.weather = None


        # DEBUGGING #
        # print("DEBUG: ephemeris keys =", self.ephemeris.keys()) ERROR
        print("DEBUG: ephemeris loaded:", self.ephemeris)
        print("DEBUG: sun object:", self.ephemeris['sun'])


        print("DEBUG: type(self.location) =", type(self.location))
        print("Tracker.py loaded from:", os.path.abspath(__file__))
        print("DEBUG: TrackingEngine class loaded from:", __file__)

    # ---------------------------------------------------------
    # STAR FACTORY
    # ---------------------------------------------------------
#from skyfield.api import Star, Angle

    def star(self, ra_hours, dec_degrees):
        return Star(
            ra=Angle(hours=ra_hours),
            dec=Angle(degrees=dec_degrees)
        )


    # ---------------------------------------------------------
    # SUN ALTITUDE CHECK
    # ---------------------------------------------------------
    def is_night(self, t):
      
        #print("DEBUG is_night type(t):", type(t))
        #print("DEBUG is_night:", t.utc_strftime(), "->", result)
        sun = self.ephemeris['sun']
        #Uncommented line below despite topos errors
        observer = self.location.at(t)
        # earth = self.ephemeris['earth']
        # observer = (earth + self.location).at(t)

        alt, az, distance = observer.observe(sun).apparent().altaz()
        value = alt.degrees < 0.0
        print("DEBUG is_night:", t.utc_strftime(), "->", value)
        print("DEBUG location type in is_night:", type(self.location))
        return value
    # ---------------------------------------------------------
    # ALT/AZ COMPUTATION
    # ---------------------------------------------------------
    def compute_altaz(self, ra_hours, dec_degrees, t):
        print("DEBUG type(self.location):", type(self.location))
        star = self.star(ra_hours, dec_degrees)
        #Uncommented observer = self..despite TOPOS errors
        # Is this a geocentric object at RUNTIME?
        observer = self.location.at(t)
        #Removed lines below, breaking Skyfields model.	
        #earth = self.ephemeris['earth']
        #observer = (earth + self.location).at(t)

        alt, az, distance = observer.observe(star).apparent().altaz()
        return alt,az

    # ---------------------------------------------------------
    # ZENITH BEAM CHECK
    # ---------------------------------------------------------
    def in_zenith_beam(self, ra_hours, dec_degrees, t, beam_deg=8.9):
        alt, az = self.compute_altaz(ra_hours, dec_degrees, t)
   # Convert Skyfield Angle --> float degrees

        alt_deg = alt.degrees
        half_beam = beam_deg / 2.0


        #min_alt = 90.0 - (beam_deg / 2.0)
        return abs(alt_deg - 90.0) <= half_beam

    # Leads guidance fragmented:
    # If myCurrentAltitude(degrees) greater than or equal to 90 - BeamWidth/2 object is visible in FOV.
    # If Objects abs value Declination - Latitude greater than BeamWidth/2 == True, object is NOT in FOV.
    # Else Objects abs value Declination - Latitude greater than BeamWidth/2 == False, object does cross FOV.

    # ---------------------------------------------------------
    # NIGHTTIME‑FILTERED VISIBILITY WINDOW
    # ---------------------------------------------------------
    def sweep_day(self, ra_hours, dec_degrees, beamwidth_deg):
        if not isinstance(ra_hours, (int, float)):
            raise TypeError("RA must be a number")

        if not isinstance(dec_degrees, (int, float)):
            raise TypeError("Dec must be a number")

        ts = self.ts
        start = ts.utc(2025, 1, 1, 0, 0)
        end   = ts.utc(2025, 1, 1, 23, 59)

        step_minutes = 1
        t = start

        entry = None
        transit = None
        exit = None
        max_alt = -999.0

        while t < end:
            print("LOOP T:", t.utc_strftime())

            if self.is_night(t):
                alt, az = self.compute_altaz(ra_hours, dec_degrees, t)
                alt_deg = alt.degrees

                if self.in_zenith_beam(ra_hours, dec_degrees, t, beamwidth_deg):

                    if entry is None:
                        entry = t

                    if alt_deg > max_alt:
                        max_alt = alt_deg
                        transit = t
                else:
                    if entry is not None and exit is None:
                        exit = t

            # 🔴 must be inside the loop, at this indentation
            t = t + (step_minutes / 1440.0)

        if entry is None:
            return {
                "enter": None,
                "transit": None,
                "exit": None,
                "duration_minutes": 0
            }

        if exit is None:
            exit = end

        duration = int((exit.utc_datetime() - entry.utc_datetime()).total_seconds() / 60)

        return {
            "enter": entry.utc_strftime('%H:%M'),
            "transit": transit.utc_strftime('%H:%M') if isinstance(transit, type(start)) else None,
            "exit": exit.utc_strftime('%H:%M'),
            "duration_minutes": duration
        }
