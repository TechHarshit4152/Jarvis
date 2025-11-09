import requests
import random



def is_online():
    try:
        response = requests.get("https://www.google.com", timeout=2)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        return False
    return False  # In case of any failure

# Example usage

