import requests
from bs4 import BeautifulSoup
import json

# Define the URL of the Medium tag page
url = "https://medium.com/tag/python"

# Set headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Send a GET request
response = requests.get(url, headers=headers)

# Check for successful response
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Medium uses 'article' tags for posts
    articles = soup.find_all('article')

    # List to store extracted data
    article_data = []

    for article in articles:
        try:
            # Extract title, author, and summary using appropriate tags
            title_tag = article.find('h2') or article.find('h3') or article.find('h1')
            title = title_tag.get_text(strip=True) if title_tag else "No Title"
            
            author_tag = article.select_one('a[data-testid="author-name"]')
            author = author_tag.get_text(strip=True) if author_tag else "Unknown"

            summary_tag = article.find('p')
            summary = summary_tag.get_text(strip=True) if summary_tag else "No Summary"
            
            # Append data
            article_data.append({
                'Title': title,
                'Author': author,
                'Summary': summary
            })

        except AttributeError as e:
            print(f"Skipping article due to error: {e}")
    
    # Save data to JSON
    with open('medium_articles.json', 'w', encoding='utf-8') as f:
        json.dump(article_data, f, ensure_ascii=False, indent=4)
    
    print("Scraping completed! Data saved to medium_articles.json")

else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
