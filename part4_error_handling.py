"""
Part 4: Robust Error Handling with Logging & Retry
==================================================
"""

import requests
import time
import logging
from requests.exceptions import (
    ConnectionError,
    Timeout,
    HTTPError,
    RequestException
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def safe_api_request(url, timeout=5, retries=3, retry_delay=2):
    """
    Make an API request with error handling and retry logic.
    
    Args:
        url (str): API endpoint
        timeout (int): seconds to wait for response
        retries (int): number of retry attempts
        retry_delay (int): seconds to wait between retries

    Returns:
        dict: {"success": bool, "data": dict or None, "error": str or None}
    """
    for attempt in range(1, retries + 1):
        try:
            logging.info(f"Requesting URL: {url} (Attempt {attempt})")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except ConnectionError:
            logging.warning("Connection failed. Retrying..." if attempt < retries else "Connection failed.")
            error_msg = "Connection failed. Check your internet."
        except Timeout:
            logging.warning("Timeout occurred. Retrying..." if attempt < retries else "Timeout occurred.")
            error_msg = f"Request timed out after {timeout} seconds."
        except HTTPError as e:
            error_msg = f"HTTP Error: {e.response.status_code}"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}  # <-- FIXED
        except RequestException as e:
            logging.warning(f"Request failed: {str(e)}. Retrying..." if attempt < retries else f"Request failed: {str(e)}")
            error_msg = f"Request failed: {str(e)}"

        if attempt < retries:
            time.sleep(retry_delay)
        else:
            return {"success": False, "error": error_msg}


def validate_crypto_response(data):
    """
    Validate cryptocurrency response structure.
    
    Returns True if valid, False otherwise.
    """
    if not isinstance(data, dict):
        return False
    if "quotes" not in data:
        return False
    if "USD" not in data["quotes"]:
        return False
    return True


def demo_error_handling():
    """Demonstrate different error scenarios."""
    print("=== Error Handling Demo ===\n")

    # Test 1: Successful request
    print("--- Test 1: Valid URL ---")
    result = safe_api_request("https://jsonplaceholder.typicode.com/posts/1")
    if result["success"]:
        print(f"Success! Got post: {result['data']['title'][:30]}...")
    else:
        print(f"Failed: {result['error']}")

    # Test 2: 404 Error
    print("\n--- Test 2: Non-existent Resource (404) ---")
    result = safe_api_request("https://jsonplaceholder.typicode.com/posts/99999")
    if result["success"]:
        print(f"Success! Data: {result['data']}")
    else:
        print(f"Failed: {result['error']}")

    # Test 3: Invalid domain
    print("\n--- Test 3: Invalid Domain ---")
    result = safe_api_request("https://this-domain-does-not-exist-12345.com/api")
    if result["success"]:
        print(f"Success!")
    else:
        print(f"Failed: {result['error']}")

    # Test 4: Timeout simulation
    print("\n--- Test 4: Timeout Simulation ---")
    result = safe_api_request("https://httpstat.us/200?sleep=5000", timeout=1)
    if result["success"]:
        print(f"Success!")
    else:
        print(f"Failed: {result['error']}")


def fetch_crypto_safely():
    """Fetch crypto data with validation and retry logic."""
    print("\n=== Safe Crypto Price Checker ===\n")

    coin = input("Enter coin (btc-bitcoin, eth-ethereum): ").strip().lower()
    if not coin:
        print("Error: Please enter a coin name.")
        return

    url = f"https://api.coinpaprika.com/v1/tickers/{coin}"
    result = safe_api_request(url)

    if result["success"]:
        data = result["data"]
        if validate_crypto_response(data):
            price = data["quotes"]["USD"]["price"]
            change_24h = data["quotes"]["USD"]["percent_change_24h"]
            print(f"\n{data['name']} ({data['symbol']})")
            print(f"Price: ${price:,.2f}")
            print(f"24h Change: {change_24h:+.2f}%")
        else:
            print("Error: Invalid crypto response structure!")
    else:
        print(f"\nError: {result['error']}")
        print("Tip: Try 'btc-bitcoin' or 'eth-ethereum'")


def validate_json_response():
    """Demonstrate JSON validation."""
    print("\n=== JSON Validation Demo ===\n")

    url = "https://jsonplaceholder.typicode.com/users/1"
    result = safe_api_request(url)

    if result["success"]:
        data = result["data"]
        required_fields = ["name", "email", "phone"]
        missing = [f for f in required_fields if f not in data]

        if missing:
            print(f"Warning: Missing fields: {missing}")
        else:
            print("All required fields present!")
            print(f"Name: {data['name']}")
            print(f"Email: {data['email']}")
            print(f"Phone: {data['phone']}")
    else:
        print(f"Error: {result['error']}")


def main():
    """Run all demos."""
    demo_error_handling()
    print("\n" + "=" * 40 + "\n")
    validate_json_response()
    print("\n" + "=" * 40 + "\n")
    fetch_crypto_safely()


if __name__ == "__main__":
    main()
