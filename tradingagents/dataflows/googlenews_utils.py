import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    retry_if_result,
)


def is_rate_limited(response):
    """Check if the response indicates rate limiting (status code 429)"""
    return response.status_code == 429


@retry(
    retry=(retry_if_result(is_rate_limited)),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
)
def make_request(url, headers):
    """Make a request with retry logic for rate limiting"""
    # Random delay before each request to avoid detection
    time.sleep(random.uniform(2, 6))
    response = requests.get(url, headers=headers)
    return response


def debug_page_structure(soup, page_num):
    """Debug function to understand the page structure"""
    print(f"\n=== DEBUG: Page {page_num} Structure ===")
    
    # Check for common news result containers
    containers = soup.select("div[class*='g']")[:3]  # First 3 results
    for i, container in enumerate(containers):
        print(f"\nContainer {i+1} classes: {container.get('class', [])}")
        
        # Look for links
        links = container.find_all("a")
        print(f"  Links found: {len(links)}")
        
        # Look for text content
        text_divs = container.find_all("div")
        for j, div in enumerate(text_divs[:5]):  # First 5 divs
            if div.get_text(strip=True):
                print(f"  Div {j}: class={div.get('class', [])}, text='{div.get_text(strip=True)[:50]}...'")


def getNewsData(query, start_date, end_date, debug=False, max_pages=10):
    """
    Scrape Google News search results for a given query and date range.
    query: str - search query
    start_date: str - start date in the format yyyy-mm-dd or mm/dd/yyyy
    end_date: str - end date in the format yyyy-mm-dd or mm/dd/yyyy
    debug: bool - whether to print debug information
    max_pages: int - maximum number of pages to scrape (default: 10)
    """
    if "-" in start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        start_date = start_date.strftime("%m/%d/%Y")
    if "-" in end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        end_date = end_date.strftime("%m/%d/%Y")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/101.0.4951.54 Safari/537.36"
        )
    }

    news_results = []
    page = 0
    while page < max_pages:
        offset = page * 10
        url = (
            f"https://www.google.com/search?q={query}"
            f"&tbs=cdr:1,cd_min:{start_date},cd_max:{end_date}"
            f"&tbm=nws&start={offset}"
        )

        try:
            response = make_request(url, headers)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Debug: Print the page structure
            if debug:
                debug_page_structure(soup, page)
            
            # Try multiple selectors for news results
            results_on_page = []
            result_selectors = ["div.SoaBEf", ".g", ".Gx5Zad", ".xpd"]
            
            for selector in result_selectors:
                results_on_page = soup.select(selector)
                if results_on_page:
                    if debug:
                        print(f"Found {len(results_on_page)} results using selector: {selector}")
                    break
            
            if not results_on_page:
                print(f"No results found on page {page} with any selector")
                if debug:
                    print(f"Response status: {response.status_code}")
                    print(f"Response content length: {len(response.content)}")
                break  # No more results found

            for el in results_on_page:
                try:
                    # Extract link with fallback
                    link_elem = el.find("a")
                    if not link_elem or not link_elem.get("href"):
                        continue
                    link = link_elem["href"]
                    
                    # Extract title with multiple selector options and fallback
                    title = None
                    title_selectors = ["div.MBeuO", ".MBeuO", "h3", ".DY5T1d"]
                    for selector in title_selectors:
                        title_elem = el.select_one(selector)
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            break
                    
                    if not title:
                        continue  # Skip if no title found
                    
                    # Extract snippet with multiple selector options and fallback
                    snippet = ""
                    snippet_selectors = [".GI74Re", ".Y3v8qd", ".st"]
                    for selector in snippet_selectors:
                        snippet_elem = el.select_one(selector)
                        if snippet_elem:
                            snippet = snippet_elem.get_text(strip=True)
                            break
                    
                    # Extract date with multiple selector options and fallback
                    date = ""
                    date_selectors = [".LfVVr", ".f", ".slp"]
                    for selector in date_selectors:
                        date_elem = el.select_one(selector)
                        if date_elem:
                            date = date_elem.get_text(strip=True)
                            break
                    
                    # Extract source with multiple selector options and fallback
                    source = ""
                    source_selectors = [".NUnG9d span", ".fxgdke", ".CEMjEf"]
                    for selector in source_selectors:
                        source_elem = el.select_one(selector)
                        if source_elem:
                            source = source_elem.get_text(strip=True)
                            break
                    
                    # Only add result if we have at least title and link
                    if title and link:
                        news_results.append(
                            {
                                "link": link,
                                "title": title,
                                "snippet": snippet,
                                "date": date,
                                "source": source,
                            }
                        )
                        if debug:
                            print(f"  Added result: {title[:50]}...")
                        
                except Exception as e:
                    if debug:
                        print(f"Error processing result: {e}")
                    # If one of the fields is not found, skip this result
                    continue

            # Update the progress bar with the current count of results scraped

            # Check for the "Next" link (pagination)
            next_link = soup.find("a", id="pnnext")
            if not next_link:
                break

            page += 1

        except Exception as e:
            print(f"Failed after multiple retries: {e}")
            break

    return news_results
