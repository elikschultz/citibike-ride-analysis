# Citibike Ride Analysis

This repository contains code for a small personal project. I am an active user of New York's Citi Bike bikeshare program, and have always found it interesting to be able to see my personal ride history within the app and on the Citi Bike site. I thought it would be nice to be able to access this data in a format that lends itself to systematic analysis, so I wrote this scraper using the Python Selenium package to get data from the site and export it to a csv.

Since a user has to log in in order to view their ride history, the program requires user input to run successfully. In addition to running the script, a user will have to follow prompts to enter:

- their phone number
- a verification code that the site sends to their phone
- enter their email address

