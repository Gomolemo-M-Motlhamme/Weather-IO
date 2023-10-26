from django.shortcuts import render
import requests as rs
import datetime
from . import API_key

def Index(request):
    APIkey = API_key.getAPI()                                                                   #API key
    current_weather_url = "http://api.openweathermap.org/data/2.5/weather?appid={}&q={}"        #url to fetch current weather
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"    #url to fetch forecasted weather
    

    if request.method == "POST":
        City = request.POST["city"]

        weather_data, daily_forecast = weather_and_forecast(City, APIkey, current_weather_url, forecast_url)

        context = {
            "weather_data": weather_data,
            "daily_forecast": daily_forecast
        }

        return render(request, "Index.html", context)
    else:
        return render(request, "Index.html")

# Get current weather and forecast
def weather_and_forecast(city, api_Key, current_weather_url, forecast_url):
    response = rs.get(current_weather_url.format(api_Key, city)).json()
    data = response  

    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]

    forcast_reponse = rs.get(forecast_url.format(lat, lon, api_Key)).json()

    #current weather
    weather_Data = {
        "city": city,
        "Day": datetime.datetime.fromtimestamp(data["dt"]).strftime("%A"),
        "temperature": round(response["main"]["temp"] - 273.15, 2),
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"]
    }

    #forcasted weather
    daily_forcasts = []
    for daily_Data in forcast_reponse["list"]:

        datetime_str = daily_Data["dt_txt"]
        datetime_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

        day_of_week = datetime_obj.strftime("%A")  # Get the day of the week
        time = datetime_obj.strftime("%H:%M")  # Get the time

        daily_forcasts.append({
            "day": day_of_week,
            "time":time,
            "min_temp": round(daily_Data["main"]["temp_min"] - 273.15, 2),
            "max_temp": round(daily_Data["main"]["temp_max"] - 273.15, 2),
            "description": daily_Data["weather"][0]["description"],
            "icon": daily_Data["weather"][0]["icon"]
        })
    return weather_Data, daily_forcasts
