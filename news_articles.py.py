import requests
from newsapi import NewsApiClient
import webbrowser

# Initialize NewsAPI client with your API key
newsapi = NewsApiClient(api_key='be60432b0f894a3d9f4a0f922a0d4c53')  # Your confirmed key

def get_news(query):
    try:
        # Fetch the latest 100 articles based on the user's query
        response = newsapi.get_everything(
            q=query,
            language='en',
            sort_by='publishedAt',  # Sort by publication date to get latest
            page_size=100          # Set to maximum allowed articles per request
        )
        if response.get('status') != 'ok':
            print(f"API response error: {response.get('message', 'Unknown error')}")
            return []
        return response.get('articles', [])
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def display_news(articles):
    if not articles:
        print("No articles found for your query.")
        return
    for i, article in enumerate(articles, 1):
        title = article.get('title', 'No title available')
        url = article.get('url', '')
        print(f"{i}. {title}")
        print(f"   URL: {url}\n")
        print(f"Click to open: {url}\n")

def open_article(url):
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Error opening URL: {e}")

def main():
    print("What kind of news are you interested in today?")
    query = input("Enter a topic (e.g., technology, sports, politics): ").strip()
    if not query:
        print("Please enter a valid topic.")
        return
    articles = get_news(query)
    display_news(articles)
    
    while articles:
        choice = input("Enter the number of the article to open (or 'q' to quit): ").strip()
        if choice.lower() == 'q':
            break
        try:
            choice = int(choice)
            if 1 <= choice <= len(articles):
                open_article(articles[choice-1]['url'])
            else:
                print(f"Please enter a number between 1 and {len(articles)}.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

if __name__ == "__main__":
    main()