from google.cloud import vision
import io
import os

def analyze_images_in_folder(folder_path):
    client = vision.ImageAnnotatorClient()
    result_file_path = os.path.join(folder_path, '..', 'result.txt')

    # result.txtファイルを開き、内容をクリアする（'w'モードで開く）
    with open(result_file_path, 'w') as result_file:
        # imgフォルダ内のすべてのjpgファイルをループ処理
        for filename in os.listdir(folder_path):
            if filename.endswith(".jpg"):
                print(f'Processing file: {filename}')  # 処理中のファイル名を表示
                image_path = os.path.join(folder_path, filename)
                
                with io.open(image_path, 'rb') as image_file:
                    content = image_file.read()

                image = vision.Image(content=content)
                response = client.web_detection(image=image)
                annotations = response.web_detection

                # bestGuessLabelsを取得し、result.txtに書き込む
                if annotations.best_guess_labels:
                    for label in annotations.best_guess_labels:
                        result_file.write(f'{filename}: {label.label}\n')
                else:
                    # bestGuessLabelsが空の場合
                    result_file.write(f'{filename}: No best guess label found.\n')

if __name__ == '__main__':
    folder_path = 'img'
    analyze_images_in_folder(folder_path)

