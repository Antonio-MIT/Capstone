import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)
print("DEBUG sys.path:", sys.path)


from ENGINE.Tracker import TrackingEngine


## TEST SUITE ###
TEST_CASES = [
    {
        "name": "Vega",
        "ra_hours": 18.615,
        "dec_degrees": 38.78,
        "beamwidth_deg": 10.0
    },
    {
        "name": "Deneb",
        "ra_hours": 20.69,
        "dec_degrees": 45.28,
        "beamwidth_deg": 10.0
    },
    {
        "name": "Test Star (RA 12h, Dec 45°)",
        "ra_hours": 12.0,
        "dec_degrees": 45.0,
        "beamwidth_deg": 10.0
    },
    {
        "name": "Altair",
        "ra_hours": 19.85,
        "dec_degrees": 8.87,
        "beamwidth_deg": 10.0
    },
    {
        "name": "Polaris",
        "ra_hours": 2.52,
        "dec_degrees": 89.26,
        "beamwidth_deg": 10.0
    }
]




def run_test():
    print("Running TrackingEngine test...")

    engine = TrackingEngine(
    latitude=37.983810,
    longitude=23.727539,
    elevation_m=0
)

    # Test values | FAILED TO ENTER BEAM & SINGULAR TEST
    #ra_hours = 12.0
    #dec_degrees = 45.0
    #beamwidth_deg = 10.0




    #print("Inputs:")
    #print("  RA =", ra_hours)
    #print("  Dec =", dec_degrees)
    #print("  Beamwidth =", beamwidth_deg)
    for case in TEST_CASES:
        print(f"==={case['name']} ===")
        #print(f"RA:{case['ra_hours']h, Dec: {case['dec_degrees']}°, Beam: {case['beamwidth_deg']}°") SYTAX ERROR
        print(f"RA: {case['ra_hours']}h, Dec: {case['dec_degrees']}°, Beam: {case['beamwidth_deg']}°")
    result = engine.sweep_day(
        ra_hours=case["ra_hours"],
        dec_degrees=case["dec_degrees"],
        beamwidth_deg=case["beamwidth_deg"]
    )

    print("\nResults:")
    print("  Enter:", result["enter"])
    print("  Transit:", result["transit"])
    print("  Exit:", result["exit"])
    print("  Duration:", result["duration_minutes"], "minutes")

if __name__ == "__main__":
    run_test()
