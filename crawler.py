import requests

def fetch_url(url: str) -> str: # Fetches the content of the given URL and returns it as a string.
    response = requests.get(url, timeout=10) 
    response.raise_for_status()  # Raise an error for bad responses
    return response.text

if __name__ == "__main__":
    url = input("URL to fetch: ")

    try:
        html = fetch_url(url)
        print(f"Downloaded {len(html)} characters")
        print(html[:500])  # Print the first 500 characters of the HTML
    except requests.RequestException as error:
        print(f"Could not fetch page: {error}")
