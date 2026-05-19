import requests
#Your new WeatherEngine must match three constraints:

#Use OpenWeatherMap, not weather.gov

#Accept the API key from TrackingEngine

#Return JSON in the structure your GUI already expects  
#(because your GUI uses weather['main']['temp'] and weather['weather'][0]['description'])


#Class constructor
class WeatherEngine:
    def __init__(self, api_key, latitude, longitude):
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude

#Class method

    def get_current_weather(self):
       url = (
          f"https://api.openweathermap.org/data/2.5/weather"
          f"?lat={self.latitude}&lon={self.longitude}"
          f"&appid={self.api_key}&units=metric"
)

       response = requests.get(url)
       data = response.json()
       return data


#Build that URL

#Call requests.get()

#Convert to JSON

#Return the JSON

