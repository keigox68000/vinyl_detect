import discogs_client
import configparser
import os

# 設定ファイルからアクセストークンを読み込む
config = configparser.ConfigParser()
config.read('setting.ini')
ACCESS_TOKEN = config['discogs']['access_token']

# Discogsクライアントの設定
USER_AGENT = 'ExampleApplication/0.1'
d = discogs_client.Client(USER_AGENT, user_token=ACCESS_TOKEN)

def search_albums_and_save_results(keyword):
    """キーワードで検索し、結果をoutput.txtに保存します。"""
    try:
        results = d.search(keyword, type='release')
        if results:  # 検索結果がある場合
            result = next(iter(results), None)  # 最初の検索結果を取得
            if result:
                full_title = result.title
                # アルバムタイトルからアーティスト名を取り除く
                if ' - ' in full_title:
                    album_title = full_title.split(' - ')[1]
                else:
                    album_title = full_title
                artist_name = result.artists[0].name if result.artists else 'Unknown Artist'
                album_art_url = result.images[0]['uri'] if result.images else 'No Image'
                with open('output.txt', 'a') as file:
                    file.write(f'{album_title}/{artist_name}/{album_art_url}\n')
    except Exception as e:
        print(f"Error processing {keyword}: {e}")



# output.txtの中身を空にする（存在しない場合は新たに作成）
with open('output.txt', 'w') as file:
    pass

# result.txtからキーワードを読み込んで処理
with open('result.txt', 'r') as file:
    for line in file:
        parts = line.strip().split(':')
        if len(parts) == 2:
            _, keyword = parts
            search_albums_and_save_results(keyword)
        else:
            print(f"Invalid line format: {line}")
