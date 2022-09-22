#Note:  I really hate the restrictions of the starter code, so i just started form scratch. sorry not sorry

import time
from datetime import datetime
import requests as rq #importing the requsest <-my spelling is why i used 'rq'
import json
from citipy import citipy #location finder
#import geocoder as gc #personal location finder to add my own spin this
import numpy as np #fancy numpy stuff
from Config import api_key
import pandas as pd

#create my 
url = 'http://api.openweathermap.org/data/2.5/weather?units=Imperial&APPID='
target_url = f'{url}{api_key}'
#don't print your API key 

#make a list of 2000 random latitude and longitude cords
lats = np.random.uniform(low =-90.000, high=90.000, size=2000)
longt = np.random.uniform(low=-180.000, high=180.000, size=2000)
lat_lngs = zip(lats, longt) #zip zip zip it up, 
lat_lngs #outputs as zip object time to convert to a list

coordinates = list(lat_lngs)

cities = [] #create an empty list for the cities 

for cored in coordinates: #tempted to add a loading bar
    city = citipy.nearest_city(coordinates[0], cored[1]).city_name
    if city not in cities:
        cities.append(city)
len(cities) #in notebook this will print the number of unique cities 

city_data = []

print("Beginning Data Retrieval     ")
print("-----------------------------")

record_count = 1
set_count = 1

for i, city in enumerate(cities): #enumerate seems like the right thing to use,probably could've used the number of results tho

    if(i % 50 == 0 and i >= 100):
        set_count += 1
        record_count = 1
        time.sleep(60) #time to
    
    city_url = url + '&q=' + city.replace(' ','+')
    print(f'Processing Record {record_count} of Set {set_count} | City: {city}')
    record_count += 1

    try:
        # Parse the JSON and retrieve data.
        city_weather = rq.get(city_url).json()
        # Parse out the needed data.
        city_lat = city_weather["coord"]["lat"]
        city_lng = city_weather["coord"]["lon"]
        city_max_temp = city_weather["main"]["temp_max"]
        city_humidity = city_weather["main"]["humidity"]
        city_clouds = city_weather["clouds"]["all"]
        city_wind = city_weather["wind"]["speed"]
        city_country = city_weather["sys"]["country"]
        # Convert the date to ISO standard.
        city_date = datetime.utcfromtimestamp(city_weather["dt"]).strftime('%Y-%m-%d %H:%M:%S')
        # Append the city information into city_data list.
        city_data.append({"City": city.title(),
                          "Lat": city_lat,
                          "Lng": city_lng,
                          "Max Temp": city_max_temp,
                          "Humidity": city_humidity,
                          "Cloudiness": city_clouds,
                          "Wind Speed": city_wind,
                          "Country": city_country,
                          "Date": city_date})
    except:
        print(f"ERROR WARNING.  CITY NOT FOUND. {city}")
        pass

print('------------------------')
print("Data Retrieval Complete") #loading bar would've been cool though.
#Also would've been faster to split the data in threads using "threading module"
#Not sure if requests can handle that though. and it is outside of the scope of this project.

city_data_df = pd.DateFrame(city_data)
city_data_df.head(100)


# Create the output file (CSV).
output_data_file = "weather_database/cities.csv"
# Export the City_Data into a CSV.
#city_data_df.to_csv(output_data_file, index_label="City_ID")