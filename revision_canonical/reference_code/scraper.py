"""
Simple web scraper utility using BeautifulSoup4.
"""

from bs4 import BeautifulSoup
import requests

# Standard headers to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_contents(url: str) -> str:
    """
    Return the title and text contents of the website at the given URL.
    Removes script, style, img, and input tags.
    Truncates result to 2,000 characters by default.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string if soup.title else "No title found"
        
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""
            
        return (title + "\n\n" + text)[:2000]
    except Exception as e:
        return f"Error fetching {url}: {e}"


def fetch_website_links(url: str) -> list[str]:
    """
    Return a list of href links found on the website at the given URL.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        links = [link.get("href") for link in soup.find_all("a")]
        return [link for link in links if link]
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return []
