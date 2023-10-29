import requests
import re
import os

def fetch_photos_from_instagram(USER_ID, ACCESS_TOKEN):
    endpoint = f"https://graph.facebook.com/v18.0/{USER_ID}/media?fields=id,caption,media_type,media_url&access_token={ACCESS_TOKEN}"
    response = requests.get(endpoint)
    return response.json()

def extract_hashtags_from_caption(data):
    hashtags = []
    for photo in data['data']:
        if photo.get('caption'):
            hashtags.extend(re.findall(r"#(\w+)", photo['caption']))
    return hashtags

def download_photo(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def filter_photos_by_hashtag(data, HASHTAG):
    return [photo for photo in data['data'] if photo.get('caption') and HASHTAG in photo['caption']]

def save_photos_to_directory(photo_urls, user_id, photobook_name):
    save_directory = os.path.join("/app/app/static/images", user_id, photobook_name)
    os.makedirs(save_directory, exist_ok=True)

    saved_photos = []
    for i, url in enumerate(photo_urls):
        filename = os.path.join(save_directory, f"photo_{i}.jpg")
        download_photo(url, filename)
        saved_photos.append(filename)
    
    return saved_photos
