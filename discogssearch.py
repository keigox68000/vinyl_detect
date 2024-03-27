import discogs_client
import requests
import os

# Discogsクライアントの設定
USER_AGENT = 'ExampleApplication/0.1'
ACCESS_TOKEN = 'UUYXPIkYajiPYzaZnFHzIBztMBRrpVQabGEcOGOC'
d = discogs_client.Client(USER_AGENT, user_token=ACCESS_TOKEN)

def search_album_and_save_art(keyword):
    """キーワードで検索し、最初のリリースのアルバムアートを保存します。"""
    try:
        results = d.search(keyword, type='release')
        result = next(iter(results), None)  # 最初の結果を取得
        if result is not None and result.images:
            artist_name = result.artists[0].name if result.artists else 'Unknown Artist'
            album_title = result.title
            primary_image = next((image for image in result.images if image['type'] == 'primary'), None)
            if primary_image:
                filename = f"{album_title}-{artist_name}".replace("/", "-") # スラッシュを避ける
                save_album_art(primary_image['uri'], filename)
            else:
                print(f"No primary image available for {keyword}")
        else:
            print(f"No results found for {keyword}")
    except Exception as e:
        print(f"Error processing {keyword}: {e}")

def save_album_art(image_url, filename):
    """アルバムアートをダウンロードして保存します。"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.discogs.com/'
    }
    try:
        response = requests.get(image_url, headers=headers)
        response.raise_for_status()
        valid_filename = "".join(char for char in filename if char.isalnum() or char in " _-").replace("/", "-") # スラッシュを避ける
        file_path = os.path.join('.', f'{valid_filename}.jpg')
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'Album art saved to {file_path}')
    except requests.RequestException as e:
        print(f'Error downloading album art for {filename}: {e}')

# result.txtからキーワードを読み込んで処理
with open('result.txt', 'r') as file:
    for line in file:
        parts = line.strip().split(':')
        if len(parts) == 2:
            _, keyword = parts
            search_album_and_save_art(keyword)
        else:
            print(f"Invalid line format: {line}")
