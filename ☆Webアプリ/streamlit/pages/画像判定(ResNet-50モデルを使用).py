import streamlit as st
import torch
from torchvision import models, transforms
from PIL import Image
import requests
from translate import Translator

# モデルをロードして評価モードに設定（ResNet-50を使用）
model = models.resnet50(pretrained=True)
model.eval()

# 画像の前処理を設定
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# ImageNetのラベルを取得
LABELS_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
labels = requests.get(LABELS_URL).json()

# Translatorの設定（Google Translatorを使用）
translator = Translator(to_lang="ja")

# Streamlitアプリのセットアップ
st.title("ResNet-50を使った画像分類")
uploaded_file = st.file_uploader("画像ファイルをアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 画像を表示
    img = Image.open(uploaded_file)
    st.image(img, caption="アップロードされた画像", use_column_width=True)

    # 画像の前処理
    img_preprocessed = preprocess(img)
    batch_img_tensor = torch.unsqueeze(img_preprocessed, 0)

    # 分類結果を表示
    st.write("分類結果")

    # モデルで画像を分類
    with torch.no_grad():
        output = model(batch_img_tensor)

    # 結果をデコードして表示
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top5_prob, top5_catid = torch.topk(probabilities, 5)

    st.write("予測結果:")
    for i in range(top5_prob.size(0)):
        label_en = labels[top5_catid[i]]
        label_ja = translator.translate(label_en)
        st.write(f"{label_ja} ({label_en}): {top5_prob[i].item() * 100:.2f}%")
