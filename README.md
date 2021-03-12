# Citibike Ride Analysis

This repository contains code for a small personal project. I am a user of New York's Citi Bike bikeshare program, and have always found it interesting to be able to see my personal ride history within the app and on the Citi Bike site. I thought it would be nice to be able to access this data in a format that lends itself to systematic analysis, so I wrote this scraper using the Python Selenium package to get data from the site and export it to a csv. (Citi Bike does make some data more readily available for download, but as far as I can tell this is anonymized data for the system as a whole, and I am particularly curious to look at my own ride history.)

The first script to run is `scraper.py`. Since a user has to log in in order to view their ride history, the program requires user input to run successfully. In addition to running the script, a user will have to follow prompts to enter:

- their phone number
- a verification code that the site sends to their phone
- enter their email address

Once the user enters their information, `scraper.py` completes its work of getting all of the user's ride history into a csv file.

The next script to run is `get_station_gps_coordinates.py`. This script requires the user to have the Google Geocoding API enabled, and to have their API key saved as an environment variable. API key setup instructions are available [here](https://developers.google.com/maps/documentation/geocoding/start). One caveat here is that only station names that are given as intersections are used, since other station names can confuse the API. Fortunately, the vast majority of Citi Bike station names are given as intersections.

Finally, the `mapper.r` script creates a map that shows a user's rides, with a color gradient to represent route frequency. A sample output is shown below:

![citibike_ride_map](https://user-images.githubusercontent.com/35080150/110874202-573ea180-82a1-11eb-8d58-9fdccc6feba3.png)
