import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def fetch_url(url: str) -> str: # Fetches the content of the given URL and returns it as a string.
    response = requests.get(url, timeout=10) 
    response.raise_for_status()  # Raise an error for bad responses
    return response.text

def extract_links(html: str, base_url: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for tag in soup.find_all("a", href=True):
        full_url = urljoin(base_url, tag["href"])
        if full_url.startswith(("http://", "https://")):
            links.add(full_url)

    return links

if __name__ == "__main__":
    url = input("URL to fetch: ")

    try:
        html = fetch_url(url)
        links = extract_links(html, url)
        print(f"Found {len(links)} links")
        for link in sorted(links):
            print(link)
            
        print(f"Downloaded {len(html)} characters")
        print(html[:500])  # Print the first 500 characters of the HTML
    except requests.RequestException as error:
        print(f"Could not fetch page: {error}")