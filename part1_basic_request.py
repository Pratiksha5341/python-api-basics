"""
Part 1: Basic GET Request
=========================
Difficulty: Beginner

Learn: How to make a simple GET request and view the response.

We'll use JSONPlaceholder - a free fake API for testing.
"""

import requests

headers = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises error for 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print("❌ Error:", e)
        return None


print("===================================")
print(" Exercise 1: Fetch Post #5")
print("===================================")

url_post_5 = "https://jsonplaceholder.typicode.com/posts/5"
data1 = fetch_data(url_post_5)

if data1:
    print(data1)


print("\n===================================")
print(" Exercise 2: Fetch All Users")
print("===================================")

url_users = "https://jsonplaceholder.typicode.com/users"
data2 = fetch_data(url_users)

if data2:
    print(data2)


print("\n===================================")
print(" Exercise 3: Fetch Invalid Post")
print("===================================")

url_invalid = "https://jsonplaceholder.typicode.com/posts/999"
data3 = fetch_data(url_invalid)

if data3:
    print(data3)
else:
    print("No data found.")

# --- EXERCISES ---
# Try these on your own:
#
# Exercise 1: Change the URL to fetch post number 5
#             Hint: Change /posts/1 to /posts/5
#
# Exercise 2: Fetch a list of all users
#             URL: https://jsonplaceholder.typicode.com/users
#
# Exercise 3: What happens if you fetch a post that doesn't exist?
#             Try: https://jsonplaceholder.typicode.com/posts/999
