import requests
from bs4 import BeautifulSoup
import re
import time
import csv
import argparse
import os

def load_existing_urls(metadata_file_handle):
    """
    Loads existing article URLs from the metadata file into a set.

    Args:
    metadata_file_handle (file object): An open file handle for the article metadata CSV.

    Returns:
    set: A set of existing article URLs.
    """
    existing_urls = set()
    try:
        metadata_file_handle.seek(0)  # Go to the beginning of the file
        reader = csv.reader(metadata_file_handle)
        next(reader)  # Skip header
        for row in reader:
            existing_urls.add(row[1])
    except StopIteration:  # In case the file is empty and has no header
        pass
    return existing_urls


def fetch_random_article(language, existing_urls, metadata_file):
    """
    Fetches a random Wikipedia article in the specified language and writes its metadata to a CSV file
    if it's not a duplicate.

    Args:
    language (str): The language of the Wikipedia (e.g., 'en' for English, 'nl' for Dutch, 'it' for Italian).
    existing_urls (set): A set of URLs of already fetched articles.
    metadata_file (str): The file path for the article metadata CSV.
    """
    time.sleep(8)  # Rate limiting - pause for 8 seconds between requests for wikipedia's api limit
    url = f"https://{language}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnnamespace": 0,
        "rnlimit": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    title = data['query']['random'][0]['title']
    pageid = data['query']['random'][0]['id']
    article_url = f"https://{language}.wikipedia.org/wiki/{title.replace(' ', '_')}"

#    if article_url not in existing_urls:
#        existing_urls.add(article_url)
    write_article_metadata(metadata_file, language, pageid, article_url)
    # Fetch the full article content using a separate API request
    params = {
        "action": "parse",
        "pageid": pageid,
        "format": "json",
        "prop": "text"
    }
    response = requests.get(url, params=params)
    content_data = response.json()
    html_content = content_data["parse"]["text"]["*"]

    # Use BeautifulSoup to extract clean text from HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()
    return pageid, text_content
#    else:
#        return fetch_random_article(language, existing_urls, metadata_file)

def write_article_metadata(file_handle, language, pageid, url):
    """
    Writes article metadata to an open CSV file handle.

    Args:
    file_handle (file object): An open file handle for the article metadata CSV.
    language (str): Language of the article.
    pageid (int): Page ID of the article.
    url (str): URL of the article.
    """
    writer = csv.writer(file_handle)
    writer.writerow([language + '_' + str(pageid), url])

def extract_segments(text, lengths, language, pageid, file_handles):
    """
    Extracts segments of specified lengths from the text and writes them to open file handles.

    Args:
    text (str): The text from which to extract segments.
    lengths (list of int): A list of segment lengths to extract.
    language (str): The language of the text.
    pageid (int): The page ID of the article.
    file_handles (dict): A dictionary of open file handles.
    """
    words = text.split()
    for length in lengths:
        if len(words) >= length:
            segment_file = f"{language}_{length}_data.csv"
            segment = ' '.join(words[:length])
            writer = csv.writer(file_handles[segment_file])
            writer.writerow([language, language + '_' + str(pageid), length, segment])
            words = words[length:]

def main():
    parser = argparse.ArgumentParser(description='Fetch random Wikipedia articles for language detection data.')
    parser.add_argument('languages', nargs='+', help='Languages to fetch articles for (e.g., en nl it)')
    parser.add_argument('num_articles', type=int, help='Number of articles to fetch for each language')

    args = parser.parse_args()

    article_metadata_file = "article_metadata.csv"
    with open(article_metadata_file, 'a+', newline='', encoding='utf-8') as metadata_file_handle:
        existing_urls = load_existing_urls(metadata_file_handle)
        file_handles = {}

        # Initialize and open files for each language and segment length
        for language in args.languages:
            for length in [10, 20, 50]:
                filename = f"{language}_{length}_data.csv"
                file_exists = os.path.exists(filename)  # Check if file already exists
                file_handles[filename] = open(filename, 'a', newline='', encoding='utf-8')  # Open for appending
                if not file_exists:
                    # Write header only if file is being created
                    writer = csv.writer(file_handles[filename])
                    writer.writerow(["Language", "ArticleID", "TextLength", "TextContent"])

        # Fetch articles and process data
        for language in args.languages:
            for _ in range(args.num_articles):
                try:
                    pageid, article_text = fetch_random_article(language, existing_urls, metadata_file_handle)
                    extract_segments(article_text, [10, 20, 50], language, pageid, file_handles)
                except TypeError:
                    # Handle the case where fetch_random_article returns None
                    continue

        # Close all file handles for segment files
        for file in file_handles.values():
            file.close()

if __name__ == "__main__":
    main()
