from ENGINE.Tracker import TrackingEngine

#POSITONAL ARGUMENTS - Athens, Greece
# Lat is 38 degree N
# Long is 24 degree E
LAT = 37.9339
LON = 23.7275

engine = TrackingEngine(LAT,LON)

print(">>> TYPE OF LOCATION:", type(engine.location))

# Vega
# result = engine.sweep_day(18.615, 38.783, 10)

# Polaris
#result = engine.sweep_day(2.53,89.2641,10)

# UNKNOWN
result = engine.sweep_day(0.0, 38.0, 10)

print(">>> RESULT:", result)

