import requests
from configparser import ConfigParser

# 設定を読み込む
config = ConfigParser()
config.read('setting.ini')
integration_token = config.get('notion', 'integration')
database_id = config.get('notion', 'databaseID')

def add_to_notion(title, band, image_url):
    url = "https://api.notion.com/v1/pages"

    headers = {
        "Authorization": f"Bearer {integration_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Title": {  # Notionデータベースのタイトル列名に合わせてください
                "title": [{"text": {"content": title}}]
            },
            "Band": {  # Notionデータベースのバンド列名に合わせてください
                "rich_text": [{"text": {"content": band}}]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": image_url
                    }
                }
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"Successfully added {title} by {band} with image to Notion.")
    else:
        print(f"Failed to add to Notion: {response.text}")

# output.txtファイルからデータを読み込む
with open('output.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if not line:
            continue  # 空行はスキップ
        
        # URLの前後処理
        if 'https://' in line:
            parts = line.split('https://')
            title_band = parts[0].strip()
            url = 'https://' + parts[1].strip()
        else:
            print(f"Invalid line format, skipping: {line}")
            continue
        
        # '/'が含まれているかどうか確認
        if '/' in title_band:
            title, band = title_band.split('/', 1)
        else:
            print(f"No separator found in title_band, using full line as title: {title_band}")
            title = title_band  # または適切なデフォルト値
            band = "Unknown"  # バンド名が不明な場合のデフォルト値
        
        title = title.strip()
        band = band.strip()
        
        # Notionへの追加処理を行う
        add_to_notion(title, band, url)
