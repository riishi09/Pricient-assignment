# Create your views here.
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import json
from itertools import zip_longest


def get_yelp_data():
    # Fetch Village restaurant details
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    url = "https://api.yelp.com/v3/businesses/search"
    params = {"term": "Village", "location": "Hicksville, NY", "limit": 1}
    response = requests.get(url, headers=headers, params=params).json()
    # print(response)

    # Parse and store restaurant data
    village = response["businesses"][0]
    # print(village)
    # print(village["address"])
    return village


def get_items():
    url = "https://www.yelp.com/menu/village-the-soul-of-india-hicksville"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    menu = []
    # Example: Extract menu items
    menu_items = soup.find_all(
        class_="arrange_unit arrange_unit--fill menu-item-details menu-item-no-photo"
    )
    # print(menu_items.text.split("\n")[2])
    for item in menu_items:
        menu.append(item.text.split("\n")[2])
        # print(item.text)
    return menu


def item_price():
    url = "https://www.yelp.com/menu/village-the-soul-of-india-hicksville"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    price = []
    # Example: Extract menu items
    item_price = soup.find_all(class_="menu-item-price-amount")
    # print(item_price.text.split("$")[1])
    for item in item_price:
        price.append((item.text.split("$")[1].split(" ")[0].split("\n")[0]))
        # print(item.text)
    return price


def get_restaurants():
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    url = "https://api.yelp.com/v3/businesses/search"
    params = {
        "latitude": 40.76656,
        "longitude": -73.52353,
        "radius": 2000,
        "sort_by": "rating",
        "limit": 5,
    }
    response = requests.get(url, headers=headers, params=params).json()
    return response


def place_info():
    # address = "11 West Marie St, Hicksville, NY 11801"
    # params = {"key": GMAPS_API_KEY, "address": address}
    # place_details = get_place_details("ChIJPYSDLXWBwokRHLcHIl02Kh8", GMAPS_API_KEY)
    url = f"https://places.googleapis.com/v1/places/ChIJPYSDLXWBwokRHLcHIl02Kh8?fields=places&key={GMAPS_API_KEY}"

    response = requests.get(url).json()
    # print(place_details)


def get_weather_data():
    # Fetch weather data
    location = {"lat": 40.7685, "lon": -73.5251}
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={location['lat']}&lon={location['lon']}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url).json()
    temp_kelvin = response["main"]["temp"]
    temp_min = response["main"]["temp_min"]
    temp_max = response["main"]["temp_max"]
    weather = response["weather"][0]["main"]

    # Convert temperature
    temp_fahrenheit = (temp_kelvin - 273.15) * 9 / 5 + 32
    temp_min_fahrenheit = (temp_min - 273.15) * 9 / 5 + 32
    temp_max_fahrenheit = (temp_max - 273.15) * 9 / 5 + 32
    # print(response)
    # print(temp_fahrenheit)
    # print(weather)

    return {
        "temp": temp_fahrenheit,
        "weather": weather,
        "tempMin": temp_min_fahrenheit,
        "tempMax": temp_max_fahrenheit,
    }


def predict_prices():
    # Example pricing logic
    weather = get_weather_data()
    item = get_items()
    price = item_price()
    is_cold = weather["temp"] < 45
    is_rainy = "rain" in weather["weather"]

    predictions = []
    for p, i in zip(price, item):
        x = float(p)
        predicted_price = (x * 1.3) if is_cold or is_rainy else x
        predictions.append({f"{i}": predicted_price})
    # print(predictions)
    return predictions


def index(request):
    village = get_yelp_data()
    restaurants = get_restaurants()
    weather = get_weather_data()
    place = place_info()
    predictions = predict_prices()

    context = {
        "village": village,
        "restaurants": restaurants,
        "weather": weather,
        "predictions": predictions,
        "place": place,
    }
    return render(request, "info.html", context)
