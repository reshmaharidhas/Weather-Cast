import textwrap
import tkinter as tk
from tkinter import ttk
import requests
import json
import math
from threading import Thread
from tkinter import messagebox
from PIL import Image,ImageTk
from datetime import datetime
from datetime import date
from datetime import timedelta
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import seaborn as sns
import matplotlib.pyplot as plt
import google.generativeai as genai
import os
import io


class WeatherCast:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather Cast")
        self.root.geometry("1800x770")
        self.root.minsize(width=1800,height=770)
        # Initializing the app with a city name if the app is not able to fetch user's public IP address.
        self.user_IP_Address = "Delhi"
        self.ip_address_city = "Delhi"
        self.last_selected_city_lat_lon = []
        # UI colors
        self.sky_color_light = "#9fe9fc"
        self.bg_dark_color = "#0463CA"
        self.pale_blue_color = "#3682d5"
        self.root.config(bg=self.bg_dark_color)
        # API keys
        self.my_api_key = "YOUR_OPENWEATHERMAP_API_KEY"        # Replace with your API key by registering at OpenWeatherMap API.
        self.my_weatherapi_key = "YOUR_WEATHERAPI_API_KEY"     # Replace with your API key by registering at WeatherAPI.
        # predefined variables
        self.temp_unit = "F"
        self.current_weather_icon_code = ""
        self.temperature_unit_string = "imperial"
        self.air_quality_values = ["Good","Fair","Unhealthy","Hazardous","Very Hazardous"]
        self.air_quality_colors = ["#00ff00","yellow","orange","red","purple"]
        self.months_list = ["Jan","Feb","March","April","May","June","July","Aug","Sept","Oct","Nov","Dec"]
        self.uv_index_tips_list = ["Enjoy being outside","Seek shade during midday.\nWear hat & sunscreen",
                                   "Avoid being outside during midday.\n Shirt, sunscreen, sunglass & hat are must."]
        # sky pictures
        self.night_sky_pic1 = tk.PhotoImage(file="assets/images/nightsky.png")
        self.day_sky_pic1 = tk.PhotoImage(file="assets/images/day_sky_background2.png")
        self.cloudy_day_pic1 = tk.PhotoImage(file="assets/images/cloudy_sky_pic1.png")
        self.drizzle_day_pic1 = tk.PhotoImage(file="assets/images/drizzling_day.png")
        self.rainy_night_pic1 = tk.PhotoImage(file="assets/images/night_sky_raining.png")
        self.rainy_day_pic1 = tk.PhotoImage(file="assets/images/day_sky_raining.png")
        self.snowy_day_pic1 = tk.PhotoImage(file="assets/images/snowy_day.png")
        self.thunderstorm_day_pic1 = tk.PhotoImage(file="assets/images/thunderstorm_day.png")
        self.thunderstorm_day_night_pic1 = tk.PhotoImage(file="assets/images/thunderstorm_night.png")
        self.tornado_day_night_pic1 = tk.PhotoImage(file="assets/images/tornado_day_night.png")
        # symbol images
        self.thermometer_pic = tk.PhotoImage(file="assets/images/thermometer.png")
        self.down_arrow_pic = tk.PhotoImage(file="assets/images/down-arrow-50.png").subsample(2,2)
        self.up_arrow_pic = tk.PhotoImage(file="assets/images/up-arrow-50.png").subsample(2,2)
        self.refresh_icon = tk.PhotoImage(file="assets/images/icons8-refresh-50.png").subsample(2,2)
        self.location_icon = tk.PhotoImage(file="assets/images/location-48.png").subsample(2,2)
        self.about_icon = tk.PhotoImage(file="assets/images/icons8-about-50.png").subsample(2,2)
        self.app_icon_image = tk.PhotoImage(file="assets/images/weather_cast_icon.png")
        self.app_icon_image_small = tk.PhotoImage(file="assets/images/weather_cast_icon.png").subsample(2,2)
        # weather dashboard icon images
        self.wind_picture = tk.PhotoImage(file="assets/images/icons8-wind-50.png").subsample(2,2)
        self.pressure_icon = tk.PhotoImage(file="assets/images/icons8-pressure-50.png").subsample(2,2)
        self.humidity_icon = tk.PhotoImage(file="assets/images/icon-humidity-50.png").subsample(2,2)
        self.visibility_icon = tk.PhotoImage(file="assets/images/icon-visibility.png").subsample(2,2)
        self.dewpoint_icon = tk.PhotoImage(file="assets/images/dew-point.png").subsample(2,2)
        self.sunrise_icon = tk.PhotoImage(file="assets/images/icons8-sunrise-48.png")
        self.sunset_icon = tk.PhotoImage(file="assets/images/icons8-sunset-48.png")
        self.moon_crescent_icon = tk.PhotoImage(file="assets/images/moon-crescent.png")
        self.moon_rise_icon = tk.PhotoImage(file="assets/images/moonrise.png")
        self.moon_set_icon = tk.PhotoImage(file="assets/images/moonset.png")
        self.sun_timeline_pic2 = tk.PhotoImage(file="assets/images/icons8-sun-timeline_pic2.png")
        self.sun_timeline_pic3 = tk.PhotoImage(file="assets/images/icons8-sun-timeline_pic3.png")
        self.closed_umbrella_icon = tk.PhotoImage(file="assets/images/button_icons/closed_umbrella.png")
        self.open_umbrella_rain_icon = tk.PhotoImage(file="assets/images/button_icons/umbrella_rain.png")
        self.fact_bulb_icon = tk.PhotoImage(file="assets/images/fact_bulb.png")
        # Button icons
        self.wind_button_icon = tk.PhotoImage(file="assets/images/button_icons/wind.png")
        self.temperature_button_icon = tk.PhotoImage(file="assets/images/button_icons/temperature.png")
        self.pressure_button_icon = tk.PhotoImage(file="assets/images/button_icons/pressure.png")
        self.humidity_button_icon = tk.PhotoImage(file="assets/images/button_icons/humidity.png")
        self.dew_point_button_icon = tk.PhotoImage(file="assets/images/button_icons/dew_point.png")
        self.cloud_cover_button_icon = tk.PhotoImage(file="assets/images/button_icons/clouds_cover.png")
        self.precipitation_button_icon = tk.PhotoImage(file="assets/images/button_icons/precipitation.png")
        self.rain_chance_button_icon = tk.PhotoImage(file="assets/images/button_icons/rain_chance.png")
        self.snow_chance_button_icon = tk.PhotoImage(file="assets/images/button_icons/snow.png")
        self.visibility_button_icon = tk.PhotoImage(file="assets/images/button_icons/visibility.png")
        self.uv_button_icon = tk.PhotoImage(file="assets/images/button_icons/uv.png")
        # Moon phases images
        self.moon_phase_full_moon = tk.PhotoImage(file="assets/images/full-moon.png").subsample(5,5)
        self.moon_phase_new_moon = tk.PhotoImage(file="assets/images/black_full_moon.png").subsample(5,5)
        self.moon_phase_waxing_crescent = tk.PhotoImage(file="assets/images/waxing-crescent_moon.png").subsample(5,5)
        self.moon_phase_first_quarter = tk.PhotoImage(file="assets/images/waxing_quarter.png").subsample(5,5)
        self.moon_phase_waxing_gibbous = tk.PhotoImage(file="assets/images/waxing_gibbous.png").subsample(5,5)
        self.moon_phase_waning_gibbous = tk.PhotoImage(file="assets/images/waning_gibbous.png").subsample(5,5)
        self.moon_phase_last_quarter = tk.PhotoImage(file="assets/images/waning_quarter.png").subsample(5,5)
        self.moon_phase_waning_crescent = tk.PhotoImage(file="assets/images/waning_crescent_moon.png").subsample(5,5)
        # PhotoImage variables of faces for air pollution.
        self.face1 = tk.PhotoImage(file="assets/images/face1-removebg-preview.png").subsample(3, 3)
        self.face2 = tk.PhotoImage(file="assets/images/face2-removebg-preview.png").subsample(3, 3)
        self.face3 = tk.PhotoImage(file="assets/images/face3-removebg-preview.png").subsample(3, 3)
        self.face4 = tk.PhotoImage(file="assets/images/face4-removebg-preview.png").subsample(3, 3)
        self.face5 = tk.PhotoImage(file="assets/images/face5-removebg-preview.png").subsample(3, 3)
        # weather sun or moon picture PhotoImage variables
        self.d01_pic = "assets/images/clear_sun.png"
        self.n01_pic = "assets/images/clear_moon.png"
        self.d02_pic = "assets/images/02d.png"
        self.n02_pic = "assets/images/02n.png"
        self.d03_pic = "assets/images/03d.png"
        self.d04_pic = "assets/images/04d.png"
        self.d09_pic = "assets/images/09d.png"
        self.d10_pic = "assets/images/10d.png"
        self.n10_pic = "assets/images/10n.png"
        self.d11_pic = "assets/images/11d.png"
        self.d13_pic = "assets/images/13d.png"
        self.d50_pic = "assets/images/50d.png"
        self.patchy_rain = tk.PhotoImage(file="assets/images/patchy_rain.png")
        self.patchy_snow = tk.PhotoImage(file="assets/images/patchy_snow.png")
        self.cloudy_icon = tk.PhotoImage(file="assets/images/cloudy.png")
        self.sleet = tk.PhotoImage(file="assets/images/sleet.png")
        self.light_sleet = tk.PhotoImage(file="assets/images/light_sleet.png")
        self.patchy_freezing_drizzle = tk.PhotoImage(file="assets/images/patchy_freezing_drizzle.png")
        self.blowing_snow = tk.PhotoImage(file="assets/images/blowing_snow.png")
        self.fog = tk.PhotoImage(file="assets/images/fog.png")
        self.freezing_fog = tk.PhotoImage(file="assets/images/freezing_fog.png")
        self.drizzle = tk.PhotoImage(file="assets/images/drizzle.png")
        self.light_drizzle = tk.PhotoImage(file="assets/images/light_drizzle.png")
        self.freezing_drizzle = tk.PhotoImage(file="assets/images/freezing_drizzle.png")
        self.heavy_freezing_drizzle = tk.PhotoImage(file="assets/images/heavy_freezing_drizzle.png")
        self.light_rain = tk.PhotoImage(file="assets/images/light_rain.png")
        self.heavy_rain = tk.PhotoImage(file="assets/images/heavy_rain.png")
        self.light_freezing_rain = tk.PhotoImage(file="assets/images/light_freezing_rain.png")
        self.mod_heavy_freezing_rain = tk.PhotoImage(file="assets/images/light_heavy_freezing_rain.png")
        self.light_snow = tk.PhotoImage(file="assets/images/light_snow.png")
        self.moderate_snow = tk.PhotoImage(file="assets/images/moderate_snow.png")
        self.heavy_snow = tk.PhotoImage(file="assets/images/heavy_snow.png")
        self.ice_pellets = tk.PhotoImage(file="assets/images/ice_pellets.png")
        self.torrential_rain = tk.PhotoImage(file="assets/images/torrential_rain.png")
        self.light_snow_shower = tk.PhotoImage(file="assets/images/light_snow_shower.png")
        self.heavy_snow_shower = tk.PhotoImage(file="assets/images/heavy_snow_shower.png")
        self.light_rain_with_thunder = tk.PhotoImage(file="assets/images/light_rain_with_thunder.png")
        self.heavy_rain_with_thunder = tk.PhotoImage(file="assets/images/heavy_rain_with_thunder.png")
        self.snow_with_thunder = tk.PhotoImage(file="assets/images/snow_with_thunder.png")
        self.blizzard_pic = "assets/images/blizzard.png"
        # Dictionary matching current weather temperature to an image.
        self.weather_pictures_dict = {"01d":self.d01_pic,"01n":self.n01_pic,"02d":self.d02_pic,"02n":self.n02_pic,
                                 "03d":self.d03_pic,"03n":self.d03_pic,"04d":self.d04_pic,"04n":self.d04_pic,
                                      "09d":self.d09_pic,"09n":self.d09_pic,"10d":self.d10_pic,
                                 "10n":self.n10_pic,"11d":self.d11_pic,"11n":self.d11_pic,"13d":self.d13_pic,
                                      "13n":self.d13_pic,"50d":self.d50_pic,"50n":self.d50_pic}
        self.weather_pictures_dict_photoimage = {"01d":tk.PhotoImage(file=self.d01_pic).subsample(6,6),
                                                 "01n":tk.PhotoImage(file=self.n01_pic).subsample(6,6),
                                                "02d":tk.PhotoImage(file=self.d02_pic).subsample(6,6),
                                                 "02n":tk.PhotoImage(file=self.n02_pic).subsample(6,6),
                                 "03d":tk.PhotoImage(file=self.d03_pic).subsample(6,6),
                                                 "03n":tk.PhotoImage(file=self.d03_pic).subsample(6,6),
                                        "04d":tk.PhotoImage(file=self.d04_pic).subsample(6,6),
                                                 "04n":tk.PhotoImage(file=self.d04_pic).subsample(6,6),
                                      "09d":tk.PhotoImage(file=self.d09_pic).subsample(6,6),
                                                 "09n":tk.PhotoImage(file=self.d09_pic).subsample(6,6),
                                                 "10d":tk.PhotoImage(file=self.d10_pic).subsample(6,6),
                                 "10n":tk.PhotoImage(file=self.n10_pic).subsample(6,6),
                                                 "11d":tk.PhotoImage(file=self.d11_pic).subsample(6,6),
                                                 "11n":tk.PhotoImage(file=self.d11_pic).subsample(6,6),
                                                 "13d":tk.PhotoImage(file=self.d13_pic).subsample(6,6),
                                      "13n":tk.PhotoImage(file=self.d13_pic).subsample(6,6),
                                                 "50d":tk.PhotoImage(file=self.d50_pic).subsample(6,6),
                                                 "50n":tk.PhotoImage(file=self.d50_pic).subsample(6,6)}
        self.forecast_weather_icons_dict = {"1000d":tk.PhotoImage(file=self.d01_pic).subsample(6,6),
                                            "1000n":tk.PhotoImage(file=self.n01_pic).subsample(6,6),
                                            "1003d":tk.PhotoImage(file=self.d02_pic).subsample(6,6),
                                            "1003n":tk.PhotoImage(file=self.n02_pic).subsample(6,6),
                                            1006:self.cloudy_icon,
                                            1009:tk.PhotoImage(file=self.d04_pic).subsample(6,6),
                                            1030:tk.PhotoImage(file=self.d50_pic).subsample(6,6),
                                            1063:tk.PhotoImage(file="assets/images/patchy_rain.png"),
                                            1066:self.patchy_snow,1069:self.sleet,
                                            1072:self.patchy_freezing_drizzle,
                                            1087:tk.PhotoImage(file=self.d11_pic).subsample(7,7),
                                            1114:self.blowing_snow,1117:self.blizzard_pic,1135:self.fog,
                                            1147:self.freezing_fog,
                                            1150:self.drizzle,1153:self.light_drizzle,
                                            1168:self.freezing_drizzle,
                                            1171:self.heavy_freezing_drizzle,1180:self.patchy_rain,
                                            1183:self.light_rain,
                                            1192:self.heavy_rain,1195:self.heavy_rain,
                                            1186:tk.PhotoImage(file=self.d09_pic).subsample(6,6),
                                            1189:tk.PhotoImage(file=self.d09_pic).subsample(6,6),
                                            1198:self.light_freezing_rain,1201:self.mod_heavy_freezing_rain,
                                            1204:self.light_sleet,1207:self.sleet,1210:self.light_snow,1213:self.light_snow,
                                            1216:self.moderate_snow,1219:self.moderate_snow,1222:self.heavy_snow,
                                            1225:self.heavy_snow,1237:self.ice_pellets,1240:self.light_drizzle,
                                            1243:self.heavy_rain,1246:self.torrential_rain,1249:self.light_sleet,
                                            1252:self.sleet,1261:self.ice_pellets,1264:self.ice_pellets,
                                            1255:self.light_snow_shower,1258:self.heavy_snow_shower,
                                            1273:self.light_rain_with_thunder,1276:self.heavy_rain_with_thunder,
                                            1279:self.snow_with_thunder,1282:self.snow_with_thunder}
        self.moon_phases_dict = {"New Moon":self.moon_phase_new_moon,"Full Moon":self.moon_phase_full_moon,
                                 "Waxing Crescent":self.moon_phase_waxing_crescent,
                                 "First Quarter":self.moon_phase_first_quarter,"Waxing Gibbous":self.moon_phase_waxing_gibbous,
                                 "Waning Gibbous":self.moon_phase_waning_gibbous,"Last Quarter":self.moon_phase_last_quarter,
                                 "Waning Crescent":self.moon_phase_waning_crescent}
        self.air_quality_face_images = [self.face1,self.face2,self.face3,self.face4,self.face5]
        self.air_quality_component_names_dict = {"co":"Carbon monoxide","no":"Nitrogen monoxide","no2":"Nitrogen dioxide",
                                                 "o3":"Ozone","so2":"Sulphur dioxide","nh3":"Ammonia","pm2_5":"Fine particles matter",
                                                 "pm10":"Coarse particulate"}
        self.air_components_dict = {}
        self.time_short_form_list = ["12 am","1 am","2 am","3 am","4 am","5 am","6 am","7 am","8 am","9 am","10 am","11 am",
                                     "12 pm","1 pm","2 pm","3 pm","4 pm","5 pm","6 pm","7 pm","8 pm","9 pm","10 pm","11 pm"]
        self.forecast_button_names = ["Temperature","Wind speed","Pressure","Humidity","Precipitation","Cloud cover",
                                      "Chance of rain","Snow","Visibility","Dew point","UV"]
        self.forecast_ylabels_list = ["°F","mph","mbr","%","mm","%","%","cm","km","°C",""]
        self.temperature_forecast_list = []
        self.temperature_forecast_icon_list = []
        self.wind_forecast_list = []
        self.pressure_forecast_list = []
        self.humidity_forecast_list = []
        self.precipitation_forecast_list = []
        self.cloud_cover_forecast_list = []
        self.rain_chance_forecast_list = []
        self.snow_forecast_list = []
        self.visibility_forecast_list = []
        self.dew_point_forecast_list = []
        self.uv_forecast_list = []
        self.wind_degree_forecast_list = []
        self.forecast_obj = None
        self.historical_weather_report_obj = None
        self.previous_2days = []
        self.temperature_historical_report_list = []
        self.precipitation_historical_report_list = []
        # frame1
        self.frame1 = tk.Frame(self.root,background=self.bg_dark_color,width=1100)
        self.frame1.grid(row=0,column=0)
        self.user_input = tk.StringVar()
        self.locate_current_location_btn = tk.Button(self.frame1,image=self.location_icon,bg=self.bg_dark_color,command=lambda :self.thread_initialize_location(self.ip_address_city),bd=0,activebackground=self.bg_dark_color)
        self.locate_current_location_btn.grid(row=0,column=0)
        self.entry_field = tk.Entry(self.frame1,width=100,textvariable=self.user_input,font=("Arial",14))
        self.entry_field.grid(row=0,column=1,padx=2)
        self.recommendations = ttk.Combobox(self.frame1,state="readonly",font=("Arial",14))
        self.recommendations.bind("<<ComboboxSelected>>", self.get_user_selected_from_combobox)
        self.recommendations.grid(row=0,column=2,padx=3)
        self.search_button = tk.Button(self.frame1,text="Show Live Weather",command=self.thread_get_location_input,bg="#000000",fg="white",activebackground="#000000",activeforeground="#ffffff",relief=tk.RAISED,font=("Arial",13))
        self.search_button.grid(row=0,column=3,padx=7)
        self.root.bind("<Return>",self.shortcut_enter_button_pressed)
        self.refresh_info_buttton = tk.Button(self.frame1,text="Refresh",command=self.thread_refresh_weather_data,image=self.refresh_icon,bg=self.bg_dark_color,activebackground=self.bg_dark_color,font=("Arial",12))
        self.refresh_info_buttton.grid(row=0,column=4)
        self.temperature_unit_changing_button = tk.Button(self.frame1,text=self.temp_unit,command=self.thread_change_temperature_unit,fg="#ffffff",bg="#3682d5",activebackground="#3682d5",font=("Arial",12,"bold"),activeforeground="#000000")
        self.temperature_unit_changing_button.grid(row=0,column=5,padx=10)
        self.app_info_button = tk.Button(self.frame1,text="About",image=self.about_icon,command=self.about,bg=self.bg_dark_color,activebackground=self.bg_dark_color)
        self.app_info_button.grid(row=0,column=7,padx=30)
        # frame2
        self.frame2 = tk.Frame(self.root,background=self.bg_dark_color,width=1800)
        style = ttk.Style(self.root)
        style.theme_create(
            "name", parent="alt", settings={
                ".": {"configure": {"background": self.bg_dark_color,
                                    "relief": "flat"},
                                    "font": ("Calibri", 14)},
                "TLabel": {"configure": {"foreground": "white",
                                         "background":self.bg_dark_color,
                                         "padding": 10,
                                         "font": ("Calibri", 19)}},
                "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0],"borderwidth":0}
                              },
                "TNotebook.Tab": {
                    "configure": {"relief": "flat",
                                  "foreground":"white",
                                  "bordercolor": self.bg_dark_color,
                                  "darkcolor": self.bg_dark_color,
                                  "padding": [5, 1],
                                  "background": self.bg_dark_color,
                                  "font": ("Calibri", 14)
                                  },
                    "map": {"background": [("selected", self.bg_dark_color)],
                            "expand": [("selected", [1, 1, 1, 0])]}
                }
            })
        style.theme_use("name")
        notebook = ttk.Notebook(self.root, style='TNotebook')
        self.main_panel = tk.Frame(notebook,background=self.bg_dark_color)
        self.innerframe1 = tk.Frame(self.main_panel,background=self.bg_dark_color)
        self.innerframe1.grid(row=0,column=0,rowspan=5)
        self.innerframe2 = tk.Frame(self.main_panel,background=self.bg_dark_color)
        self.innerframe2.grid(row=0,column=1,padx=5)
        self.sub_frame1 = tk.Frame(self.innerframe1,background=self.bg_dark_color)
        self.sub_frame1.grid(row=0,column=0)
        self.canvas1 = tk.Canvas(self.sub_frame1, width=700, height=260, highlightthickness=0)
        self.canvas1.grid(row=0,column=0)
        self.scenery_canvas = self.canvas1.create_image(0, 0, image=self.night_sky_pic1, anchor=tk.NW)
        self.location_name = self.canvas1.create_text(5,10,fill="white",anchor=tk.NW,font=("Times New Roman",25))
        self.location_city_country = self.canvas1.create_text(5,45,anchor=tk.NW,fill="white",font=("Times New Roman",16))
        self.current_time = self.canvas1.create_text(5,67,anchor=tk.NW,fill="white",font=("Times New Roman",16))
        self.current_temp = self.canvas1.create_text(115,101,fill="#ffffff",anchor=tk.NW,font=("Times New Roman",49))
        self.current_feels_like_temp = self.canvas1.create_text(115,160.5,fill="#ffffff",anchor=tk.NW,font=("Times New Roman",17))
        self.weather_status = self.canvas1.create_text(115,179,fill="#ffffff",anchor=tk.NW, font=("Arial", 20))
        self.weather_description = self.canvas1.create_text(115,205,fill="#ffffff",anchor=tk.NW,font=("Times New Roman", 18))
        self.weather_current_picture = self.canvas1.create_image(10,97,anchor=tk.NW)
        self.canvas1.create_image(370,70,image=self.wind_picture,anchor=tk.NW)
        self.wind_speed = self.canvas1.create_text(410,70,fill="#ffffff",anchor=tk.NW,font=("Times New Roman",15))
        self.canvas1.create_image(370,100,image=self.pressure_icon,anchor=tk.NW)
        self.pressure = self.canvas1.create_text(410,100,fill="#ffffff",anchor=tk.NW,font=("Times New Roman",15))
        self.canvas1.create_image(370,130,image=self.humidity_icon,anchor=tk.NW)
        self.humidity_text = self.canvas1.create_text(410,130,fill="#ffffff",anchor=tk.NW,font=("Times New Roman",15))
        self.canvas1.create_image(370,160,image=self.visibility_icon,anchor=tk.NW)
        self.visibility_text = self.canvas1.create_text(410,160,fill="#ffffff",anchor=tk.NW,font=("Times New Roman",15))
        self.canvas1.create_image(370,190,image=self.dewpoint_icon,anchor=tk.NW)
        self.dew_point_text = self.canvas1.create_text(410,190,fill="#ffffff",anchor=tk.NW,font=("Times New Roman",15))
        self.sub_frame2 = tk.Frame(self.innerframe1,background=self.bg_dark_color)
        self.sub_frame2.grid(row=1, column=0)
        self.sunrise_label = tk.Label(self.sub_frame2,font=("Times New Roman",15),bg=self.bg_dark_color,fg="#ffffff",image=self.sunrise_icon,compound=tk.TOP,text="Sunrise")
        self.sunrise_label.grid(row=2,column=0)
        tk.Label(self.sub_frame2,text="",bg=self.bg_dark_color).grid(row=2,column=1,padx=35)
        self.sunset_label = tk.Label(self.sub_frame2,font=("Times New Roman",15),bg=self.bg_dark_color,fg="#ffffff",image=self.sunset_icon,compound=tk.TOP,text="Sunset")
        self.sunset_label.grid(row=2,column=2,padx=10)
        self.sunrise_time_label = tk.Label(self.sub_frame2,bg=self.bg_dark_color,fg="#ffffff",font=("Times New Roman",15))
        self.sunrise_time_label.grid(row=3,column=0)
        self.sunset_time_label = tk.Label(self.sub_frame2,bg=self.bg_dark_color,fg="#ffffff",font=("Times New Roman",15))
        self.sunset_time_label.grid(row=3,column=2)
        self.moonrise_label = tk.Label(self.sub_frame2,text="Moon rise",image=self.moon_rise_icon,compound=tk.TOP,bg=self.bg_dark_color,fg="#ffffff",font=("Times New Roman",15))
        self.moonrise_label.grid(row=2,column=5,padx=10)
        tk.Label(self.sub_frame2, text="", bg=self.bg_dark_color).grid(row=2, column=6, padx=35)
        self.moonset_label = tk.Label(self.sub_frame2,text="Moon set",image=self.moon_set_icon,compound=tk.TOP,bg=self.bg_dark_color,fg="#ffffff",font=("Times New Roman",15))
        self.moonset_label.grid(row=2,column=7)
        self.moonrise_time_label = tk.Label(self.sub_frame2, bg=self.bg_dark_color,fg="#ffffff",font=("Times New Roman",15))
        self.moonrise_time_label.grid(row=3, column=5)
        self.moonset_time_label = tk.Label(self.sub_frame2, bg=self.bg_dark_color,fg="#ffffff",font=("Times New Roman",15))
        self.moonset_time_label.grid(row=3, column=7)
        self.sub_frame3 = tk.Frame(self.innerframe1,background="#3682d5",pady=5)
        self.sub_frame3.grid(row=2, column=0)
        tk.Label(self.sub_frame3,text="Air Quality Index",font=("Times New Roman",19,"bold"),bg="#3682d5",fg="#000000").grid(row=0,column=0,columnspan=2)
        self.air_quality_label = tk.Label(self.sub_frame3,font=("Times New Roman",19),padx=10,bg="#3682d5",fg="#000000")
        self.air_quality_label.grid(row=1,column=0)
        self.airquality_canvas = tk.Canvas(self.sub_frame3,width=50,height=50,bg=self.pale_blue_color,highlightbackground="#3682d5",bd=0)
        self.airquality_canvas.grid(row=1,column=1)
        self.airquality_frame = tk.Frame(self.sub_frame3,bg=self.pale_blue_color)
        self.airquality_frame.grid(row=2,column=0,columnspan=2,padx=5)
        self.circle_image = self.airquality_canvas.create_oval(10,10,40,40,fill="#3682d5",outline="")
        tk.Label(self.sub_frame3,text="UV Index",font=("Times New Roman",19,"bold"),bg="#3682d5",fg="#000000").grid(row=0,column=2,columnspan=12,padx=15)
        self.uv_index_label = tk.Label(self.sub_frame3,font=("Times New Roman",18),bg="#3682d5")
        self.uv_index_label.grid(row=1,column=2,columnspan=12)
        self.uv_graph_frame = tk.Frame(self.sub_frame3,bg="#3682d5")
        self.uv_graph_frame.grid(row=2, column=2, columnspan=2,padx=2)
        self.sub_frame4 = tk.Frame(self.innerframe1, background=self.bg_dark_color,width=self.innerframe1.winfo_width())
        self.sub_frame4.grid(row=3, column=0)
        tk.Label(self.sub_frame4,text="Moon phase",font=("Arial",19),bg=self.bg_dark_color,fg="#ffffff").grid(row=0,column=0,pady=5)
        self.moon_phase_label = tk.Label(self.sub_frame4,font=("Times New Roman",18),bg=self.bg_dark_color,fg="#ffffff",height=100,padx=15)
        self.moon_phase_label.grid(row=1,column=0,pady=5)
        tk.Label(self.sub_frame4,text="Fact",bg=self.bg_dark_color,fg="#ffffff",font=("Arial",19),image=self.fact_bulb_icon,compound=tk.LEFT).grid(row=0,column=1)
        self.fun_fact_label = tk.Label(self.sub_frame4,text="",fg="#ffffff",bg=self.bg_dark_color,font=("Times New Roman",15),wraplength=500)
        self.fun_fact_label.grid(row=1,column=1,columnspan=3)
        self.uv_hourly_frame = tk.Frame(self.uv_graph_frame,background=self.bg_dark_color)
        self.uv_hourly_frame.grid(row=1,column=1)
        self.forecast_frame = tk.Frame(self.innerframe2,background=self.bg_dark_color)
        self.forecast_frame.grid(row=0, column=0)
        self.forecast_sub_frame1 = tk.Frame(self.forecast_frame,background=self.bg_dark_color)
        self.forecast_sub_frame1.pack()
        tk.Label(self.forecast_sub_frame1, text="Hourly forecast", font=("Arial", 20),bg=self.bg_dark_color,fg="#ffffff").grid(row=0, column=0,columnspan=10)
        self.hourly_forecast_labels_array = []
        self.hourly_forecast_temp_labels_array = []
        for num in range(10):
            hour_label = tk.Label(self.forecast_sub_frame1,font=("Times New Roman",20),image=self.thermometer_pic,compound=tk.BOTTOM,bg=self.bg_dark_color,fg="#ffffff")
            hour_label.grid(row=1,column=num)
            self.hourly_forecast_labels_array.append(hour_label)
            temp_label = tk.Label(self.forecast_sub_frame1,font=("Times New Roman",19),text=" ",bg=self.bg_dark_color,fg="#ffffff")
            temp_label.grid(row=2,column=num)
            self.hourly_forecast_temp_labels_array.append(temp_label)
        self.graph_frame = tk.Frame(self.forecast_sub_frame1)
        self.graph_frame.grid(row=3,column=0,columnspan=11)
        tk.Canvas(self.graph_frame,width=500,height=430).grid(row=0,column=0)
        self.forecast_sub_frame2 = tk.Frame(self.forecast_frame,background=self.bg_dark_color)
        self.forecast_sub_frame2.pack()
        tk.Label(self.forecast_sub_frame2,text="5 days forecast",font=("Times New Roman",16,"bold"),fg="#ffffff").grid(row=0,column=0,columnspan=5)
        for _ in range(5):
            tk.Label(self.forecast_sub_frame2,text="").grid(row=_+1,column=0)
        self.daily_hourly_forecast_main_panel = tk.Frame(notebook,background=self.bg_dark_color)
        self.history_main_panel = tk.Frame(notebook,background=self.bg_dark_color)
        self.wind_direction_speed_main_panel = tk.Frame(notebook,background=self.bg_dark_color)
        # Icons to display on tab of notebook tabs.
        clock_icon = Image.open('assets/images/icons8-clock-30.png')
        clock_icon = ImageTk.PhotoImage(clock_icon)
        home_icon = Image.open("assets/images/icons8-home-30.png")
        home_icon = ImageTk.PhotoImage(home_icon)
        history_icon = Image.open("assets/images/icons8-history-30.png")
        history_icon = ImageTk.PhotoImage(history_icon)
        windsock_icon = Image.open("assets/images/windsock.png")
        windsock_icon= ImageTk.PhotoImage(windsock_icon)
        # Adding tabs to notebook.
        notebook.add(self.main_panel,text="Home",image=home_icon,compound=tk.LEFT)
        notebook.add(self.daily_hourly_forecast_main_panel,text="Forecast",image=clock_icon,compound=tk.LEFT)
        notebook.add(self.history_main_panel,text="History",image=history_icon,compound=tk.LEFT)
        notebook.add(self.wind_direction_speed_main_panel,text="Wind direction",image=windsock_icon,compound=tk.LEFT)
        notebook.grid(row=1, column=0, sticky="nw")
        # Setting icon for app in title bar.
        self.root.iconphoto(True,self.app_icon_image)
        # Starts the application by finding the current weather of user's location based on user's public IP address.
        self.thread_detect_user_current_location_by_ip_address()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    # Function to refresh the currently displaying city's weather data.
    def refresh_weather_data(self):
        try:
            self.get_user_selected_from_combobox(event="<<<ComboBoxSelected>>>")
        except:
            messagebox.showerror("No Internet connection","Kindly connect this device to the Internet")
          
    def thread_refresh_weather_data(self):
        thread_refresh_weather = Thread(target=self.refresh_weather_data())
        thread_refresh_weather.start()

    # Function to run when user selects any city from the combobox containing names of cities with same names in different locations.
    def get_user_selected_from_combobox(self,event):
        self.last_selected_city_lat_lon = self.lon_lat_list_different_locations[self.recommendations.current()]
        self.thread_fetch_current_weather_location(self.lon_lat_list_different_locations[self.recommendations.current()])
    def get_location_input(self):
        user_input_location = self.user_input.get()
        try:
            response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={user_input_location}&limit={20}&appid={self.my_api_key}")
            obj = json.loads(response.content)
            if len(obj)==0 or user_input_location=="":
                messagebox.showinfo("Invalid location","Please enter a valid city or town name")
                self.recommendations.set(value="")
                self.recommendations.config(values=[])
            elif response.status_code==200:
                self.different_locations_list = []
                self.lon_lat_list_different_locations = []
                for word in obj:
                    display_word = word['name']+","
                    if "state" in word:
                        display_word += word['state']+","
                    display_word += word['country']
                    self.different_locations_list.append(display_word)
                    arr = []
                    arr.append(word['lat'])
                    arr.append(word['lon'])
                    self.lon_lat_list_different_locations.append(arr)
                self.recommendations.set(value=self.different_locations_list[0])
                self.recommendations.config(values=self.different_locations_list)
                self.last_selected_city_lat_lon = [self.lon_lat_list_different_locations[0][0],
                                                   self.lon_lat_list_different_locations[0][1]]
                self.thread_fetch_current_weather_location([self.lon_lat_list_different_locations[0][0],self.lon_lat_list_different_locations[0][1]])
        except:
            messagebox.showerror("No Internet Connection","Your device is not connected to the Internet.\nKindly connect to an Internet to use this application.")

    def thread_get_location_input(self):
        thread_var = Thread(target=self.get_location_input())
        thread_var.start()

    # Function to fetch the weather data of given latitude and longitude.
    def fetch_current_weather_location(self,confirmed_location):
        try:
            current_weather_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={confirmed_location[0]}&lon={confirmed_location[1]}&units={self.temperature_unit_string}&APPID={self.my_api_key}")
            if current_weather_response.status_code==200:
                obj = json.loads(current_weather_response.content)
                weather_pic = obj['weather'][0]['icon']
                self.current_weather_icon_code = weather_pic
                # Setting background image for dashboard based on day or night, sunny/cloudy or rainy weather conditions.
                if weather_pic[2]=="d":  # When the current time is day.
                    # When the weather condition is normal, set a day time sky picture as background of dashboard.
                    self.canvas1.itemconfig(self.scenery_canvas,image=self.day_sky_pic1)
                    if int(obj['weather'][0]['id'])>800:
                        # If current weather condition is cloudy.
                        self.canvas1.itemconfig(self.scenery_canvas,image=self.cloudy_day_pic1)
                    elif int(obj["weather"][0]["id"])==781:
                        # If current weather condition is tornado.
                        self.canvas1.itemconfig(self.scenery_canvas,image=self.tornado_day_night_pic1)
                    elif int(obj["weather"][0]["id"])>=600 and int(obj["weather"][0]["id"])<=622:
                        # If current weather condition is snowing.
                        self.canvas1.itemconfig(self.scenery_canvas,image=self.snowy_day_pic1)
                    elif int(obj['weather'][0]['id'])>=500 and int(obj['weather'][0]['id'])<=531:
                        # If current weather condition is rainy.
                        self.canvas1.itemconfig(self.scenery_canvas, image=self.rainy_day_pic1)
                    elif int(obj['weather'][0]['id'])>=300 and int(obj['weather'][0]['id'])<=321:
                        # If current weather condition is drizzle.
                        self.canvas1.itemconfig(self.scenery_canvas, image=self.drizzle_day_pic1)
                    elif int(obj['weather'][0]['id'])>=200 and int(obj['weather'][0]['id'])<=232:
                        # If current weather condition is thunderstorm.
                        self.canvas1.itemconfig(self.scenery_canvas, image=self.thunderstorm_day_pic1)
                else: # If current time is night.
                    self.canvas1.itemconfig(self.scenery_canvas,image=self.night_sky_pic1)
                    if int(obj["weather"][0]["id"])==781: # Tornado
                        self.canvas1.itemconfig(self.scenery_canvas,image=self.tornado_day_night_pic1)
                    elif int(obj['weather'][0]['id'])>=500 and int(obj['weather'][0]['id'])<=531:
                        # If current weather condition is rainy.
                        self.canvas1.itemconfig(self.scenery_canvas,image=self.rainy_night_pic1)
                    elif int(obj['weather'][0]['id'])>=300 and int(obj['weather'][0]['id'])<=321:
                        # If current weather condition is drizzling.
                        self.canvas1.itemconfig(self.scenery_canvas, image=self.drizzle_day_pic1)
                    elif int(obj['weather'][0]['id'])>=200 and int(obj['weather'][0]['id'])<=232:
                        # If current weather condition is thunderstorm.
                        self.canvas1.itemconfig(self.scenery_canvas, image=self.thunderstorm_day_night_pic1)
                self.canvas1.itemconfig(self.location_name,text=obj['name'])
                self.canvas1.itemconfig(self.current_temp,text=str(obj['main']['temp'])+"°"+self.temp_unit)
                self.canvas1.itemconfig(self.current_feels_like_temp,text="Feels like "+str(obj['main']['feels_like'])+"°"+self.temp_unit)
                self.canvas1.itemconfig(self.weather_status,text=obj['weather'][0]['main'])
                self.canvas1.itemconfig(self.weather_description,text=obj['weather'][0]['description'])
                imageobject = Image.open(self.weather_pictures_dict.get(weather_pic))
                imageobject = imageobject.resize((100,100))
                weather_current_picture_fetched = ImageTk.PhotoImage(imageobject)
                self.canvas1.itemconfig(self.weather_current_picture,image=weather_current_picture_fetched)
                label2 = tk.Label(self.innerframe2,image=weather_current_picture_fetched)
                label2.image=weather_current_picture_fetched
                self.root.update()
                if self.temp_unit=="F":
                    self.canvas1.itemconfig(self.wind_speed,text="Wind speed: "+str(obj['wind']['speed'])+" mi/h")
                elif self.temp_unit=="C":
                    self.canvas1.itemconfig(self.wind_speed, text="Wind speed: " + str(obj['wind']['speed']) + " m/sec")
                self.canvas1.itemconfig(self.pressure, text="Pressure: "+str(obj['main']['pressure'])+" hPa")
                self.canvas1.itemconfig(self.humidity_text,text="Humidity: "+str(obj['main']['humidity'])+"%")
                self.canvas1.itemconfig(self.visibility_text,text="Visibility: "+str(obj['visibility']//1000)+" km")
                self.sunrise_time_label.config(text=str(datetime.fromtimestamp(int(obj['sys']['sunrise'])))[11:16])
                self.sunset_time_label.config(text=str(datetime.fromtimestamp(int(obj['sys']['sunset'])))[11:16])
                airquality_response = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={confirmed_location[0]}&lon={confirmed_location[1]}&appid={self.my_api_key}")
                if airquality_response.status_code==200:
                    air_quality_obj = json.loads(airquality_response.content)
                    current_air_quality_index = air_quality_obj['list'][0]['main']['aqi']
                    self.air_components_dict = air_quality_obj.get('list')[0]['components']
                    self.thread_show_air_quality_data(self.air_components_dict)
                    self.air_quality_label.config(text=self.air_quality_values[current_air_quality_index-1],image=self.air_quality_face_images[current_air_quality_index-1],compound=tk.LEFT)
                    self.airquality_canvas.itemconfig(self.circle_image,fill=self.air_quality_colors[current_air_quality_index-1])
                else:
                    self.air_quality_label.config(text="Unable to fetch data. Try again later!")
                # Hourly forecast in 3 hour interval.
                self.root.update()
                hourly_forecast_response = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?lat={confirmed_location[0]}&lon={confirmed_location[1]}&units={self.temperature_unit_string}&limit=10,&appid={self.my_api_key}")
                hourly_forecast_obj = json.loads(hourly_forecast_response.content)
                next_ten_3hour_temperature_array = []
                next_ten_3hour_times_array = []
                for num in range(10):
                    every = hourly_forecast_obj['list'][num]
                    hourly_weather_icon = every['weather'][0]['icon']
                    self.hourly_forecast_labels_array[num].config(text=str(every['dt_txt'][10:16]),compound=tk.BOTTOM,image=self.weather_pictures_dict_photoimage.get(hourly_weather_icon))
                    self.hourly_forecast_temp_labels_array[num].config(text=str(every['main']['temp'])+"°"+self.temp_unit,padx=3)
                    next_ten_3hour_temperature_array.append(every['main']['temp'])
                    next_ten_3hour_times_array.append(str(every['dt_txt'][11:16]))
                self.thread_plot_hourly_temperature_bar_chart(next_ten_3hour_temperature_array,next_ten_3hour_times_array)
                self.root.update()
                # Delete all widgets in frame 'forecast_sub_frame2'.
                for widget in self.forecast_sub_frame2.winfo_children():
                    widget.destroy()
                tk.Label(self.forecast_sub_frame2, text="Next 3 days forecast", font=("Arial", 19),bg=self.bg_dark_color,fg="#ffffff").grid(row=0,
                                                                                                              column=0,
                                                                                                              columnspan=5,pady=3)
                astronomy_response = self.fetch_astronomy_data(confirmed_location)
                astronomy_obj = json.loads(astronomy_response)
                self.canvas1.itemconfig(self.location_city_country, text=astronomy_obj["location"]["region"]+","+astronomy_obj["location"]["country"])
                self.canvas1.itemconfig(self.current_time,text="Local time: "+astronomy_obj["location"]["localtime"][-5:])
                self.moonrise_time_label.config(text=self.change_to_24_hour_format(astronomy_obj["astronomy"]["astro"]["moonrise"]))
                self.moonset_time_label.config(text=self.change_to_24_hour_format(astronomy_obj["astronomy"]["astro"]["moonset"]))
                self.moon_phase_label.config(text=str(astronomy_obj["astronomy"]["astro"]["moon_phase"])+"\n"+"Illumination "+str(astronomy_obj["astronomy"]["astro"]["moon_illumination"])+" %",image=self.moon_phases_dict.get(astronomy_obj["astronomy"]["astro"]["moon_phase"]),compound=tk.RIGHT)
                self.thread_fetch_more_current_weather_details(confirmed_location)
                self.thread_fetch_hourly_uv_data(confirmed_location)
                self.thread_show_forecast_frame()
                self.fetch_previous_two_days_weather_report(confirmed_location)
                self.show_historical_report_frame()
                full_location = obj['name']+astronomy_obj["location"]["region"]+","+astronomy_obj["location"]["country"]
                self.thread_generate_fun_fact(full_location)
                self.thread_show_wind_direction_frame()
            else:
                messagebox.showinfo("Error","Some error occurred. Please try again later!")
        except:
            messagebox.showerror("No Internet connection", "Your device is not connected to the Internet")

    def thread_fetch_current_weather_location(self,confirmed_location):
        thread_var = Thread(target=self.fetch_current_weather_location(confirmed_location))
        thread_var.start()

    # Function to visualize the hourly temperature forecast in 3 hour interval using line chart.
    def plot_hourly_temperature_bar_chart(self,temperature_list, labels_arr):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        fig = Figure(figsize=(11.5, 5), dpi=100)
        # adding the subplot
        plot1 = fig.add_subplot(111,facecolor =self.bg_dark_color)
        fig.suptitle("Hourly temperature", fontsize=14)
        numpy_temperature_array = np.array(temperature_list)
        for ptr in range(len(labels_arr)):
            if labels_arr[ptr]=="00:00":
                labels_arr[ptr] = "12 am"
            elif labels_arr[ptr]=="03:00":
                labels_arr[ptr] = "3 am"
            elif labels_arr[ptr]=="06:00":
                labels_arr[ptr] = "6 am"
            elif labels_arr[ptr]=="09:00":
                labels_arr[ptr] = "9 am"
            elif labels_arr[ptr]=="12:00":
                labels_arr[ptr] = "12 pm"
            elif labels_arr[ptr]=="15:00":
                labels_arr[ptr] = "3 pm"
            elif labels_arr[ptr]=="18:00":
                labels_arr[ptr] = "6 pm"
            elif labels_arr[ptr]=="21:00":
                labels_arr[ptr] = "9 pm"
        ptr = 9
        while ptr>=0:
            if labels_arr[ptr] in labels_arr and labels_arr.index(labels_arr[ptr])!=ptr:
                labels_arr[ptr] +="\n (Next)"
            else:
                labels_arr[ptr] += "\n (Today)"
            ptr = ptr-1
        # plotting the graph
        plot1.plot(labels_arr,numpy_temperature_array,linestyle="dashed",color="white",marker="o",ms=10)
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        # placing the canvas on the Tkinter window.
        canvas.get_tk_widget().pack()

    def thread_plot_hourly_temperature_bar_chart(self,arr1,labels_arr):
        thread_var = Thread(target=self.plot_hourly_temperature_bar_chart(arr1,labels_arr))
        thread_var.start()

    def fetch_astronomy_data(self,confirmed_location):
        today_date = str(datetime.now())[:10]
        astronomy_response = requests.get(f"https://api.weatherapi.com/v1/astronomy.json?key={self.my_weatherapi_key}&q={confirmed_location[0]},{confirmed_location[1]}&dt={today_date}")
        if astronomy_response.status_code == 200:
            return astronomy_response.content
        elif astronomy_response.status_code>=400 and astronomy_response.status_code<500:
            messagebox.showerror("Some error occurred","Try again after some time")

    def fetch_more_current_weather_details(self,confirmed_location):
        try:
            weather_response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={self.my_weatherapi_key}&q={confirmed_location[0]},{confirmed_location[1]}&aqi=no")
            if weather_response.status_code==200:
                weather_details = json.loads(weather_response.content)
                self.canvas1.itemconfig(self.dew_point_text,text="Dew point: "+str(weather_details["current"]["dewpoint_c"])+"°C")
                uv_index_value = weather_details["current"]["uv"]
                if uv_index_value >= 0 and uv_index_value <= 2:
                    self.uv_index_label.config(text=str(uv_index_value)+"\n"+self.uv_index_tips_list[0])
                elif uv_index_value>=3 and uv_index_value<=7:
                    self.uv_index_label.config(text=str(uv_index_value)+"\n"+self.uv_index_tips_list[1])
                elif uv_index_value>=8:
                    self.uv_index_label.config(text=str(uv_index_value)+"\n"+self.uv_index_tips_list[2])
            elif weather_response.status_code>=400 and weather_response.status_code<500:
                messagebox.showerror("Some error","Try again")
        except:
            messagebox.showerror("No Internet connection", "Your device is not connected to the Internet")

    def thread_fetch_more_current_weather_details(self,confirmed_location):
        thread_var = Thread(target=self.fetch_more_current_weather_details(confirmed_location))
        thread_var.start()
      
    # Function to fetch forecast data for 3 days in JSON format from weatherapi.
    def fetch_hourly_uv_data(self,confirmed_location):
        try:
            forecast_response = requests.get(f"https://api.weatherapi.com/v1/forecast.json?key={self.my_weatherapi_key}&q={confirmed_location[0]},{confirmed_location[1]}&days=3&aqi=no&alerts=no")
            if forecast_response.status_code==200:
                self.forecast_obj = json.loads(forecast_response.content)
                uv_arr_list = self.forecast_obj["forecast"]["forecastday"][0]["hour"]
                current_day_uv_hourly_list = []
                index_num = 0
                for every_hour_uv in uv_arr_list:
                    if index_num%2==1:
                        current_day_uv_hourly_list.append(every_hour_uv["uv"])
                    index_num += 1
                self.thread_plot_hourly_uv_index(current_day_uv_hourly_list)
                self.thread_get_next_3_days_overall_temperature_details()

        except:
            messagebox.showerror("Some error occurred","Please try again after sometime.")
          
    def thread_fetch_hourly_uv_data(self,confirmed_location):
        thread_var = Thread(target=self.fetch_hourly_uv_data(confirmed_location))
        thread_var.start()

    # Function to draw bar chart for today's UV index in 24 hours format in 2 hours forecast.
    def plot_hourly_uv_index(self,uv_index_list):
        for widget in self.uv_hourly_frame.winfo_children():
            widget.destroy()
        fig = Figure(figsize=(7.6, 4), dpi=60)
        fig.suptitle("Hourly UV index",fontsize=12)
        # adding the subplot
        plot1 = fig.add_subplot(111,facecolor = self.pale_blue_color)
        numpyarr = np.array(uv_index_list)
        labels_arr = ["1 am","3 am","5 am","7 am","9 am","11 am","1 pm","3 pm","5 pm","7 pm","9 pm","11 pm"]
        colors_arr = ["red" if uv_value>7 else "orange" if (uv_value>=5 and uv_value<=7) else "yellow" if (uv_value>=3 and uv_value<5) else "green" for uv_value in numpyarr]
        # plotting the graph
        plot1.bar(labels_arr,numpyarr,width=0.4,color=colors_arr)
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self.uv_hourly_frame)
        canvas.draw()
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

    def thread_plot_hourly_uv_index(self,uv_index_list):
        thread_var = Thread(target=self.plot_hourly_uv_index(uv_index_list))
        thread_var.start()
      
    def change_to_24_hour_format(self,timestamp):
        if timestamp[6:]=="PM":
            timestamp = str(12+int(timestamp[0:2]))+timestamp[2:5]
            return timestamp
        else:
            timestamp = str(timestamp[0:5])
            return timestamp
          
    def initialize_location(self,user_ip_address_city):
        try:
            self.entry_field.delete(0,tk.END)
            self.entry_field.insert(0,user_ip_address_city)
            self.search_button.invoke()
        except:
            messagebox.showerror("No Internet connection","Your device is not connected to the Internet")
          
    def thread_initialize_location(self,user_ip_address_city):
        thread_var = Thread(target=self.initialize_location(user_ip_address_city))
        thread_var.start()

    def shortcut_enter_button_pressed(self,event):
        self.search_button.invoke()

    # Function to get the IP address of user based on user's WIFI network.
    def detect_user_current_location_by_ip_address(self):
        try:
            self.user_IP_Address = requests.get('https://checkip.amazonaws.com').text.strip()
            self.ip_api_key = "ef60678c-457a-469e-ac10-6063b1b91636"
            self.ip_response = requests.get(
                f"https://apiip.net/api/check?ip={self.user_IP_Address}&accessKey={self.ip_api_key}")
            self.ip_address_city = "Delhi"
            # If fetching is success, assign the location found by fetching to the variable 'self.ip_address_city'.
            if self.ip_response.status_code == 200:
                self.ip_address_obj = json.loads(self.ip_response.content)
                self.ip_address_city = self.ip_address_obj["city"]
            self.thread_initialize_location(self.ip_address_city)
        except:
            messagebox.showerror("No Internet connection","Please connect your device to the Internet")

    def thread_detect_user_current_location_by_ip_address(self):
        thread_var = Thread(target=self.detect_user_current_location_by_ip_address())
        thread_var.start()

    # Function to change temperature units from fahrenheit to celsius and vice versa.
    def change_temperature_unit(self):
        if self.temp_unit=="F":
            self.temp_unit = "C"
            self.temperature_unit_string = "metric"
            self.temperature_unit_changing_button.config(text="C")
            self.forecast_ylabels_list[0] = "°C"
        else:
            self.temp_unit = "F"
            self.temperature_unit_string = "imperial"
            self.temperature_unit_changing_button.config(text="F")
            self.forecast_ylabels_list[0] = "°F"
        self.root.update()
        self.thread_refresh_weather_data()
      
    def thread_change_temperature_unit(self):
        thread_var = Thread(target=self.change_temperature_unit())
        thread_var.start()

    def start_over_airquality_frame(self):
        for widget in self.airquality_frame.winfo_children():
            widget.destroy()

    # Function to display today's air pollutant details.
    def show_air_quality_data(self,air_components_dict):
        self.start_over_airquality_frame()
        for every_component in self.air_components_dict.keys():
            pollutant_name = self.air_quality_component_names_dict.get(every_component)
            tk.Label(self.airquality_frame,
                     text=f"{pollutant_name}: {self.air_components_dict.get(every_component)} μg/m3",fg="#ffffff",bg=self.pale_blue_color,font=("Times New Roman",16)).pack()

    def thread_show_air_quality_data(self,air_components_dict):
        thread_var = Thread(target=self.show_air_quality_data(air_components_dict))
        thread_var.start()

    # Function to process the hourly forecast data fetched from WeatherAPI.
    def process_weather_forecast(self,future_response_object):
        # This fetches weather forecast for the next 3 days including today.
        day_one = future_response_object["forecast"]["forecastday"][0]["hour"]
        day_two = future_response_object["forecast"]["forecastday"][1]["hour"]
        day_three = future_response_object["forecast"]["forecastday"][2]["hour"]
        # Get the date of the 3 days in string datatype.
        self.future_forecast_days = [str(future_response_object["forecast"]["forecastday"][0]["date"]),
                                     str(future_response_object["forecast"]["forecastday"][1]["date"]),
                                     str(future_response_object["forecast"]["forecastday"][2]["date"])]
        # Convert the dates in string datatype to days of the week.
        self.future_forecast_days = self.convert_date_to_day(self.future_forecast_days)
        self.root.update()
        # Clear all elements from the arrays to insert new data.
        self.temperature_forecast_list.clear()
        self.temperature_forecast_list = [[],[],[]]
        self.temperature_forecast_icon_list.clear()
        self.temperature_forecast_icon_list = [[],[],[]]
        self.wind_forecast_list.clear()
        self.wind_forecast_list = [[],[],[]]
        self.pressure_forecast_list.clear()
        self.pressure_forecast_list = [[],[],[]]
        self.humidity_forecast_list.clear()
        self.humidity_forecast_list = [[],[],[]]
        self.precipitation_forecast_list.clear()
        self.precipitation_forecast_list = [[],[],[]]
        self.cloud_cover_forecast_list.clear()
        self.cloud_cover_forecast_list = [[],[],[]]
        self.rain_chance_forecast_list.clear()
        self.rain_chance_forecast_list = [[],[],[]]
        self.snow_forecast_list.clear()
        self.snow_forecast_list = [[],[],[]]
        self.visibility_forecast_list.clear()
        self.visibility_forecast_list = [[],[],[]]
        self.dew_point_forecast_list.clear()
        self.dew_point_forecast_list = [[],[],[]]
        self.uv_forecast_list.clear()
        self.uv_forecast_list = [[],[],[]]
        self.wind_degree_forecast_list.clear()
        self.wind_degree_forecast_list = [[],[],[]]
        for every_hour in day_one:
            if self.temp_unit=="F":
                self.temperature_forecast_list[0].append(every_hour.get("temp_f"))
            elif self.temp_unit=="C":
                self.temperature_forecast_list[0].append(every_hour.get("temp_c"))
            self.temperature_forecast_icon_list[0].append(every_hour.get("condition").get("code"))
            self.wind_forecast_list[0].append(every_hour.get("wind_mph"))
            self.pressure_forecast_list[0].append(every_hour.get("pressure_mb"))
            self.humidity_forecast_list[0].append(every_hour.get("humidity"))
            self.precipitation_forecast_list[0].append(every_hour.get("precip_mm"))
            self.cloud_cover_forecast_list[0].append(every_hour.get("cloud"))
            self.rain_chance_forecast_list[0].append(every_hour.get("chance_of_rain"))
            self.snow_forecast_list[0].append(every_hour.get("snow_cm"))
            self.visibility_forecast_list[0].append(every_hour.get("vis_km"))
            self.dew_point_forecast_list[0].append(every_hour.get("dewpoint_c"))
            self.uv_forecast_list[0].append(every_hour.get("uv"))
            self.wind_degree_forecast_list[0].append(every_hour.get("wind_degree"))
        self.root.update()
        for every_hour in day_two:
            if self.temp_unit == "F":
                self.temperature_forecast_list[1].append(every_hour.get("temp_f"))
            elif self.temp_unit == "C":
                self.temperature_forecast_list[1].append(every_hour.get("temp_c"))
            self.temperature_forecast_icon_list[1].append(every_hour.get("condition").get("code"))
            self.wind_forecast_list[1].append(every_hour.get("wind_mph"))
            self.pressure_forecast_list[1].append(every_hour.get("pressure_mb"))
            self.humidity_forecast_list[1].append(every_hour.get("humidity"))
            self.precipitation_forecast_list[1].append(every_hour.get("precip_mm"))
            self.cloud_cover_forecast_list[1].append(every_hour.get("cloud"))
            self.rain_chance_forecast_list[1].append(every_hour.get("chance_of_rain"))
            self.snow_forecast_list[1].append(every_hour.get("snow_cm"))
            self.visibility_forecast_list[1].append(every_hour.get("vis_km"))
            self.dew_point_forecast_list[1].append(every_hour.get("dewpoint_c"))
            self.uv_forecast_list[1].append(every_hour.get("uv"))
            self.wind_degree_forecast_list[1].append(every_hour.get("wind_degree"))
        self.root.update()
        for every_hour in day_three:
            if self.temp_unit == "F":
                self.temperature_forecast_list[2].append(every_hour.get("temp_f"))
            elif self.temp_unit == "C":
                self.temperature_forecast_list[2].append(every_hour.get("temp_c"))
            self.temperature_forecast_icon_list[2].append(every_hour.get("condition").get("code"))
            self.wind_forecast_list[2].append(every_hour.get("wind_mph"))
            self.pressure_forecast_list[2].append(every_hour.get("pressure_mb"))
            self.humidity_forecast_list[2].append(every_hour.get("humidity"))
            self.precipitation_forecast_list[2].append(every_hour.get("precip_mm"))
            self.cloud_cover_forecast_list[2].append(every_hour.get("cloud"))
            self.rain_chance_forecast_list[2].append(every_hour.get("chance_of_rain"))
            self.snow_forecast_list[2].append(every_hour.get("snow_cm"))
            self.visibility_forecast_list[2].append(every_hour.get("vis_km"))
            self.dew_point_forecast_list[2].append(every_hour.get("dewpoint_c"))
            self.uv_forecast_list[2].append(every_hour.get("uv"))
            self.wind_degree_forecast_list[2].append(every_hour.get("wind_degree"))
        self.root.update()
        self.thread_create_forecast_graph(self.time_short_form_list,[self.temperature_forecast_list[0],self.temperature_forecast_list[1],self.temperature_forecast_list[2]],0,self.forecast_button_names[0],self.forecast_ylabels_list[0],".",self.temperature_forecast_icon_list)

    def thread_process_weather_forecast(self,future_response_object):
        thread_var = Thread(target=self.process_weather_forecast(future_response_object))
        thread_var.start()

    # Function to draw visualization graphs based on the hourly forecast data given.
    def create_forecast_graph(self,time_arr,data_day_123,day_index,data_name,data_ylabel,marker_,temp_icons_list):
        # Clear all widgets from frame 'forecast_3_day_frame'.
        for widget in self.forecast_3_days_graph_frame.winfo_children():
            widget.destroy()
        sns.set_context("paper", font_scale=1.5)
        fig, ax = plt.subplots(figsize=(19, 6), dpi=100, facecolor=self.pale_blue_color)
        ax.set_facecolor("#c3fbf9")
        if data_name=="UV":  # Plot a bar chart if the data given is hourly UV index.
            colors_arr = ["red" if uv_value > 7 else "orange" if (uv_value >= 5 and uv_value <= 7) else "yellow" if (
                        uv_value >= 3 and uv_value < 5) else "green" for uv_value in data_day_123[day_index]]
            sns.barplot(x=time_arr,y=data_day_123[day_index],palette=colors_arr,width=0.3,legend=False,hue=time_arr)
        else: # Except UV index data, all other data given to this function is plotted as line chart.
            sns.lineplot(x=time_arr, y=data_day_123[day_index], color="blue", label=self.future_forecast_days[day_index], linestyle="dashed",marker=marker_,markersize=16).set(xlabel="Time",ylabel=data_ylabel)
            plt.legend(title=data_name)
        for widget in self.forecast_3_day_frame.winfo_children():
            widget.destroy()
        self.which_day_1_button.config(text=self.future_forecast_days[0],command=lambda :self.thread_create_forecast_graph(time_arr,data_day_123,0,data_name,data_ylabel,marker_,temp_icons_list))
        self.which_day_2_button.config(text=self.future_forecast_days[1],command=lambda :self.thread_create_forecast_graph(time_arr,data_day_123,1,data_name,data_ylabel,marker_,temp_icons_list))
        self.which_day_3_button.config(text=self.future_forecast_days[2],command=lambda :self.thread_create_forecast_graph(time_arr,data_day_123,2,data_name,data_ylabel,marker_,temp_icons_list))
        if data_name=="Pressure":
            for ptr in range(len(data_day_123[day_index])):
                sub_frame = tk.Frame(self.forecast_3_day_frame, background=self.bg_dark_color, pady=2,
                                     highlightthickness=2)
                sub_frame.grid(row=0, column=ptr, padx=2)
                tk.Label(sub_frame,text=self.time_short_form_list[ptr],bg=self.bg_dark_color,fg="#ffffff",font=("Arial",12)).pack()
                tk.Label(sub_frame, text=str(data_day_123[day_index][ptr]), font=("Arial", 12),
                         bg=self.bg_dark_color, fg="#ffffff",image=temp_icons_list,compound=tk.TOP).pack(padx=2)
        elif data_name=="Temperature":
            for ptr in range(len(data_day_123[day_index])):
                sub_frame = tk.Frame(self.forecast_3_day_frame,background=self.bg_dark_color,pady=2,highlightthickness=2)
                sub_frame.grid(row=0,column=ptr,padx=2)
                tk.Label(sub_frame,text=self.time_short_form_list[ptr],bg=self.bg_dark_color,fg="#ffffff",font=("Arial",12)).pack()
                if temp_icons_list[day_index][ptr]==1000 or temp_icons_list[day_index][ptr]==1003:
                    modifiedname = str(temp_icons_list[day_index][ptr])
                    if ptr > 6 and ptr < 19:
                        modifiedname += "d"
                    else:
                        modifiedname += "n"
                    currLbel = tk.Label(sub_frame, text=str(data_day_123[day_index][ptr]) + data_ylabel, font=("Arial", 12),
                             bg=self.bg_dark_color, fg="#ffffff",
                             image=self.forecast_weather_icons_dict.get(modifiedname), compound=tk.TOP)
                    currLbel.pack(padx=2)
                    currLbel.image=self.forecast_weather_icons_dict.get(modifiedname)
                else:
                    currLbel = tk.Label(sub_frame,text=str(data_day_123[day_index][ptr])+data_ylabel,font=("Arial",12),bg=self.bg_dark_color,fg="#ffffff",image=self.forecast_weather_icons_dict.get(temp_icons_list[day_index][ptr]),compound=tk.TOP)
                    currLbel.pack(padx=2)
                    currLbel.image=self.forecast_weather_icons_dict.get(temp_icons_list[0][ptr])
        elif data_name=="Chance of rain":
            for ptr in range(len(data_day_123[day_index])):
                sub_frame = tk.Frame(self.forecast_3_day_frame, background=self.bg_dark_color, pady=2,
                                     highlightthickness=2)
                sub_frame.grid(row=0, column=ptr, padx=2)
                tk.Label(sub_frame, text=self.time_short_form_list[ptr], bg=self.bg_dark_color, fg="#ffffff",
                         font=("Arial", 12)).pack()
                if data_day_123[day_index][ptr]==0:
                    tk.Label(sub_frame, text=str(data_day_123[day_index][ptr]) + data_ylabel, font=("Arial", 12),
                             bg=self.bg_dark_color,
                             fg="#ffffff", image=self.closed_umbrella_icon,
                             compound=tk.TOP).pack(padx=2)
                else:
                    tk.Label(sub_frame, text=str(data_day_123[day_index][ptr]) + data_ylabel, font=("Arial", 12), bg=self.bg_dark_color,
                         fg="#ffffff", image=self.open_umbrella_rain_icon,
                         compound=tk.TOP).pack(padx=2)
        else:
            for ptr in range(len(data_day_123[day_index])):
                sub_frame = tk.Frame(self.forecast_3_day_frame, background=self.bg_dark_color, pady=2, highlightthickness=2)
                sub_frame.grid(row=0, column=ptr, padx=2)
                tk.Label(sub_frame,text=self.time_short_form_list[ptr],bg=self.bg_dark_color,fg="#ffffff",font=("Arial",12)).pack(pady=2)
                tk.Label(sub_frame, text=str(data_day_123[day_index][ptr]) + data_ylabel, font=("Arial", 12), bg=self.bg_dark_color,
                     fg="#ffffff",image=temp_icons_list,compound=tk.TOP).pack(padx=2)
        self.thread_change_button_clicked_color(data_name,day_index)
        canvas = FigureCanvasTkAgg(fig, master=self.forecast_3_days_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        plt.close()  # Closes the most recently created figure
        plt.close('all')

    def thread_create_forecast_graph(self,time_arr,data_day_123,day_index,data_name,data_ylabel,marker_,temp_icons_list):
        thread_var = Thread(target=self.create_forecast_graph(time_arr,data_day_123,day_index,data_name,data_ylabel,marker_,temp_icons_list))
        thread_var.start()

    def on_closing(self):
        self.root.quit()  # Stop the mainloop
        self.root.destroy()  # Destroy the window

    def show_forecast_frame(self):
        # Delete all widgets from the frame 'daily_hourly_forecast_main_panel'.
        for widget in self.daily_hourly_forecast_main_panel.winfo_children():
            widget.destroy()
        self.forecast_innerframe1 = tk.Frame(self.daily_hourly_forecast_main_panel, background=self.bg_dark_color)
        self.forecast_innerframe1.grid(row=0, column=0)
        tk.Label(self.forecast_innerframe1,text="Hourly forecast",bg=self.bg_dark_color,fg="#ffffff",font=("Times New Roman",18,"bold")).pack()
        self.forecast_buttons_frame = tk.Frame(self.forecast_innerframe1,background=self.bg_dark_color)
        self.forecast_buttons_frame.pack(pady=7)
        self.forecast_buttons_frame_2 = tk.Frame(self.forecast_innerframe1, background=self.bg_dark_color)
        self.forecast_buttons_frame_2.pack(pady=7)
        self.forecast_3_day_frame = tk.Frame(self.forecast_innerframe1, background=self.bg_dark_color)
        self.forecast_3_day_frame.pack()
        self.forecast_button_temperature = tk.Button(self.forecast_buttons_frame,font=("Arial",14),text="Temperature",image=self.temperature_button_icon,compound=tk.LEFT,bg="purple",activebackground="purple",fg="#ffffff",padx=4,command=lambda :self.thread_create_forecast_graph(self.time_short_form_list,[self.temperature_forecast_list[0],self.temperature_forecast_list[1],self.temperature_forecast_list[2]],0,self.forecast_button_names[0],self.forecast_ylabels_list[0],".",self.temperature_forecast_icon_list))
        self.forecast_button_temperature.grid(row=0,column=0,padx=4)
        self.forecast_button_wind = tk.Button(self.forecast_buttons_frame,font=("Arial",14), text="Wind speed",padx=4,image=self.wind_button_icon,compound=tk.LEFT,bg="purple",activebackground="purple",fg="#ffffff",command=lambda :self.thread_create_forecast_graph(self.time_short_form_list,[self.wind_forecast_list[0],self.wind_forecast_list[1],self.wind_forecast_list[2]],0,self.forecast_button_names[1],self.forecast_ylabels_list[1],".",self.wind_button_icon))
        self.forecast_button_wind.grid(row=0, column=1,padx=4)
        self.forecast_button_pressure= tk.Button(self.forecast_buttons_frame,font=("Arial",14),text="Pressure", image=self.pressure_button_icon,compound=tk.LEFT
                                                 ,bg="purple",activebackground="purple" ,fg="#ffffff",padx=4,
                                              command=lambda: self.thread_create_forecast_graph(
                                                  self.time_short_form_list, [self.pressure_forecast_list[0],
                                                  self.pressure_forecast_list[1], self.pressure_forecast_list[2]],0,
                                                  self.forecast_button_names[2], self.forecast_ylabels_list[2],
                                                  ".",self.pressure_button_icon))
        self.forecast_button_pressure.grid(row=0, column=2, padx=4)
        self.forecast_button_humidity = tk.Button(self.forecast_buttons_frame,font=("Arial",14),text="Humidity", bg="purple",
                                                  fg="#ffffff",activebackground="purple",padx=4,
                                                  command=lambda: self.thread_create_forecast_graph(
                                                      self.time_short_form_list, [self.humidity_forecast_list[0],
                                                      self.humidity_forecast_list[1], self.humidity_forecast_list[2]],0,
                                                      self.forecast_button_names[3], self.forecast_ylabels_list[3],
                                                      ".",temp_icons_list=self.humidity_button_icon))
        self.forecast_button_humidity.grid(row=0, column=3, padx=4)
        self.forecast_button_precipitation = tk.Button(self.forecast_buttons_frame,font=("Arial",14),text="Precipitation", bg="purple",
                                                  fg="#ffffff",activebackground="purple",padx=4,
                                                       image=self.precipitation_button_icon,compound=tk.LEFT,
                                                  command=lambda: self.thread_create_forecast_graph(
                                                      self.time_short_form_list, [self.precipitation_forecast_list[0],
                                                      self.precipitation_forecast_list[1], self.precipitation_forecast_list[2]],0,
                                                      self.forecast_button_names[4], self.forecast_ylabels_list[4],
                                                      ".",temp_icons_list=self.precipitation_button_icon))
        self.forecast_button_precipitation.grid(row=0, column=4, padx=4)
        self.forecast_button_cloud_cover = tk.Button(self.forecast_buttons_frame,font=("Arial",14),text="Cloud cover", bg="purple",
                                                       fg="#ffffff",padx=4,activebackground="purple",image=self.cloud_cover_button_icon,compound=tk.LEFT,
                                                       command=lambda: self.thread_create_forecast_graph(
                                                           self.time_short_form_list,
                                                           [self.cloud_cover_forecast_list[0],
                                                           self.cloud_cover_forecast_list[1],
                                                           self.cloud_cover_forecast_list[2]],0,
                                                           self.forecast_button_names[5],
                                                           self.forecast_ylabels_list[5],".",temp_icons_list=self.cloud_cover_button_icon))
        self.forecast_button_cloud_cover.grid(row=0, column=5, padx=4)
        self.forecast_button_rain_chance = tk.Button(self.forecast_buttons_frame,font=("Arial",14),text="Chance of rain", bg="purple",
                                                     fg="#ffffff",padx=4,image=self.rain_chance_button_icon,compound=tk.LEFT,activebackground="purple",
                                                     command=lambda: self.thread_create_forecast_graph(
                                                         self.time_short_form_list,
                                                         [self.rain_chance_forecast_list[0],
                                                         self.rain_chance_forecast_list[1],
                                                         self.rain_chance_forecast_list[2]],0,
                                                         self.forecast_button_names[6],
                                                         self.forecast_ylabels_list[6],".",temp_icons_list=self.rain_chance_button_icon))
        self.forecast_button_rain_chance.grid(row=0, column=6, padx=4)
        self.forecast_button_snow = tk.Button(self.forecast_buttons_frame,font=("Arial",14),text="Snow", bg="purple",activebackground="purple",
                                                     fg="#ffffff",padx=4,image=self.snow_chance_button_icon,compound=tk.LEFT,
                                                     command=lambda: self.thread_create_forecast_graph(
                                                         self.time_short_form_list,
                                                         [self.snow_forecast_list[0],
                                                         self.snow_forecast_list[1],
                                                         self.snow_forecast_list[2]],0,
                                                         self.forecast_button_names[7],
                                                         self.forecast_ylabels_list[7], ".",temp_icons_list=self.snow_chance_button_icon))
        self.forecast_button_snow.grid(row=0, column=7, padx=4)
        self.forecast_button_visibility = tk.Button(self.forecast_buttons_frame,font=("Arial",14),text="Visibility", bg="purple",activebackground="purple",
                                              fg="#ffffff",image=self.visibility_button_icon,compound=tk.LEFT,padx=4,
                                              command=lambda: self.thread_create_forecast_graph(
                                                  self.time_short_form_list,
                                                  [self.visibility_forecast_list[0],
                                                  self.visibility_forecast_list[1],
                                                  self.visibility_forecast_list[2]],0,
                                                  self.forecast_button_names[8],
                                                  self.forecast_ylabels_list[8], ".",temp_icons_list=self.visibility_button_icon))
        self.forecast_button_visibility.grid(row=0, column=8, padx=4)
        self.forecast_button_dew_point = tk.Button(self.forecast_buttons_frame,font=("Arial",14),text="Dew point", bg="purple",activebackground="purple",
                                                    fg="#ffffff",image=self.dew_point_button_icon,compound=tk.LEFT,
                                                    command=lambda: self.thread_create_forecast_graph(
                                                        self.time_short_form_list,
                                                        [self.dew_point_forecast_list[0],
                                                        self.dew_point_forecast_list[1],
                                                        self.dew_point_forecast_list[2]],0,
                                                        self.forecast_button_names[9],
                                                        self.forecast_ylabels_list[9], ".",temp_icons_list=self.dew_point_button_icon))
        self.forecast_button_dew_point.grid(row=0, column=9, padx=4)
        self.forecast_button_uv= tk.Button(self.forecast_buttons_frame, font=("Arial", 14), text="UV",
                                                   bg="purple", activebackground="purple",padx=4,
                                                   fg="#ffffff", image=self.dew_point_button_icon, compound=tk.LEFT,
                                                   command=lambda: self.thread_create_forecast_graph(
                                                       self.time_short_form_list,
                                                       [self.uv_forecast_list[0],
                                                        self.uv_forecast_list[1],
                                                        self.uv_forecast_list[2]], 0,
                                                       self.forecast_button_names[10],
                                                       self.forecast_ylabels_list[10], ".",
                                                       temp_icons_list=self.uv_button_icon))
        self.forecast_button_uv.grid(row=0, column=10, padx=4)
        self.which_day_1_button = tk.Button(self.forecast_buttons_frame_2,text="Day 1",font=("Arial",14),bg="#33d9b2",activebackground="#33d9b2",fg="#ffffff")
        self.which_day_1_button.grid(row=1,column=0,padx=7)
        self.which_day_2_button = tk.Button(self.forecast_buttons_frame_2, text="Day 2",font=("Arial",14),bg="#33d9b2",activebackground="#33d9b2",fg="#ffffff")
        self.which_day_2_button.grid(row=1, column=1, padx=7)
        self.which_day_3_button = tk.Button(self.forecast_buttons_frame_2, text="Day 3",font=("Arial",14),bg="#33d9b2",activebackground="#33d9b2",fg="#ffffff")
        self.which_day_3_button.grid(row=1, column=2, padx=7)
        self.forecast_3_days_graph_frame = tk.Frame(self.forecast_innerframe1)
        self.forecast_3_days_graph_frame.pack(pady=2)
        self.thread_process_weather_forecast(self.forecast_obj)
    def thread_show_forecast_frame(self):
        thread_var = Thread(target=self.show_forecast_frame())
        thread_var.start()

    def convert_date_to_day(self,date_array):
        for ptr in range(len(date_array)):
            format = '%Y-%m-%d'
            # convert from string format to datetime format
            day_converted = datetime.strptime(date_array[ptr], format)
            # get the date from the datetime using date()
            day_converted = day_converted.date().strftime("%A")
            date_array[ptr] = day_converted
        return date_array

    def change_button_clicked_color(self,button_text,day_index):
        for widget in self.forecast_buttons_frame.winfo_children():
            if widget.cget("text")==button_text:
                widget.configure(bg="black")
            else:
                widget.configure(bg="purple")
        arr = [self.which_day_1_button,self.which_day_2_button,self.which_day_3_button]
        for ptr in range(len(arr)):
            if ptr==day_index:
                widget = arr[ptr]
                widget.configure(bg="black")
            else:
                arr[ptr].configure(bg="#33d9b2")
              
    def thread_change_button_clicked_color(self,data_name,day_index):
        thread_var = Thread(target=self.change_button_clicked_color(data_name,day_index))
        thread_var.start()

    # Function to fetch historical weather data for previous 2 days.
    def fetch_previous_two_days_weather_report(self,confirmed_location):
        # Get today date.
        today_date = date.today()
        # Get the past 1st day's date.
        yesterday = today_date-timedelta(days=1)
        # Get the past 2nd day's date.
        day_before_yesterday = today_date-timedelta(days=2)
        self.previous_2days = []
        # Convert the date to day, and append to array 'previous_2days'.
        self.previous_2days.append(yesterday.strftime("%A"))
        self.previous_2days.append(day_before_yesterday.strftime("%A"))
        self.historical_weather_report_obj = []
        yesterday_response = requests.get(f"https://api.weatherapi.com/v1/history.json?key={self.my_weatherapi_key}&q={confirmed_location[0]},{confirmed_location[1]}&dt={yesterday}")
        if yesterday_response.status_code==200:
            yesterday_obj = json.loads(yesterday_response.content)
            self.historical_weather_report_obj.append(yesterday_obj)
            day_before_yesterday_response = requests.get(f"https://api.weatherapi.com/v1/history.json?key={self.my_weatherapi_key}&q={confirmed_location[0]},{confirmed_location[1]}&dt={day_before_yesterday}")
            if day_before_yesterday_response.status_code==200:
                day_before_yesterday_obj = json.loads(day_before_yesterday_response.content)
                self.historical_weather_report_obj.append(day_before_yesterday_obj)
            else:
                messagebox.showerror("Error", "An error occurred. Please try again after some time.")
        else:
            messagebox.showerror("Error","An error occurred. Please try again after some time.")
          
    def show_historical_report_frame(self):
        # Delete all widgets in the frame 'history_main_panel'.
        for widget in self.history_main_panel.winfo_children():
            widget.destroy()
        # Creating frame.
        self.historical_weather_innerframe1 = tk.Frame(self.history_main_panel, background=self.bg_dark_color)
        self.historical_weather_innerframe1.pack()
        tk.Label(self.historical_weather_innerframe1,text="Historical weather",bg=self.bg_dark_color,fg="#ffffff",font=("Times New Roman",18,"bold")).pack()
        self.historical_weather_buttons_frame = tk.Frame(self.historical_weather_innerframe1,background=self.bg_dark_color)
        self.historical_weather_buttons_frame.pack(pady=7)
        self.history_temperature_button = tk.Button(self.historical_weather_buttons_frame,text="Temperature",bg="purple",fg="#ffffff",font=("Arial",14),image=self.temperature_button_icon,compound=tk.LEFT,command=lambda :self.thread_create_historical_report_graph(self.time_short_form_list,self.temperature_historical_report_list,"Temperature","Celsius"))
        self.history_temperature_button.grid(row=0,column=0,padx=5)
        self.history_precipitation_button = tk.Button(self.historical_weather_buttons_frame, text="Precipitation",bg="purple",fg="#ffffff",font=("Arial",14),image=self.precipitation_button_icon,compound=tk.LEFT,command=lambda :self.thread_create_historical_report_graph(self.time_short_form_list,self.precipitation_historical_report_list,"Precipitation","mm"))
        self.history_precipitation_button.grid(row=0, column=1,padx=5)
        self.historical_weather_graph_frame = tk.Frame(self.historical_weather_innerframe1,background=self.bg_dark_color)
        self.historical_weather_graph_frame.pack(pady=10)
        self.thread_process_historical_weather_report(self.historical_weather_report_obj)

    def change_button_clicked_color_historical(self,button_text):
        for widget in self.historical_weather_buttons_frame.winfo_children():
            if widget.cget("text")==button_text:
                widget.configure(bg="black")
            else:
                widget.configure(bg="purple")
              
    def process_historical_weather_report(self,historical_report_data):
        # Get the weather data of yesterday.
        day_previous = historical_report_data[0]["forecast"]["forecastday"][0]["hour"]
        # Get the weather data of day before yesterday.
        day_previous_of_previous = historical_report_data[1]["forecast"]["forecastday"][0]["hour"]
        # Resetting the arrays to assign new data.
        self.temperature_historical_report_list.clear()
        self.temperature_historical_report_list = [[],[]]
        self.precipitation_historical_report_list.clear()
        self.precipitation_historical_report_list = [[],[]]
        for every_hour in day_previous:
            if self.temp_unit=="C":
                self.temperature_historical_report_list[0].append(every_hour.get("temp_c"))
            elif self.temp_unit=="F":
                self.temperature_historical_report_list[0].append(every_hour.get("temp_f"))
            self.precipitation_historical_report_list[0].append(every_hour.get("precip_mm"))
        self.root.update()
        for every_hour in day_previous_of_previous:
            if self.temp_unit=="C":
                self.temperature_historical_report_list[1].append(every_hour.get("temp_c"))
            elif self.temp_unit=="F":
                self.temperature_historical_report_list[1].append(every_hour.get("temp_f"))
            self.precipitation_historical_report_list[1].append(every_hour.get("precip_mm"))
        self.root.update()
        self.thread_create_historical_report_graph(self.time_short_form_list,self.temperature_historical_report_list,"Temperature",self.temp_unit)

    def thread_process_historical_weather_report(self, historical_report_data):
        thread_processing_historical_weather = Thread(target=self.process_historical_weather_report(historical_report_data))
        thread_processing_historical_weather.start()

    def create_historical_report_graph(self,time_arr,data_day_12,data_name,y_label):
        for widget in self.historical_weather_graph_frame.winfo_children():
            widget.destroy()
        sns.set_context("paper", font_scale=1.5)
        fig, ax = plt.subplots(figsize=(19, 7), dpi=100, facecolor=self.pale_blue_color)
        ax.set_facecolor("#c3fbf9")
        sns.lineplot(x=time_arr, y=data_day_12[0], color="green", label=self.previous_2days[0],
                     linestyle="dashed", marker=".", markersize=16).set(xlabel="Time", ylabel=y_label)
        sns.lineplot(x=time_arr, y=data_day_12[1], color="red", label=self.previous_2days[1],
                     linestyle="dashed", marker=".", markersize=16).set(xlabel="Time", ylabel=y_label)
        plt.legend(title=data_name)
        self.change_button_clicked_color_historical(data_name)
        canvas = FigureCanvasTkAgg(fig, master=self.historical_weather_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        plt.close()  # Closes the most recently created figure
        plt.close('all')
      
    def thread_create_historical_report_graph(self,time_arr,data_day_12,data_name,y_label):
        thread_var = Thread(target=self.create_historical_report_graph(time_arr,data_day_12,data_name,y_label))
        thread_var.start()

    # Function to generate a random fact about the city searched using Gemini AI.
    # Fetched using Gemini AI API from the model 'Gemini 1.5 flash'.
    def generate_fun_fact(self,city_name):
        # Gemini AI API key.
        os.environ["API_KEY"] = "YOUR_GEMINI_AI_API_KEY"    # Replace with your API key by registering at Gemini API.
        genai.configure(api_key=os.environ["API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Prompting the Gemini AI.
        response = model.generate_content(f"Tell a good fact about city {city_name} in 1 line.")
        # Get the response returned by the AI.
        generated_fact = response.text
        # Split the string 'generated_fact' to fit within a label of width 50.
        generated_fact = "\n".join(textwrap.wrap(generated_fact,width=50))
        # Set the splitted response from AI to the Label 'fun_fact_label'.
        self.fun_fact_label.config(text=generated_fact)
      
    def thread_generate_fun_fact(self,city_name):
        thread_var = Thread(target=self.generate_fun_fact(city_name))
        thread_var.start()
      
    def get_next_3_days_overall_temperature_details(self):
        three_days_array = self.forecast_obj["forecast"]["forecastday"]
        num = 0
        for widget in self.forecast_sub_frame2.winfo_children():
            widget.destroy()
        tk.Label(self.forecast_sub_frame2, text="3 days forecast", font=("Arial", 19), bg=self.bg_dark_color,
                 fg="#ffffff").grid(row=0,
                                    column=0,
                                    columnspan=5, pady=3)
        for every_day in three_days_array:
            min_temp = 0
            max_temp = 0
            if self.temp_unit=="F":
                min_temp = str(every_day["day"]["mintemp_f"])
                max_temp = str(every_day["day"]["maxtemp_f"])
            elif self.temp_unit=="C":
                min_temp = str(every_day["day"]["mintemp_c"])
                max_temp = str(every_day["day"]["maxtemp_c"])
            date_number = str(int(every_day["date"][8:10]))
            month_number = int(every_day["date"][5:7])
            future_date = str(date_number)+" "+self.months_list[month_number - 1]
            weather_condition_description = every_day["day"]["condition"]["text"]
            weather_condition_icon = every_day["day"]["condition"]["code"]
            next_day_forecast_label = tk.Label(self.forecast_sub_frame2, text=future_date+ "   ", font=("Times New Roman", 19),
                                                   bg=self.bg_dark_color, fg="#ffffff")
            next_day_forecast_label.grid(row=num + 1, column=0,pady=5)
            tk.Label(self.forecast_sub_frame2, text=str(weather_condition_description), font=("Times New Roman", 20),
                         bg=self.bg_dark_color, fg="#ffffff").grid(row=num + 1, column=1)
            tk.Label(self.forecast_sub_frame2, text=f"Low:{min_temp}°{self.temp_unit}",
                         font=("Times New Roman", 20), image=self.down_arrow_pic, compound=tk.LEFT,
                         bg=self.bg_dark_color, fg="#ffffff").grid(row=num + 1, column=2)
            tk.Label(self.forecast_sub_frame2, text=f"High:{max_temp}°{self.temp_unit} ",
                         font=("Times New Roman", 20), image=self.up_arrow_pic, compound=tk.LEFT, bg=self.bg_dark_color,
                         fg="#ffffff").grid(row=num + 1, column=3)
            num += 1
            self.root.update()

    def thread_get_next_3_days_overall_temperature_details(self):
        thread_var = Thread(target=self.get_next_3_days_overall_temperature_details())
        thread_var.start()

    # Function to convert the given angle to x and y coordinate points.
    def find_xy_coordinate(self,angle):
        angle = angle - 90
        # Convert given angle to radians.
        radians_input = angle * (math.pi / 180)
        # Radius is set to 200.
        radius = 200
        # Convert radians to coordinate points.
        x = radius * math.cos(radians_input)
        y = radius * math.sin(radians_input)
        return [x, y]
      
    def show_wind_direction_frame(self):
        # Delete all widgets in the frame 'wind_direction_speed_main_panel'.
        for widget in self.wind_direction_speed_main_panel.winfo_children():
            widget.destroy()
        tk.Label(self.wind_direction_speed_main_panel,text="3 days Wind direction & Wind speed",bg=self.bg_dark_color,fg="#ffffff",font=("Times New Roman",21,"bold")).pack()
        # Creating frame.
        self.wind_direction_innerframe_1 = tk.Frame(self.wind_direction_speed_main_panel,background=self.bg_dark_color)
        self.wind_direction_innerframe_1.pack(pady=20)
        # Creating 3 sub frames for 3 days.
        self.wind_direction_subframe_1 = tk.Frame(self.wind_direction_innerframe_1,background=self.bg_dark_color)
        self.wind_direction_subframe_1.grid(row=0,column=0,padx=10,pady=15)
        self.wind_direction_subframe_2 = tk.Frame(self.wind_direction_innerframe_1,background=self.bg_dark_color)
        self.wind_direction_subframe_2.grid(row=0, column=1,padx=10,pady=15)
        self.wind_direction_subframe_3 = tk.Frame(self.wind_direction_innerframe_1,background=self.bg_dark_color)
        self.wind_direction_subframe_3.grid(row=0, column=2,padx=10,pady=15)
        # Color code details
        self.wind_degree_details = tk.Frame(self.wind_direction_innerframe_1, background=self.bg_dark_color)
        self.wind_degree_details.grid(row=1, column=1, rowspan=12)
        self.mini_canvas1 = tk.Canvas(self.wind_degree_details, width=300, height=260, background=self.bg_dark_color,
                                      highlightthickness=0)
        self.mini_canvas1.grid(row=0, column=0, rowspan=12)
        self.mini_canvas1.create_rectangle(0, 0, 40, 20, fill="#FF00FF")
        self.mini_canvas1.create_text(90, 10, text=">157 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(0, 30, 40, 50, fill="turquoise")
        self.mini_canvas1.create_text(90, 40, text="130 to 156 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(0, 60, 40, 80, fill="white")
        self.mini_canvas1.create_text(90, 70, text="111 to 129 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(0, 90, 40, 110, fill="yellow")
        self.mini_canvas1.create_text(90, 100, text="96 to 110 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(0, 120, 40, 140, fill="#98fb98")
        self.mini_canvas1.create_text(90, 130, text="73 to 95 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(0, 150, 40, 170, fill="#005F6A")
        self.mini_canvas1.create_text(90, 160, text="64 to 72 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(0, 180, 40, 200, fill="violet")
        self.mini_canvas1.create_text(90, 190, text="55 to 63 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(0, 210, 40, 230, fill="purple")
        self.mini_canvas1.create_text(90, 220, text="47 to 54 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(0, 235, 40, 255, fill="red")
        self.mini_canvas1.create_text(90, 245, text="39 to 46 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(160, 0, 200, 20, fill="#CB4154")
        self.mini_canvas1.create_text(250, 10, text="32 to 38 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(160, 30, 200, 50, fill="orange")
        self.mini_canvas1.create_text(250, 40, text="25 to 31 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(160, 60, 200, 80, fill="green")
        self.mini_canvas1.create_text(250, 70, text="19 to 24 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(160, 90, 200, 110, fill="blue")
        self.mini_canvas1.create_text(250, 100, text="13 to 18 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(160, 120, 200, 140, fill="#00FF00")
        self.mini_canvas1.create_text(250, 130, text="8 to 12 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(160, 150, 200, 170, fill="#420c09")
        self.mini_canvas1.create_text(250, 160, text="4 to 7 mph", fill="white", font=("Arial", 10))
        self.mini_canvas1.create_rectangle(160, 180, 200, 200, fill="grey")
        self.mini_canvas1.create_text(250, 190, text="0 to 3 mph", fill="white", font=("Arial", 10))
        self.root.update()
        self.thread_process_wind_degree_speed()

    def thread_show_wind_direction_frame(self):
        thread_var = Thread(target=self.show_wind_direction_frame())
        thread_var.start()
      
    def process_wind_degree_speed(self):
        tk.Label(self.wind_direction_subframe_1,text=self.future_forecast_days[0],fg="#ffffff",bg=self.bg_dark_color,font=("Arial",17)).pack()
        self.wind_direction_canvas1 = tk.Canvas(self.wind_direction_subframe_1, width=550, height=500,
                                                scrollregion="-260 -250 200 200", background="black")
        self.wind_direction_canvas1.create_text(0,-230,text="N",fill="#ffffff",font=("Arial",16))
        self.wind_direction_canvas1.create_text(-230, 0, text="W", fill="#ffffff", font=("Arial", 16))
        self.wind_direction_canvas1.create_text(230,0,text="E",fill="#ffffff",font=("Arial",16))
        self.wind_direction_canvas1.create_text(0, 230, text="S", fill="#ffffff", font=("Arial", 16))
        self.wind_direction_canvas1.pack()
        tk.Label(self.wind_direction_subframe_2, text=self.future_forecast_days[1], fg="#ffffff",bg=self.bg_dark_color,font=("Arial",17)).pack()
        self.wind_direction_canvas2 = tk.Canvas(self.wind_direction_subframe_2, width=550, height=500,
                                                scrollregion="-260 -250 200 200", background="black")
        self.wind_direction_canvas2.create_text(0, -230, text="N", fill="#ffffff", font=("Arial", 16))
        self.wind_direction_canvas2.create_text(-230, 0, text="W", fill="#ffffff", font=("Arial", 16))
        self.wind_direction_canvas2.create_text(230, 0, text="E", fill="#ffffff", font=("Arial", 16))
        self.wind_direction_canvas2.create_text(0, 230, text="S", fill="#ffffff", font=("Arial", 16))
        self.wind_direction_canvas2.pack()
        tk.Label(self.wind_direction_subframe_3, text=self.future_forecast_days[2], fg="#ffffff",bg=self.bg_dark_color,font=("Arial",17)).pack()
        self.wind_direction_canvas3 = tk.Canvas(self.wind_direction_subframe_3, width=550, height=500,
                                                scrollregion="-260 -250 200 200", background="black")
        self.wind_direction_canvas3.create_text(0, -230, text="N", fill="#ffffff", font=("Arial", 16))
        self.wind_direction_canvas3.create_text(-230, 0, text="W", fill="#ffffff", font=("Arial", 16))
        self.wind_direction_canvas3.create_text(230, 0, text="E", fill="#ffffff", font=("Arial", 16))
        self.wind_direction_canvas3.create_text(0, 230, text="S", fill="#ffffff", font=("Arial", 16))
        self.wind_direction_canvas3.pack()
        self.root.update()
        self.canvas_list = [self.wind_direction_canvas1,self.wind_direction_canvas2,self.wind_direction_canvas3]
        #wind_degrees_list.sort(reverse=True)
        for current_wind_degree_array_ptr in range(3):
            self.root.update()
            current_wind_degree_array = self.wind_degree_forecast_list[current_wind_degree_array_ptr]
            wind_speed_mph = self.wind_forecast_list[current_wind_degree_array_ptr]
            for ptr in range(len(current_wind_degree_array)):
                coords_arr = self.find_xy_coordinate(current_wind_degree_array[ptr])
                colorname = "grey"
                if wind_speed_mph[ptr] >= 157:
                    colorname = "#FF00FF"
                elif wind_speed_mph[ptr] >= 130 and wind_speed_mph[ptr] <= 156:
                    colorname = "turquoise"
                elif wind_speed_mph[ptr] >= 111 and wind_speed_mph[ptr] <= 129:
                    colorname = "white"
                elif wind_speed_mph[ptr] >= 96 and wind_speed_mph[ptr] <= 110:
                    colorname = "yellow"
                elif wind_speed_mph[ptr] >= 73 and wind_speed_mph[ptr] <= 95:
                    colorname = "#98fb98"
                elif wind_speed_mph[ptr] >= 64 and wind_speed_mph[ptr] <= 72:
                    colorname = "#005F6A"
                elif wind_speed_mph[ptr] >= 55 and wind_speed_mph[ptr] <= 63:
                    colorname = "violet"
                elif wind_speed_mph[ptr] >= 47 and wind_speed_mph[ptr] <= 54:
                    colorname = "purple"
                elif wind_speed_mph[ptr] >= 39 and wind_speed_mph[ptr] <= 46:
                    colorname = "red"
                elif wind_speed_mph[ptr] >= 32 and wind_speed_mph[ptr] <= 38:
                    colorname = "#CB4154"
                elif wind_speed_mph[ptr] >= 25 and wind_speed_mph[ptr] <= 31:
                    colorname = "orange"
                elif wind_speed_mph[ptr] >= 19 and wind_speed_mph[ptr] <= 24:
                    colorname = "green"
                elif wind_speed_mph[ptr] >= 13 and wind_speed_mph[ptr] <= 18:
                    colorname = "blue"
                elif wind_speed_mph[ptr] >= 8 and wind_speed_mph[ptr] <= 12:
                    colorname = "#00FF00"
                elif wind_speed_mph[ptr] >= 4 and wind_speed_mph[ptr] <= 7:
                    colorname = "#420C09"
                elif wind_speed_mph[ptr] >= 0 and wind_speed_mph[ptr] <= 3:
                    colorname = "grey"
                self.canvas_list[current_wind_degree_array_ptr].create_line(0, 0, coords_arr[0], coords_arr[1], fill=colorname, width=3)

    def thread_process_wind_degree_speed(self):
        thread_var = Thread(target=self.process_wind_degree_speed())
        thread_var.start()

    def about(self):
        new_popup_window = tk.Toplevel()
        new_popup_window.title("About Weather Cast")
        new_popup_window.geometry("600x340")
        new_popup_window.transient(self.root)  # To avoid it from preventing the root window to be paused.
        new_popup_window.wm_attributes('-topmost', True)
        app_icon_label = tk.Label(new_popup_window, image=self.app_icon_image_small)
        app_icon_label.pack()
        tk.Label(new_popup_window, text="Weather Cast", font=("Arial", 19)).pack(pady=3)
        content = "Version: 1.1.0\nRelease Date: 11th August 2024\nDeveloper: Reshma Haridhas\nOS: Windows 10 or later\nCopyright: © 2024 Reshma Haridhas. All Rights Reserved"
        content_label = tk.Label(new_popup_window, text=content, font=("Arial", 12), fg="#000000")
        content_label.pack()
