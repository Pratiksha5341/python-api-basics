"""
Part 3: Dynamic Queries with User Input
=======================================
Difficulty: Intermediate

Learn:
- Using input() to make dynamic API requests
- Building URLs with f-strings
- Query parameters in URLs
"""

"""
Part 3: Dynamic Queries with User Input
=======================================
Difficulty: Intermediate
"""

import requests

# Mapping some cities to latitude/longitude for weather exercise
CITY_COORDINATES = {
    "delhi": (28.61, 77.23),
    "mumbai": (19.07, 72.87),
    "bangalore": (12.97, 77.59),
    "chennai": (13.08, 80.27),
    "kolkata": (22.57, 88.36)
}


def get_user_info():
    """Fetch user info based on user input with validation."""
    print("=== User Information Lookup ===\n")
    
    user_id = input("Enter user ID (1-10): ").strip()
    if not user_id.isdigit() or not (1 <= int(user_id) <= 10):
        print("Invalid user ID! Must be a number between 1 and 10.")
        return

    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"\n--- User #{user_id} Info ---")
        print(f"Name: {data['name']}")
        print(f"Email: {data['email']}")
        print(f"Phone: {data['phone']}")
        print(f"Website: {data['website']}")
    else:
        print(f"\nUser with ID {user_id} not found!")


def search_posts():
    """Search posts by user ID with validation."""
    print("\n=== Post Search ===\n")
    
    user_id = input("Enter user ID to see their posts (1-10): ").strip()
    if not user_id.isdigit() or not (1 <= int(user_id) <= 10):
        print("Invalid user ID! Must be a number between 1 and 10.")
        return

    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"userId": user_id}

    response = requests.get(url, params=params)
    posts = response.json()

    if posts:
        print(f"\n--- Posts by User #{user_id} ---")
        for i, post in enumerate(posts, 1):
            print(f"{i}. {post['title']}")
    else:
        print("No posts found for this user.")


def get_crypto_price():
    """Fetch cryptocurrency price based on user input."""
    print("\n=== Cryptocurrency Price Checker ===\n")

    print("Available coins: btc-bitcoin, eth-ethereum, doge-dogecoin")
    coin_id = input("Enter coin ID (e.g., btc-bitcoin): ").lower().strip()

    url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        price_usd = data['quotes']['USD']['price']
        change_24h = data['quotes']['USD']['percent_change_24h']

        print(f"\n--- {data['name']} ({data['symbol']}) ---")
        print(f"Price: ${price_usd:,.2f}")
        print(f"24h Change: {change_24h:+.2f}%")
    else:
        print(f"\nCoin '{coin_id}' not found!")
        print("Try: btc-bitcoin, eth-ethereum, doge-dogecoin")


def get_weather():
    """Fetch current weather for a city."""
    print("\n=== Weather Checker ===\n")
    print("Available cities:", ", ".join(CITY_COORDINATES.keys()))
    
    city = input("Enter city name: ").lower().strip()
    if city not in CITY_COORDINATES:
        print("City not available! Try one from the list.")
        return

    lat, lon = CITY_COORDINATES[city]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather = data.get("current_weather", {})
        print(f"\n--- Weather in {city.title()} ---")
        print(f"Temperature: {weather.get('temperature', 'N/A')}°C")
        print(f"Wind Speed: {weather.get('windspeed', 'N/A')} km/h")
        print(f"Weather Code: {weather.get('weathercode', 'N/A')}")
    else:
        print("Failed to fetch weather data.")


def search_todos():
    """Search todos by completion status."""
    print("\n=== Todo Search ===\n")
    status = input("Show completed todos? (yes/no): ").lower().strip()
    
    if status not in ["yes", "no"]:
        print("Invalid input! Enter 'yes' or 'no'.")
        return

    completed = True if status == "yes" else False
    url = "https://jsonplaceholder.typicode.com/todos"
    params = {"completed": completed}
    
    response = requests.get(url, params=params)
    todos = response.json()

    if todos:
        print(f"\n--- Todos where completed={completed} ---")
        for i, todo in enumerate(todos[:10], 1):  # Show only first 10 for brevity
            print(f"{i}. {todo['title']}")
        if len(todos) > 10:
            print(f"...and {len(todos)-10} more todos.")
    else:
        print("No todos found.")


def main():
    """Main menu for the program."""
    print("=" * 40)
    print("  Dynamic API Query Demo")
    print("=" * 40)

    while True:
        print("\nChoose an option:")
        print("1. Look up user info")
        print("2. Search posts by user")
        print("3. Check crypto price")
        print("4. Check weather")
        print("5. Search todos by completion")
        print("6. Exit")

        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            get_user_info()
        elif choice == "2":
            search_posts()
        elif choice == "3":
            get_crypto_price()
        elif choice == "4":
            get_weather()
        elif choice == "5":
            search_todos()
        elif choice == "6":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


# --- EXERCISES ---
#
# Exercise 1: Add a function to fetch weather for a city
#             Use Open-Meteo API (no key required):
#             https://api.open-meteo.com/v1/forecast?latitude=28.61&longitude=77.23&current_weather=true
#             Challenge: Let user input city name (you'll need to find lat/long)
#
# Exercise 2: Add a function to search todos by completion status
#             URL: https://jsonplaceholder.typicode.com/todos
#             Params: completed=true or completed=false
#
# Exercise 3: Add input validation (check if user_id is a number)
