import requests
from bs4 import BeautifulSoup
from time import perf_counter

def analyze_page(url):

    try:
        start = perf_counter()
        response = requests.get(url, timeout=5)
        response_time = perf_counter() - start

        status_code = response.status_code
        headers = response.headers

        is_working = 200 <= status_code < 400
        redirect_count = len(response.history)
        redirect_statuses = [item.status_code for item in response.history]


        return {
            "url" : url,
            "status_code" : status_code,
            "response_time" : response_time,
            "headers" : headers,
            "is_working" : is_working,
            "redirect_count" : redirect_count,
            "redirect_statuses" : redirect_statuses
        }
    except requests.RequestException as error:
        return {
            "url" : url,
            "status_code" : None,
            "response_time" : None,
            "is_working" : None,
            "redirect_count" : None,
            "redirect_statuses" : None,
            "error" : str(error),
        }


result = analyze_page("https://example.com")

print(result)