headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

url = f"https://www.amazon.in/s?k={product_query.replace(' ', '+')}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.select("span.a-text-normal")
    prices = soup.select("span.a-price-whole")
    ratings = soup.select("span.a-icon-alt")

    # Return first result
    product = {
        "Platform": "Amazon",
        "Product Name": titles[0].text.strip(),
        "Price (₹)": prices[0].text.strip(),
        "Rating": ratings[0].text.strip().split()[0],
        "Top Review": "Not available via scraper"
    }
    return [product]
