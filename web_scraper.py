import requests
from bs4 import BeautifulSoup

def scrape_amazon(query, max_results=5):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9"
    }

    search_url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find_all("div", {"data-component-type": "s-search-result"})

    results = []

    for item in items[:max_results]:
        # Title
        title_tag = item.select_one("span.a-text-normal")
        title = title_tag.text.strip() if title_tag else "No Title Found"

        # Price
        price_tag = item.select_one("span.a-price-whole")
        price = price_tag.text.strip().replace(",", "") if price_tag else "0"

        # Rating
        rating_tag = item.select_one("span.a-icon-alt")
        rating = rating_tag.text.strip().split()[0] if rating_tag else "0"

        # Product URL
        link_tag = item.find("a", {"class": "a-link-normal"})
        product_url = f"https://www.amazon.in{link_tag['href']}" if link_tag else "#"

        try:
            price = float(price)
        except:
            price = 0.0

        results.append({
            "Product": title,
            "Price (₹)": price,
            "Rating": rating,
            "URL": product_url
        })

    return results
