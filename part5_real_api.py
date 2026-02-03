"""
Part 5: Real-World APIs - Weather & Crypto Dashboard
====================================================
Difficulty: Advanced
"""

import requests
import json
import os
from datetime import datetime


# ==================================================
# Exercise 1: Added more cities
# ==================================================
CITIES = {
    "delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "hyderabad": (17.3850, 78.4867),
    "pune": (18.5204, 73.8567),
    "nagpur": (21.1458, 79.0882),
    "new york": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "tokyo": (35.6762, 139.6503),
    "sydney": (-33.8688, 151.2093),
}


CRYPTO_IDS = {
    "bitcoin": "btc-bitcoin",
    "ethereum": "eth-ethereum",
    "dogecoin": "doge-dogecoin",
    "cardano": "ada-cardano",
    "solana": "sol-solana",
    "ripple": "xrp-xrp",
}


# ==================================================
# WEATHER (Open-Meteo – Free API)
# ==================================================
def get_weather(city):
    city = city.lower()
    if city not in CITIES:
        print("City not found.")
        return None

    lat, lon = CITIES[city]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def display_weather(city):
    data = get_weather(city)
    if not data:
        return

    weather = data["current_weather"]

    print("\n" + "=" * 40)
    print(f" Weather in {city.title()}")
    print("=" * 40)
    print(f" Temperature : {weather['temperature']} °C")
    print(f" Wind Speed : {weather['windspeed']} km/h")
    print(f" Time       : {weather['time']}")
    print("=" * 40)

    save_to_file("weather_result.json", data)


# ==================================================
# CRYPTO (CoinPaprika – Free API)
# ==================================================
def get_crypto(coin):
    coin_id = CRYPTO_IDS.get(coin.lower())
    if not coin_id:
        return None

    url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def display_crypto(coin):
    data = get_crypto(coin)
    if not data:
        print("Crypto not found.")
        return

    usd = data["quotes"]["USD"]

    print("\n" + "=" * 40)
    print(f" {data['name']} ({data['symbol']})")
    print("=" * 40)
    print(f" Price        : ${usd['price']:.2f}")
    print(f" Market Cap   : ${usd['market_cap']:.0f}")
    print(f" 24h Change   : {usd['percent_change_24h']}%")
    print("=" * 40)

    save_to_file("crypto_result.json", data)


# ==================================================
# Exercise 2: Compare Multiple Cryptos
# ==================================================
def compare_cryptos(coins):
    print("\n" + "=" * 55)
    print(" Crypto Comparison")
    print("=" * 55)
    print(f"{'Coin':<15}{'Price($)':<15}{'24h Change'}")
    print("-" * 55)

    for coin in coins:
        data = get_crypto(coin)
        if data:
            usd = data["quotes"]["USD"]
            print(f"{coin.title():<15}{usd['price']:<15.2f}{usd['percent_change_24h']}%")

    print("=" * 55)


# ==================================================
# Exercise 3: POST Request Example
# ==================================================
def create_post():
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "title": "My Post",
        "body": "This is created using POST request",
        "userId": 1
    }

    response = requests.post(url, json=payload)
    print("\nPOST Response:")
    print(response.json())


# ==================================================
# Exercise 4: Save Results to JSON File
# ==================================================
def save_to_file(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✔ Data saved to {filename}")


# ==================================================
# Exercise 5: API Key Support (Example)
# ==================================================
def openweather_example():
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        print("OpenWeather API key not set.")
        return

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": "Delhi", "appid": api_key, "units": "metric"}

    response = requests.get(url, params=params)
    print(response.json())


# ==================================================
# DASHBOARD
# ==================================================
def dashboard():
    while True:
        print("\n" + "=" * 50)
        print(" Real-World API Dashboard")
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=" * 50)
        print("1. Check Weather")
        print("2. Check Crypto Price")
        print("3. Compare Cryptos")
        print("4. Create POST Request")
        print("5. Exit")

        choice = input("Select (1-5): ")

        if choice == "1":
            city = input("Enter city: ")
            display_weather(city)

        elif choice == "2":
            coin = input("Enter crypto: ")
            display_crypto(coin)

        elif choice == "3":
            coins = input("Enter cryptos (comma separated): ").split(",")
            compare_cryptos([c.strip() for c in coins])

        elif choice == "4":
            create_post()

        elif choice == "5":
            print("Goodbye 👋")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    dashboard()
