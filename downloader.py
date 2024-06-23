import os
import requests
from bs4 import BeautifulSoup
import requests_cache

BASE_URL = "https://www.teanglann.ie/en/fuaim/"

# Enable requests caching
requests_cache.install_cache('web_page_cache', expire_after=3600)

def download_audio_files(word, dialect=None):
    # Create the directory structure
    word_directory = os.path.join("audio", word)
    os.makedirs(word_directory, exist_ok=True)

    # Fetch the page content
    word_url = BASE_URL + word.lower()
    response = requests.get(word_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract audio URLs
    audio_urls = _extract_audio_urls(soup, dialect)

    # Download audio files
    for audio_url, audio_dialect in audio_urls:
        audio_filename = audio_dialect + ".mp3"
        audio_filepath = os.path.join(word_directory, audio_filename)
        _download_file(audio_url, audio_filepath)
        print(f"Downloaded audio file: {audio_filename}")

def _extract_audio_urls(soup, dialect):
    audio_urls = []
    audio_divs = soup.find_all('div', class_='recording')
    for audio_div in audio_divs:
        audio_tag = audio_div.find('audio')
        audio_url = audio_tag['src'] if audio_tag else None
        audio_dialect = audio_div.find('div', class_='dialect').text.strip()
        if audio_url:
            audio_urls.append((audio_url, audio_dialect))

    # Filter audio URLs by dialect if provided
    if dialect:
        audio_urls = [(url, d.replace(" DIALECT", "")) for url, d in audio_urls if dialect.lower() in d.lower()]

    return audio_urls

def _download_file(url, filepath):
    if url.startswith("/"):
        url = "https://www.teanglann.ie" + url

    response = requests.get(url)
    with open(filepath, 'wb') as f:
        f.write(response.content)

# Example usage:
# download_audio_files("cabhair", dialect="ULSTER")
download_audio_files("cabhair")

