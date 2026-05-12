from Tracker import TrackingEngine

def run_test():
    print("Running TrackingEngine test...")

    engine = TrackingEngine(
        latitude=37.983810,
        longitude=23.727539,
        elevation_m=0
    )

    # Test values
    ra_hours = 12.0
    dec_degrees = 45.0
    beamwidth_deg = 10.0

    print("Inputs:")
    print("  RA =", ra_hours)
    print("  Dec =", dec_degrees)
    print("  Beamwidth =", beamwidth_deg)

    result = engine.sweep_day(
        ra_hours=ra_hours,
        dec_degrees=dec_degrees,
        beamwidth_deg=beamwidth_deg
    )

    print("\nResults:")
    print("  Enter:", result["enter"])
    print("  Transit:", result["transit"])
    print("  Exit:", result["exit"])
    print("  Duration:", result["duration_minutes"], "minutes")

if __name__ == "__main__":
    run_test()
