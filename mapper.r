# Uncomment to install packages as needed
# install.packages('ggmap')
# install.packages('dplyr')
# install.packages('magrittr')
library(ggmap)
library(dplyr)
library(magrittr)

# Import data and aggregate ride counts by route
ride_data = read.csv('all_rides_with_gps.csv')
ride_data = ride_data %>% 
  group_by(ride_start_longitude, ride_start_latitude, ride_end_latitude, ride_end_longitude) %>%
  summarise(total_rides = n())

# Map setup
register_google(key = Sys.getenv('GEOCODING_API_KEY'))
gc = geocode('New York')
map = get_map(c(left = min(c(ride_data$ride_start_longitude, ride_data$ride_end_longitude), na.rm = TRUE) - 0.01,
                bottom = min(c(ride_data$ride_start_latitude, ride_data$ride_end_latitude), na.rm = TRUE) - 0.01,
                right = max(c(ride_data$ride_start_longitude, ride_data$ride_end_longitude), na.rm = TRUE) + 0.01,
                top = max(c(ride_data$ride_start_latitude, ride_data$ride_end_latitude), na.rm = TRUE) + 0.01))

# Plot map and rides
ggmap(map, extent = 'device') +
  geom_segment(data = ride_data,
             aes(x = ride_start_longitude,
                 y = ride_start_latitude,
                 xend = ride_end_longitude,
                 yend = ride_end_latitude,
                 color = log(total_rides),
                 alpha = log(total_rides),
                 size = log(total_rides)),
             arrow = arrow(length = unit(0.015, "npc"))) +
  scale_colour_gradient(low = "yellow", high = "red", guide = FALSE) +
  scale_alpha_continuous(range = c(0.8, 1), guide = FALSE) +
  scale_size_continuous(range=c(0.2, 0.3), guide = FALSE)
  coord_quickmap()

ggsave('citibike_ride_map.png')
