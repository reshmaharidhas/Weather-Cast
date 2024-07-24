import tkinter as tk
from tkinter import ttk
import requests
import json
from threading import Thread
from tkinter import messagebox
from PIL import Image,ImageTk
import datetime
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)


class WeatherCast:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather Cast")
        self.root.geometry("1500x710")
        self.root.minsize(width=1500,height=700)
        # Initializing the app with a city name if the app is not able to fetch user's public IP address.
        self.user_IP_Address = "Delhi"
        self.ip_address_city = "Delhi"
        self.last_selected_city_lat_lon = []
        # UI colors
        self.sky_color_light = "#9fe9fc"
        self.bg_dark_color = "#0463CA"
        self.root.config(bg=self.bg_dark_color)
        # API keys
        self.my_api_key = "YOUR_OPENWEATHERMAP_API_KEY"     # Replace with your API key by registering at OpenWeatherMap API.
        self.my_weatherapi_key = "YOUR_WEATHERAPI_API_KEY"      # Replace with your API key by registering at WeatherAPI.
        # predefined variables
        self.temp_unit = "F"
        self.temperature_unit_string = "imperial"
        self.air_quality_values = ["Good","Fair","Unhealthy","Hazardous","Very Hazardous"]
        self.air_quality_colors = ["#00ff00","yellow","orange","red","purple"]
        self.months_list = ["Jan","Feb","March","April","May","June","July","Aug","Sept","Oct","Nov","Dec"]
        self.uv_index_tips_list = ["Enjoy being outside","Seek shade during midday. Wear hat & sunscreen",
                                   "Avoid being outside during midday.\n Shirt, sunscreen, sunglass & hat are must."]
        # sky pictures
        self.night_sky_pic1 = tk.PhotoImage(file="assets/images/nightsky.png")
        self.day_sky_pic1 = tk.PhotoImage(file="assets/images/day_sky_background.png")
        self.cloudy_day_pic1 = tk.PhotoImage(file="assets/images/cloudy_sky_pic1.png")
        self.rainy_night_pic1 = tk.PhotoImage(file="assets/images/night_sky_raining.png")
        self.rainy_day_pic1 = tk.PhotoImage(file="assets/images/day_sky_raining.png")
        # symbol images
        self.thermometer_pic = tk.PhotoImage(file="assets/images/thermometer.png")
        self.down_arrow_pic = tk.PhotoImage(file="assets/images/down-arrow-50.png").subsample(2,2)
        self.up_arrow_pic = tk.PhotoImage(file="assets/images/up-arrow-50.png").subsample(2,2)
        self.refresh_icon = tk.PhotoImage(file="assets/images/icons8-refresh-50.png").subsample(2,2)
        self.location_icon = tk.PhotoImage(file="assets/images/location-48.png").subsample(2,2)
        self.app_icon_image = tk.PhotoImage(file="assets/images/weather_cast_icon.png")
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
        self.moon_phases_dict = {"New Moon":self.moon_phase_new_moon,"Full Moon":self.moon_phase_full_moon,
                                 "Waxing Crescent":self.moon_phase_waxing_crescent,
                                 "First Quarter":self.moon_phase_first_quarter,"Waxing Gibbous":self.moon_phase_waxing_gibbous,
                                 "Waning Gibbous":self.moon_phase_waning_gibbous,"Last Quarter":self.moon_phase_last_quarter,
                                 "Waning Crescent":self.moon_phase_waning_crescent}
        self.air_quality_face_images = [self.face1,self.face2,self.face3,self.face4,self.face5]
        # frame1
        self.frame1 = tk.Frame(self.root,background=self.bg_dark_color)
        self.frame1.pack(pady=7)
        self.user_input = tk.StringVar()
        self.locate_current_location_btn = tk.Button(self.frame1,image=self.location_icon,bg=self.bg_dark_color,command=lambda :self.thread_initialize_location(self.ip_address_city),bd=0,activebackground=self.bg_dark_color)
        self.locate_current_location_btn.grid(row=0,column=0)
        self.entry_field = tk.Entry(self.frame1,width=100,textvariable=self.user_input)
        self.entry_field.grid(row=0,column=1,padx=2)
        self.recommendations = ttk.Combobox(self.frame1,state="readonly")
        self.recommendations.bind("<<ComboboxSelected>>", self.get_user_selected_from_combobox)
        self.recommendations.grid(row=0,column=2,padx=3)
        self.search_button = tk.Button(self.frame1,text="Show Live Weather",command=self.thread_get_location_input,bg="#000000",fg="white",activebackground="#000000",activeforeground="#ffffff",relief=tk.RAISED)
        self.search_button.grid(row=0,column=3,padx=7)
        self.root.bind("<Return>",self.shortcut_enter_button_pressed)
        self.refresh_info_buttton = tk.Button(self.frame1,text="Refresh",command=self.thread_refresh_weather_data,image=self.refresh_icon,bg=self.bg_dark_color,activebackground=self.bg_dark_color)
        self.refresh_info_buttton.grid(row=0,column=4)
        self.temperature_unit_changing_button = tk.Button(self.frame1,text=self.temp_unit,command=self.thread_change_temperature_unit,fg="#ffffff",bg="#3682d5",activebackground="#3682d5",font=("Arial",12,"bold"),activeforeground="#000000")
        self.temperature_unit_changing_button.grid(row=0,column=5,padx=10)
        # frame2
        self.frame2 = tk.Frame(self.root,background=self.bg_dark_color)
        self.frame2.pack()
        self.side_panel = tk.Frame(self.frame2)
        self.side_panel.grid(row=0,column=0)
        self.innerframe1 = tk.Frame(self.frame2,background=self.bg_dark_color)
        self.innerframe1.grid(row=0,column=1)
        self.innerframe2 = tk.Frame(self.frame2)
        self.innerframe2.grid(row=0,column=2,rowspan=2)
        self.sub_frame1 = tk.Frame(self.innerframe1)
        self.sub_frame1.grid(row=0,column=0)
        self.canvas1 = tk.Canvas(self.sub_frame1, width=640, height=200, highlightthickness=0)
        self.canvas1.grid(row=0,column=0)
        self.scenery_canvas = self.canvas1.create_image(0, 0, image=self.night_sky_pic1, anchor=tk.NW)
        self.location_name = self.canvas1.create_text(5,10,fill="white",anchor=tk.NW,font=("Times New Roman",20))
        self.location_city_country = self.canvas1.create_text(5,38,anchor=tk.NW,fill="white",font=("Times New Roman",13))
        self.current_time = self.canvas1.create_text(5,55,anchor=tk.NW,fill="white",font=("Times New Roman",13))
        self.current_temp = self.canvas1.create_text(115,70,fill="#ffffff",anchor=tk.NW,font=("Times New Roman",42))
        self.current_feels_like_temp = self.canvas1.create_text(115,122,fill="#ffffff",anchor=tk.NW,font=("Times New Roman",13))
        self.weather_status = self.canvas1.create_text(115,140,fill="#ffffff",anchor=tk.NW, font=("Arial", 20))
        self.weather_description = self.canvas1.create_text(115,170,fill="#ffffff",anchor=tk.NW,font=("Times New Roman", 13))
        self.weather_current_picture = self.canvas1.create_image(10,70,anchor=tk.NW)
        self.canvas1.create_image(350,30,image=self.wind_picture,anchor=tk.NW)
        self.wind_speed = self.canvas1.create_text(390,30,fill="#ffffff",anchor=tk.NW,font=("Times New Roman",12))
        self.canvas1.create_image(350,60,image=self.pressure_icon,anchor=tk.NW)
        self.pressure = self.canvas1.create_text(390,60,fill="#ffffff",anchor=tk.NW,font=("Times New Roman",12))
        self.canvas1.create_image(350,90,image=self.humidity_icon,anchor=tk.NW)
        self.humidity_text = self.canvas1.create_text(390,90,fill="#ffffff",anchor=tk.NW,font=("Times New Roman",12))
        self.canvas1.create_image(350,120,image=self.visibility_icon,anchor=tk.NW)
        self.visibility_text = self.canvas1.create_text(390,120,fill="#ffffff",anchor=tk.NW,font=("Times New Roman",12))
        self.canvas1.create_image(350,150,image=self.dewpoint_icon,anchor=tk.NW)
        self.dew_point_text = self.canvas1.create_text(390,150,fill="#ffffff",anchor=tk.NW,font=("Times New Roman",12))
        self.sub_frame2 = tk.Frame(self.innerframe1,background=self.bg_dark_color)
        self.sub_frame2.grid(row=1, column=0)
        tk.Label(self.sub_frame2,image=self.sun_timeline_pic3,bg=self.bg_dark_color).grid(row=0,column=2,padx=10,pady=7)
        tk.Label(self.sub_frame2, image=self.sun_timeline_pic2,bg=self.bg_dark_color).grid(row=1, column=1,padx=10)
        tk.Label(self.sub_frame2, image=self.sun_timeline_pic3,bg=self.bg_dark_color).grid(row=1, column=3,padx=10)
        self.sunrise_label = tk.Label(self.sub_frame2,font=("Times New Roman",12),bg=self.bg_dark_color,fg="#ffffff",image=self.sunrise_icon,compound=tk.TOP,text="Sunrise")
        self.sunrise_label.grid(row=2,column=0)
        self.sunset_label = tk.Label(self.sub_frame2,font=("Times New Roman",12),bg=self.bg_dark_color,fg="#ffffff",image=self.sunset_icon,compound=tk.TOP,text="Sunset")
        self.sunset_label.grid(row=2,column=4)
        self.sunrise_time_label = tk.Label(self.sub_frame2,bg=self.bg_dark_color,fg="#ffffff")
        self.sunrise_time_label.grid(row=3,column=0)
        self.sunset_time_label = tk.Label(self.sub_frame2,bg=self.bg_dark_color,fg="#ffffff")
        self.sunset_time_label.grid(row=3,column=4)
        tk.Label(self.sub_frame2,image=self.moon_crescent_icon,bg=self.bg_dark_color).grid(row=1,column=6)
        tk.Label(self.sub_frame2,image=self.moon_crescent_icon,bg=self.bg_dark_color).grid(row=0,column=7)
        tk.Label(self.sub_frame2,image=self.moon_crescent_icon,bg=self.bg_dark_color).grid(row=1,column=8)
        self.moonrise_label = tk.Label(self.sub_frame2,text="Moon rise",image=self.moon_rise_icon,compound=tk.TOP,bg=self.bg_dark_color,fg="#ffffff",font=("Times New Roman",12))
        self.moonrise_label.grid(row=2,column=5)
        self.moonset_label = tk.Label(self.sub_frame2,text="Moon set",image=self.moon_set_icon,compound=tk.TOP,bg=self.bg_dark_color,fg="#ffffff",font=("Times New Roman",12))
        self.moonset_label.grid(row=2,column=9)
        self.moonrise_time_label = tk.Label(self.sub_frame2, bg=self.bg_dark_color,fg="#ffffff")
        self.moonrise_time_label.grid(row=3, column=5)
        self.moonset_time_label = tk.Label(self.sub_frame2, bg=self.bg_dark_color,fg="#ffffff")
        self.moonset_time_label.grid(row=3, column=9)
        self.sub_frame3 = tk.Frame(self.innerframe1,background="#3682d5")
        self.sub_frame3.grid(row=2, column=0)
        tk.Label(self.sub_frame3,text="Air Quality Index",font=("Times New Roman",15,"bold"),bg="#3682d5",fg="#000000").grid(row=0,column=0,columnspan=2)
        self.air_quality_label = tk.Label(self.sub_frame3,font=("Times New Roman",15),padx=10,bg="#3682d5",fg="#000000")
        self.air_quality_label.grid(row=1,column=0)
        self.airquality_canvas = tk.Canvas(self.sub_frame3,width=50,height=50,bg="#3682d5",highlightbackground="#3682d5",bd=0)
        self.airquality_canvas.grid(row=1,column=1)
        self.circle_image = self.airquality_canvas.create_oval(10,10,40,40,fill="#3682d5",outline="")
        tk.Label(self.sub_frame3,text="UV Index",font=("Times New Roman",15,"bold"),bg="#3682d5",fg="#000000").grid(row=0,column=2,padx=15)
        self.uv_index_label = tk.Label(self.sub_frame3,font=("Times New Roman",15),bg="#3682d5")
        self.uv_index_label.grid(row=1,column=2)
        self.sub_frame4 = tk.Frame(self.innerframe1, background=self.bg_dark_color,width=self.innerframe1.winfo_width())
        self.sub_frame4.grid(row=3, column=0)
        tk.Label(self.sub_frame4,text="Moon phase",font=("Arial",16),bg=self.bg_dark_color,fg="#ffffff").grid(row=0,column=0,pady=5)
        self.moon_phase_label = tk.Label(self.sub_frame4,font=("Times New Roman",14),bg=self.bg_dark_color,fg="#ffffff",height=100,padx=15)
        self.moon_phase_label.grid(row=1,column=0,pady=5)
        tk.Label(self.sub_frame4,text="Hourly UV index",font=("Arial",16),bg=self.bg_dark_color,fg="#ffffff").grid(row=0,column=1)
        self.uv_hourly_frame = tk.Frame(self.sub_frame4)
        self.uv_hourly_frame.grid(row=1,column=1)
        self.forecast_frame = tk.Frame(self.innerframe2,background=self.bg_dark_color)
        self.forecast_frame.grid(row=0, column=0)
        self.forecast_sub_frame1 = tk.Frame(self.forecast_frame,background=self.bg_dark_color)
        self.forecast_sub_frame1.pack()
        tk.Label(self.forecast_sub_frame1, text="Hourly forecast", font=("Arial", 16),bg=self.bg_dark_color,fg="#ffffff").grid(row=0, column=0,columnspan=10)
        self.hourly_forecast_labels_array = []
        self.hourly_forecast_temp_labels_array = []
        for num in range(10):
            hour_label = tk.Label(self.forecast_sub_frame1,font=("Times New Roman",16),image=self.thermometer_pic,compound=tk.BOTTOM,bg=self.bg_dark_color,fg="#ffffff")
            hour_label.grid(row=1,column=num)
            self.hourly_forecast_labels_array.append(hour_label)
            temp_label = tk.Label(self.forecast_sub_frame1,font=("Times New Roman",14),text=" ",bg=self.bg_dark_color,fg="#ffffff")
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
        # Setting icon for app in title bar.
        self.root.iconphoto(True,self.app_icon_image)
        # Starts the application by finding the current weather of user's location based on user's public IP address.
        self.thread_detect_user_current_location_by_ip_address()
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
                # Setting background image for dashboard based on day or night, sunny/cloudy or rainy weather conditions.
                if weather_pic[2]=="d":
                    self.canvas1.itemconfig(self.scenery_canvas,image=self.day_sky_pic1)
                    if int(obj['weather'][0]['id'])>800:
                        self.canvas1.itemconfig(self.scenery_canvas,image=self.cloudy_day_pic1)
                    elif int(obj['weather'][0]['id'])>=500 and int(obj['weather'][0]['id'])<=531:
                        self.canvas1.itemconfig(self.scenery_canvas, image=self.rainy_day_pic1)
                else:
                    self.canvas1.itemconfig(self.scenery_canvas,image=self.night_sky_pic1)
                    if int(obj['weather'][0]['id'])>=500 and int(obj['weather'][0]['id'])<=531:
                        self.canvas1.itemconfig(self.scenery_canvas,image=self.rainy_night_pic1)
                self.canvas1.itemconfig(self.location_name,text=obj['name'])
                self.canvas1.itemconfig(self.current_temp,text=str(obj['main']['temp'])+"°"+self.temp_unit)
                self.canvas1.itemconfig(self.current_feels_like_temp,text="Feels like "+str(obj['main']['feels_like']))
                self.canvas1.itemconfig(self.weather_status,text=obj['weather'][0]['main'])
                self.canvas1.itemconfig(self.weather_description,text=obj['weather'][0]['description'])
                imageobject = Image.open(self.weather_pictures_dict.get(weather_pic))
                imageobject = imageobject.resize((100,100))
                weather_current_picture_fetched = ImageTk.PhotoImage(imageobject)
                self.canvas1.itemconfig(self.weather_current_picture,image=weather_current_picture_fetched)
                label2 = tk.Label(self.innerframe2,image=weather_current_picture_fetched)
                label2.image=weather_current_picture_fetched
                self.root.update()
                self.canvas1.itemconfig(self.wind_speed,text="Wind speed: "+str(obj['wind']['speed'])+" mi/h")
                self.canvas1.itemconfig(self.pressure, text="Pressure: "+str(obj['main']['pressure'])+" hPa")
                self.canvas1.itemconfig(self.humidity_text,text="Humidity: "+str(obj['main']['humidity'])+"%")
                self.canvas1.itemconfig(self.visibility_text,text="Visibility: "+str(obj['visibility']//1000)+" km")
                self.sunrise_time_label.config(text=str(datetime.datetime.fromtimestamp(int(obj['sys']['sunrise'])))[11:16])
                self.sunset_time_label.config(text=str(datetime.datetime.fromtimestamp(int(obj['sys']['sunset'])))[11:16])
                airquality_response = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={confirmed_location[0]}&lon={confirmed_location[1]}&appid={self.my_api_key}")
                if airquality_response.status_code==200:
                    air_quality_obj = json.loads(airquality_response.content)
                    current_air_quality_index = air_quality_obj['list'][0]['main']['aqi']
                    self.air_quality_label.config(text=self.air_quality_values[current_air_quality_index-1],image=self.air_quality_face_images[current_air_quality_index-1],compound=tk.LEFT)
                    self.airquality_canvas.itemconfig(self.circle_image,fill=self.air_quality_colors[current_air_quality_index-1])
                else:
                    self.air_quality_label.config(text="Unable to fetch data. Try again later!")
                # Hourly forecast
                self.root.update()
                hourly_forecast_response = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?lat={confirmed_location[0]}&lon={confirmed_location[1]}&units={self.temperature_unit_string}&limit=10,&appid={self.my_api_key}")
                hourly_forecast_obj = json.loads(hourly_forecast_response.content)
                next_ten_3hour_temperature_array = []
                next_ten_3hour_times_array = []
                for num in range(10):
                    every = hourly_forecast_obj['list'][num]
                    hourly_weather_icon = every['weather'][0]['icon']
                    self.hourly_forecast_labels_array[num].config(text=str(every['dt_txt'][10:16]),compound=tk.BOTTOM,image=self.weather_pictures_dict_photoimage.get(hourly_weather_icon))
                    self.hourly_forecast_temp_labels_array[num].config(text=str(every['main']['temp'])+"°"+self.temp_unit,padx=5)
                    next_ten_3hour_temperature_array.append(every['main']['temp'])
                    next_ten_3hour_times_array.append(str(every['dt_txt'][11:16]))
                self.thread_plot_hourly_temperature_bar_chart(next_ten_3hour_temperature_array,next_ten_3hour_times_array)
                five_day_forecast = []
                five_day_dates = []
                five_day_forecast_icons_list = []
                for num in range(len(hourly_forecast_obj['list'])):
                    if hourly_forecast_obj['list'][num]['dt_txt'][11:16]=="00:00":
                        temperatures_list = [hourly_forecast_obj['list'][num]['main']['temp'],hourly_forecast_obj['list'][num]['main']['temp_min'],
                                             hourly_forecast_obj['list'][num]['main']['temp_max'],hourly_forecast_obj['list'][num]['weather'][0]['main']+", "+hourly_forecast_obj['list'][num]['weather'][0]['description']]
                        five_day_forecast.append(temperatures_list)
                        five_day_forecast_icons_list.append(hourly_forecast_obj['list'][num]['weather'][0]['icon'])
                        five_day_dates.append(hourly_forecast_obj['list'][num]['dt_txt'][5:10])
                self.root.update()
                for num in range(len(five_day_dates)):
                    extracted_date_month = five_day_dates[num]
                    extracted_date = extracted_date_month[3:]
                    extracted_month = extracted_date_month[0:2]
                    five_day_dates[num] = extracted_date+" "+self.months_list[int(extracted_month)-1]
                for widget in self.forecast_sub_frame2.winfo_children():
                    widget.destroy()
                tk.Label(self.forecast_sub_frame2, text="Next 5 days forecast", font=("Arial", 16),bg=self.bg_dark_color,fg="#ffffff").grid(row=0,
                                                                                                              column=0,
                                                                                                              columnspan=5)
                for num in range(5):
                    next_day_forecast_label = tk.Label(self.forecast_sub_frame2,text=five_day_dates[num]+": "+str(five_day_forecast[num][0])+"°"+self.temp_unit,font=("Times New Roman",14),bg=self.bg_dark_color,fg="#ffffff")
                    next_day_forecast_label.grid(row=num+1,column=0)
                    imageobject = Image.open(self.weather_pictures_dict.get(five_day_forecast_icons_list[num]))
                    imageobject = imageobject.resize((30, 30))
                    weather_current_picture_fetched = ImageTk.PhotoImage(imageobject)
                    next_day_forecast_label.config(image=weather_current_picture_fetched,compound=tk.RIGHT)
                    next_day_forecast_label.image = weather_current_picture_fetched
                    tk.Label(self.forecast_sub_frame2,text=five_day_forecast[num][3],font=("Times New Roman",14),bg=self.bg_dark_color,fg="#ffffff").grid(row=num+1,column=1)
                    tk.Label(self.forecast_sub_frame2,text=f"Low:{five_day_forecast[num][1]}°{self.temp_unit}",font=("Times New Roman",14),image=self.down_arrow_pic,compound=tk.LEFT,bg=self.bg_dark_color,fg="#ffffff").grid(row=num+1,column=2)
                    tk.Label(self.forecast_sub_frame2,text=f"High:{five_day_forecast[num][2]}°{self.temp_unit} ",font=("Times New Roman",14),image=self.up_arrow_pic,compound=tk.LEFT,bg=self.bg_dark_color,fg="#ffffff").grid(row=num+1,column=3)
                self.root.update()
                astronomy_response = self.fetch_astronomy_data(confirmed_location)
                astronomy_obj = json.loads(astronomy_response)
                self.canvas1.itemconfig(self.location_city_country, text=astronomy_obj["location"]["region"]+","+astronomy_obj["location"]["country"])
                self.canvas1.itemconfig(self.current_time,text="Local time: "+astronomy_obj["location"]["localtime"][-5:])
                self.moonrise_time_label.config(text=self.change_to_24_hour_format(astronomy_obj["astronomy"]["astro"]["moonrise"]))
                self.moonset_time_label.config(text=self.change_to_24_hour_format(astronomy_obj["astronomy"]["astro"]["moonset"]))
                self.moon_phase_label.config(text=astronomy_obj["astronomy"]["astro"]["moon_phase"],image=self.moon_phases_dict.get(astronomy_obj["astronomy"]["astro"]["moon_phase"]),compound=tk.RIGHT)
                self.thread_fetch_more_current_weather_details(confirmed_location)
                self.thread_fetch_hourly_uv_data(confirmed_location)
            else:
                messagebox.showinfo("Error","Some error occurred. Please try again later!")
        except:
            messagebox.showerror("No Internet connection", "Your device is not connected to the Internet")

    def thread_fetch_current_weather_location(self,confirmed_location):
        thread_var = Thread(target=self.fetch_current_weather_location(confirmed_location))
        thread_var.start()

    def plot_hourly_temperature_bar_chart(self,temperature_list, labels_arr):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        fig = Figure(figsize=(10, 5), dpi=76)
        # adding the subplot
        plot1 = fig.add_subplot(111)
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
        plot1.plot(labels_arr,numpy_temperature_array,linestyle="dashed",color="blue",marker="o",ms=10)
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

    def thread_plot_hourly_temperature_bar_chart(self,arr1,labels_arr):
        thread_var = Thread(target=self.plot_hourly_temperature_bar_chart(arr1,labels_arr))
        thread_var.start()

    def fetch_astronomy_data(self,confirmed_location):
        today_date = str(datetime.datetime.now())[:10]
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
                self.canvas1.itemconfig(self.dew_point_text,text="Dew point: "+str(weather_details["current"]["dewpoint_c"]))
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
    def fetch_hourly_uv_data(self,confirmed_location):
        try:
            uv_forecast_response = requests.get(f"https://api.weatherapi.com/v1/forecast.json?key={self.my_weatherapi_key}&q={confirmed_location[0]},{confirmed_location[1]}&days=1&aqi=no&alerts=no")
            if uv_forecast_response.status_code==200:
                uv_forecast_obj = json.loads(uv_forecast_response.content)
                uv_arr_list = uv_forecast_obj["forecast"]["forecastday"][0]["hour"]
                current_day_uv_hourly_list = []
                index_num = 0
                for every_hour_uv in uv_arr_list:
                    if index_num%2==1:
                        current_day_uv_hourly_list.append(every_hour_uv["uv"])
                    index_num += 1
                self.thread_plot_hourly_uv_index(current_day_uv_hourly_list)
        except:
            messagebox.showerror("Some error occurred","Please try again after sometime.")
    def thread_fetch_hourly_uv_data(self,confirmed_location):
        thread_var = Thread(target=self.fetch_hourly_uv_data(confirmed_location))
        thread_var.start()

    def plot_hourly_uv_index(self,uv_index_list):
        for widget in self.uv_hourly_frame.winfo_children():
            widget.destroy()
        fig = Figure(figsize=(6.5, 2.7), dpi=70)
        # adding the subplot
        plot1 = fig.add_subplot(111)
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

    def detect_user_current_location_by_ip_address(self):
        try:
            self.user_IP_Address = requests.get('https://checkip.amazonaws.com').text.strip()
            self.ip_api_key = "YOUR_IP_API_API_KEY"  # Replace with your API key by registering at apiip
            self.ip_response = requests.get(
                f"https://apiip.net/api/check?ip={self.user_IP_Address}&accessKey={self.ip_api_key}")
            self.ip_address_city = "Delhi"
            if self.ip_response.status_code == 200:
                self.ip_address_obj = json.loads(self.ip_response.content)
                self.ip_address_city = self.ip_address_obj["city"]
            self.thread_initialize_location(self.ip_address_city)
        except:
            messagebox.showerror("No Internet connection","Please connect your device to the Internet")

    def thread_detect_user_current_location_by_ip_address(self):
        thread_var = Thread(target=self.detect_user_current_location_by_ip_address())
        thread_var.start()

    def change_temperature_unit(self):
        if self.temp_unit=="F":
            self.temp_unit = "C"
            self.temperature_unit_string = "metric"
            self.temperature_unit_changing_button.config(text="C")
        else:
            self.temp_unit = "F"
            self.temperature_unit_string = "imperial"
            self.temperature_unit_changing_button.config(text="F")
        self.root.update()
        self.thread_refresh_weather_data()
    def thread_change_temperature_unit(self):
        thread_var = Thread(target=self.change_temperature_unit())
        thread_var.start()
