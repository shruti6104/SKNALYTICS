# product_compare.py

import random

# Simulated Data - Replace with actual scraping or APIs later
def get_mock_data(product_name):
    platforms = ['Amazon', 'Flipkart', 'Nykaa', 'Myntra']
    
    mock_data = []
    for platform in platforms:
        entry = {
            'Platform': platform,
            'Product Name': product_name,
            'Price (₹)': round(random.uniform(299, 1499), 2),
            'Rating': round(random.uniform(3.5, 5.0), 1),
            'Top Review': f"This {product_name} is really amazing on {platform}! Loved it ❤️"
        }
        mock_data.append(entry)

    return mock_data


# Function to get product comparison data as DataFrame
def get_product_comparison(product_name):
    data = get_mock_data(product_name)
    return data
