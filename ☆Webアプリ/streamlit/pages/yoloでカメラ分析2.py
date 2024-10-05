import cv2
import os

# 画像を保存するディレクトリ
save_dir = 'captured_images'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# カメラキャプチャの設定
cap = cv2.VideoCapture(0)

# 画像保存用のリスト
image_paths = []

# 撮影と保存
while True:
    ret, frame = cap.read()

    # 撮影した画像を表示
    cv2.imshow('frame', frame)

    # 's'キーを押すと画像を保存
    if cv2.waitKey(1) == ord('s'):
        filename = f'image_{len(image_paths)}.jpg'
        filepath = os.path.join(save_dir, filename)
        cv2.imwrite(filepath, frame)
        image_paths.append(filepath)
        print(f"画像を保存しました: {filepath}")

    # 'q'キーを押すと終了
    if cv2.waitKey(1) == ord('q'):
        break

# カメラを解放
cap.release()
cv2.destroyAllWindows()

# 保存した画像をまとめて分析 (例: 各画像の平均色を計算)
for image_path in image_paths:
    img = cv2.imread(image_path)
    avg_color_per_row = np.average(img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    print(f"{image_path}の平均色は: {avg_color}")
