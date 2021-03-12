# Import and setup

import pandas as pd
import requests
import os
import time

# API key for Google Geociding API, stored as environment variable
API_KEY = os.environ.get('GEOCODING_API_KEY')
rides_df = pd.read_csv('all_rides.csv')

# Iterate over each location in the dataset and get coordinates from Google Geocoding API
geocoding_dict = dict()
distinct_stations = tuple(rides_df['ride_start_location'].append(rides_df['ride_end_location']).unique())

for station in distinct_stations:
    # Ensure station is given as an intersection
    if station.find('&') != -1:
        # Format address for API call (old stations have " (old)" appended to the end of their names, 
        # which throws off the API)
        address = '+'.join(station.split()).replace('&', 'and').replace(' old', '') # Format address for API call
        
        geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address},+New+York,+NY&key={API_KEY}'
        response = requests.get(geocoding_url)
        data = response.json()
        geocoding_dict[station] = (data['results'][0]['geometry']['location']['lat'], data['results'][0]['geometry']['location']['lng'])
        
        # API only allows 50 calls per second
        time.sleep(0.05)

    else:
        print('The following station name is not given as an intersection: ', station)
        
rides_df['ride_start_latitude'] = rides_df['ride_start_location'].apply(lambda x: geocoding_dict.get(x, (None, None))[0])
rides_df['ride_start_longitude'] = rides_df['ride_start_location'].apply(lambda x: geocoding_dict.get(x, (None, None))[1])
rides_df['ride_end_latitude'] = rides_df['ride_end_location'].apply(lambda x: geocoding_dict.get(x, (None, None))[0])
rides_df['ride_end_longitude'] = rides_df['ride_end_location'].apply(lambda x: geocoding_dict.get(x, (None, None))[1])


rides_df.to_csv('all_rides_with_gps.csv')
