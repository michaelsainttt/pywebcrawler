from collections import deque
from time import sleep 
from urllib.parse import urlparse, urldefrag, urljoin

import requests
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

def crawl_site(start_url: str, max_pages: int = 5) -> set[str]: # Function to crawl a website starting from the given URL, up to a maximum number of pages.
    start_domain = urlparse(start_url).netloc

    to_visit = deque([start_url]) # Queue to keep track of URLs to visit
    discovered = {start_url} # Set to keep track of discovered URLs
    visited = set() # Set to keep track of visited URLs

    while to_visit and len(visited) < max_pages: # While there are URLs to visit and the number of visited pages is less than the maximum allowed
        current_url = to_visit.popleft()
        visited.add(current_url)

        print(f"\nCrawling: {current_url}")

        try:
            html = fetch_url(current_url)
        except requests.RequestException as error:
            print(f"Could not fetch page: {error}")
            continue

        links = extract_links(html, current_url) # Extract links from the fetched HTML content

        for link in links: # Iterate through all the extracted links
            clean_link, _ = urldefrag(link)  # Remove fragment identifiers
            link_domain = urlparse(clean_link).netloc # Get the domain of the link

            if link_domain == start_domain and clean_link not in discovered:
                discovered.add(clean_link)
                to_visit.append(clean_link)

        sleep(1)  # to avoid overwhelming the server with requests

    return visited
        
if __name__ == "__main__":
    start_url = input("Starting URL: ")

    visited_pages = crawl_site(start_url, max_pages=5)

    print(f"\nFinished crawling {len(visited_pages)} pages:")
    for page in sorted(visited_pages):
        print(page)

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
