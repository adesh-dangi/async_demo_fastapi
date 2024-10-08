free_api_token = "<token>"
end_point_header = "<header>"
# Define the API endpoints (using real or close-to-real URLs)
# Spoonacular API for food recipes
FOOD_API = "https://api.spoonacular.com/recipes/random"
WEATHER_API = f"https://Historical-Weather-API2.proxy-production.allthingsdev.co/v1/archive?latitude=52.52&longitude=13.41&elevation=1603&start_date=2024-07-09&end_date=2024-07-23&hourly=temperature_2m&tilt=0&azimuth=0&models=best_match&daily=weather_code&temperature_unit=celsius&wind_speed_unit=kmh&precipitation_unit=mm&timeformat=iso8601&timezone=auto&cell_selection=land' \
--header 'x-apihub-key: {free_api_token}"  # OpenWeatherMap API
MUSIC_API = "https://api.spotify.com/v1/search"  # Spotify API for music search
# Google Maps Geocoding API
MAP_API = "https://maps.googleapis.com/maps/api/geocode/json"