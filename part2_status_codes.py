"""
Part 2: Status Codes and JSON Parsing
=====================================
Difficulty: Beginner+

Learn:
- Understanding HTTP status codes
- Parsing JSON data like a Python dictionary
- Accessing specific fields from API response
"""

import requests

# --- ORIGINAL CODE (from Part 2) ---
print("=== Understanding Status Codes ===\n")

# Example 1: Successful request (200 OK)
print("--- Example 1: Valid Request ---")
url_valid = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url_valid)
print(f"URL: {url_valid}")
print(f"Status Code: {response.status_code}")
print(f"Success? {response.status_code == 200}")

# Example 2: Not Found (404)
print("\n--- Example 2: Invalid Request (404) ---")
url_invalid = "https://jsonplaceholder.typicode.com/posts/99999"
response_404 = requests.get(url_invalid)
print(f"URL: {url_invalid}")
print(f"Status Code: {response_404.status_code}")
print(f"Found? {response_404.status_code == 200}")

# Example 3: Parsing JSON Data
print("\n--- Example 3: Parsing JSON ---")
url = "https://jsonplaceholder.typicode.com/users/1"
response = requests.get(url)
data = response.json()
print(f"Full Name: {data['name']}")
print(f"Username: {data['username']}")
print(f"Email: {data['email']}")
print(f"City: {data['address']['city']}")
print(f"Company: {data['company']['name']}")

# Example 4: Working with a list of items
print("\n--- Example 4: List of Items ---")
url_list = "https://jsonplaceholder.typicode.com/posts?userId=1"
response = requests.get(url_list)
posts = response.json()
print(f"User 1 has {len(posts)} posts:")
for i, post in enumerate(posts[:3], 1):
    print(f"  {i}. {post['title'][:40]}...")

# --- UPDATED CODE (SOLUTIONS) ---

print("\n" + "="*20)
print("   EXERCISE SOLUTIONS")
print("="*20)

# Exercise 1: Fetch user with ID 5 and print their phone number
print("\n--- Exercise 1: User 5 Phone ---")
ex1_url = "https://jsonplaceholder.typicode.com/users/5"
ex1_response = requests.get(ex1_url)
ex1_data = ex1_response.json()
print(f"Phone number for User 5 ({ex1_data['name']}): {ex1_data['phone']}")

# Exercise 2: Check if a resource exists before printing data
print("\n--- Exercise 2: Status Check Logic ---")
test_id = 500 # This ID doesn't exist in the placeholder API
ex2_url = f"https://jsonplaceholder.typicode.com/posts/{test_id}"
ex2_response = requests.get(ex2_url)

if ex2_response.status_code == 200:
    ex2_data = ex2_response.json()
    print(f"Post {test_id} Data: {ex2_data}")
else:
    print(f"Resource {test_id} not found! Status Code: {ex2_response.status_code}")

# Exercise 3: Count how many comments are on post ID 1
print("\n--- Exercise 3: Comment Count ---")
ex3_url = "https://jsonplaceholder.typicode.com/posts/1/comments"
ex3_response = requests.get(ex3_url)
comments = ex3_response.json()
print(f"Number of comments on Post ID 1: {len(comments)}")


# --- EXERCISES ---
#
# Exercise 1: Fetch user with ID 5 and print their phone number
#             URL: https://jsonplaceholder.typicode.com/users/5
#
# Exercise 2: Check if a resource exists before printing data
#             if response.status_code == 200:
#                 print(data)
#             else:
#                 print("Resource not found!")
#
# Exercise 3: Count how many comments are on post ID 1
#             URL: https://jsonplaceholder.typicode.com/posts/1/comments
