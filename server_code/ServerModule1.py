import anvil.secrets
import anvil.server
import anvil.http
from datetime import datetime
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def get_forcast_data(location):
  API_URL = f"http://api.openweathermap.org/data/2.5/forecast?lat={location['lat']}&lon={location['lon']}&appid={anvil.secrets.get_secret('api_key')}&units=metric"
  print(API_URL)
  response = anvil.http.request(API_URL, json=True)
   # Extract forecast data
  times = [datetime.fromtimestamp(i['dt']) for i in response['list']]
  temps = [i['main']['temp'] for i in response['list']]
  # Extract summary data
  summary_data = {"temp_min": response['list'][0]['main']['temp_min'], 
                  "temp_max": response['list'][0]['main']['temp_max'], 
                  "description": response['list'][0]['weather'][0]['description'], 
                  "icon": response['list'][0]['weather'][0]['icon']}
  
  return times, temps,summary_data
