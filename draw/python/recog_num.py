import numpy as np
from sklearn import datasets, svm, metrics
from PIL import Image

#　■トレーニングデータの準備■
digits = datasets.load_digits()  # ldigitsデータ読み込み (1797, 8, 8)
# リサイズデータ(1797, 8, 8) -> (1797, 64) digits.dataでも同じ
data_train = digits.images.reshape((digits.images.shape[0], -1))
label_train = digits.target  # 正解ラベル(1797,)

# ■自作数値データの準備■
# pilで画像読み込み
pil_images = []
for i in range(1):
    # mytest_数値.pngでローカルに保存したファイル
    # 8bit(256階調) gray
    pil_image = Image.open('C:\Users\terak\Documents\プログラミング\GitHub\Flask\FlaskMathOnHeroku\flask_game\Game\mytest_0.png').convert('L')
    pil_image_resize = pil_image.resize((8, 8), Image.LANCZOS)
    pil_images.append(pil_image)
# pil画像のデータ変換
test_data = np.empty((10, 8, 8), dtype=float)
for i in range(10):
    pil_image_resize = pil_images[i].resize((8, 8), Image.LANCZOS)  # 8×8にリサイズ
    test_data[i] = np.array(pil_image_resize, dtype=float)  # ndarray型に変換
    test_data[i] = 16 - np.floor(17 * test_data[i] / 256)  # 0-255 -> 0-16＆明暗反転
# リサイズデータ(10, 8, 8) -> (10, 64)
test_data = test_data.reshape((test_data.shape[0], -1))
# テストデータの正解ラベル(10,)
label_test = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

# ■トレーニングデータで機械学習SVM(SVC)■
clf = svm.SVC(gamma=0.001, C=10.0)
clf.fit(data_train, label_train)

# ■自作数値データで識別テスト■
predict = clf.predict(test_data)
# ■結果検証
print('テストラベル（正解の数字)')
print(label_test)
print('解析結果（識別した数字）')
print(predict)
ac_score = metrics.accuracy_score(label_test, predict)
print("正解率{}%".format(ac_score*100))
