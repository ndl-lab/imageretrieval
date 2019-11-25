# imageretrieval
画像検索インデックス作成プログラム(image search indexing program)

## 画像からの特徴抽出(feature extraction from images)
デフォルトではdatasetディレクトリ以下にあるディレクトリ別に特徴抽出します。

抽出された特徴量はディレクトリ名ごとにpickleで保存されます。

例：

dataset/1

の中にPASCAL VOC形式のレイアウトxmlと、同名の画像ファイルがあるとき、

があるとき、1.pklに特徴量が保存されます。
形式はディクショナリで、{"iiifuri":uri,"vec":(1280次元の特徴量)}

"iiifuri"は、次世代デジタルライブラリーがNDLデジタルコレクションのIIIF Image apiを使用しているため必要なURIです。

必要に応じて持たせる情報をカスタマイズしてください。

```python3 extract_features_mobilenetv2.py```
## インデックス作成
Yahoo!社の[NGTD](https://github.com/yahoojapan/ngtd)を導入したDockerコンテナを用意し、

run.shを書き換えて、適当なポート番号でNGTDを起動します。

ポート番号を合わせて、インデックスに投入したいpickleファイルを指定したうえで、

buildindex.pyを実行するとインデックスが作成されます。

検索クエリの作り方は[次世代デジタルライブラリーのバックエンドソースコード](https://github.com/ndl-lab/tugidigi-web/blob/master/back/src/main/java/jp/go/ndl/lab/dl/back/service/VectorSearchService.java)、やNGTDのリポジトリをご参照ください。



