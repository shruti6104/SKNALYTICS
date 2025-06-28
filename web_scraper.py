import requests
from bs4 import BeautifulSoup

def scrape_amazon(product_name):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    query = product_name.replace(" ", "+")
    url = f"https://www.amazon.in/s?k={query}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    results = []
    for item in soup.select(".s-result-item")[:5]:
        title = item.select_one("h2 span")
        price = item.select_one(".a-price-whole")
        rating = item.select_one(".a-icon-alt")
        link = item.select_one("h2 a")

        if title and price and rating and link:
            results.append({
                "Platform": "Amazon",
                "Product": title.text.strip(),
                "Price (₹)": price.text.strip(),
                "Rating": rating.text.strip(),
                "URL": "https://www.amazon.in" + link['href']
            })

    return results
