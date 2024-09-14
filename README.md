# Weather-Cast    [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
<p align="center">
  <img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Freshmaharidhas%2FWeather-Cast&labelColor=%23000000&countColor=%2300ff00&style=plastic&labelStyle=none"/>
  <img src="https://img.shields.io/github/watchers/reshmaharidhas/Weather-Cast"/>
  <img src="https://img.shields.io/github/languages/top/reshmaharidhas/Weather-Cast?labelColor=%23000000"/>
  <img src="https://img.shields.io/sourceforge/dt/weather-cast?label=Sourceforge%20downloads&labelColor=%23FF0000&color=%23000000"/>
  <img src="https://img.shields.io/github/downloads/reshmaharidhas/Weather-Cast/total?label=GitHub%20downloads&labelColor=%23000000&color=%230000FF"/>
  <img src="https://img.shields.io/github/v/release/reshmaharidhas/Weather-Cast"/>
  <img src="https://img.shields.io/github/release-date/reshmaharidhas/Weather-Cast"/>
  <img src="https://img.shields.io/github/license/reshmaharidhas/Weather-Cast?labelColor=%23000000"/>
</p>
Weather app is a desktop weather app for Windows OS.

![frankfurt_screenshot](https://github.com/user-attachments/assets/578c795c-3a7d-4ed0-83cc-f32d08f2576f)

## Demo
https://github.com/user-attachments/assets/6cb2b071-30f1-4dab-8e6d-bdccb84467b6

## Tech Stack
- Python
- Tkinter
- Gemini AI
- Matplotlib
- Seaborn
- REST API

## API used
- OpenWeatherMap API
- WeatherAPI API
- apiip API
- Gemini API
  
## Features
- Displays current weather information of selected city.
  - Current temperature and description of current temperature (sunny☀️/cloudy☁️/rainy🌧️/thunder⛈️/Snow)
  - Feels-like temperature
  - Wind speed
  - Humidity
  - Dew point
  - Visibility
  - Pressure
  - UV index
  - Air pollution index
- Dynamically changing background on dashboard based on current weather temperature of selected city.
- Displays global cities with the same name of the city you searched in combobox to let the user choose from.
- Displays the country name of the selected city with the local time.🕦
- Displays present day's information
  - Moon phase with picture and illumination in percentage.
    - 🌑 New moon
    - 🌒 Waxing Crescent
    - 🌓 First Quarter
    - 🌔 Waxing Gibbous
    - 🌕 Full moon
    - 🌖 Waning Gibbous
    - 🌗 Third Quarter
    - 🌘 Waning Crescent
  - Displays sunrise🌅, sunset🌇, moon rise, and moon set🌕 timing of present day in the selected city.
- View all weather data of user's current location on clicking the location button by automatically detecting user location using public IP address.
- Present day's air pollutants and their concentrations to safeguard your respiratory health.
- Shows the overall weather forecast for the next 2 days with temperature, temperature description, lowest and highest temperature for each day with icons.
- View the hourly temperatures for the next 10 hours in 3 hour interval period.
- Line chart📈 to visualize the next 10 hourly weather fluctuations based on temperature.
- One click refresh button to view the updated weather information of the last selected city.
- Displays the current air pollution index with a human face depicting the air pollution level of the selected city.
- Displays current UV index with tips to protect from harmful UV rays.
- Bar chart📊 to visualize the present day's hourly UV index with varied colors.
- Toggle between Fahrenheit and Celsius temperature🌡️ units in single click of button.
- Search for weather data for any city around the world in a navigation friendly interface.🔍
- Detailed hourly weather forecast for the next 3 days including the present day visualized using line charts for,
  - Temperature
  - Pressure
  - Wind speed
  - Humidity
  - Precipitation
  - Chance of rain
  - Cloud cover
  - Snow
  - Visibility
  - Dew point
  - UV index (bar chart)
- Historical weather trends visualization for the past 2 days with hourly details for
  - Temperature
  - Precipitation
- Wind direction and speed visualization for the next 3 days on a custom-designed wind rose chart.
- View a random interesting fact about the city searched generated using Gemini AI.

## Screenshots
![hyderabad_screenshot](https://github.com/user-attachments/assets/53af5cdc-5e6f-4948-bfe9-a9c64c9a1874)
![tokyo](https://github.com/user-attachments/assets/ad470454-843a-40a7-92d2-139e9bf96d60)
![berlin_germany_day](https://github.com/user-attachments/assets/c432070c-1f51-4195-8e27-d5a8e531f4e4)
![amsterdam_US_day_clearsun](https://github.com/user-attachments/assets/45443c13-78a4-4c7d-9189-7e6286150918)

## Run⚙️
Before running the application,
- Obtain API key from OpenWeatherMap API.
- Obtain API key from WeatherAPI API.
- Obtain API access key from www.apiip.net
- Obtain API key from Gemini API.
- Insert your API keys into weather_cast.py file at appropriate places in the code and replace with your new registered API keys = "YOUR_...._API_KEY'
- Run the main.py file.

## License
MIT License
