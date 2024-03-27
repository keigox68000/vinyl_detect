from google.cloud import vision
import io
import os
from google.oauth2 import service_account

# 現在のスクリプトのディレクトリパスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
# サービスアカウントキーファイルへのパスを構築
service_account_path = os.path.join(current_dir, 'vinyl-detect-key.json')
# サービスアカウントキーファイルを使用して認証情報を作成
credentials = service_account.Credentials.from_service_account_file(service_account_path)
# 認証情報を使用してVision APIクライアントを初期化
client = vision.ImageAnnotatorClient(credentials=credentials)

def analyze_images_in_folder(folder_path):
    # client = vision.ImageAnnotatorClient() # この行を削除
    result_file_path = os.path.join(folder_path, '..', 'result.txt')

    with open(result_file_path, 'w') as result_file:
        for filename in os.listdir(folder_path):
            if filename.endswith(".jpg"):
                print(f'Processing file: {filename}')
                image_path = os.path.join(folder_path, filename)
                
                with io.open(image_path, 'rb') as image_file:
                    content = image_file.read()

                image = vision.Image(content=content)
                response = client.web_detection(image=image)
                annotations = response.web_detection

                if annotations.best_guess_labels:
                    for label in annotations.best_guess_labels:
                        result_file.write(f'{filename}: {label.label}\n')
                else:
                    result_file.write(f'{filename}: No best guess label found.\n')

if __name__ == '__main__':
    folder_path = 'img'
    analyze_images_in_folder(folder_path)
