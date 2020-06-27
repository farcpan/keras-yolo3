# YOLO-v3をColaboratoryで使用するためのプロジェクト

[keras-yolo3](https://github.com/qqwweee/keras-yolo3)をforkしたプロジェクト。

Colaboratory環境で動作させるための修正を適宜咥えている。

---

## Colaboratory上で動作させるライブラリのバージョン

[keras-yolo3](https://github.com/qqwweee/keras-yolo3) は`tensorflow 2.0`や`keras 2.2`以降に対応していないため、Colaboratory上のライブラリバージョンを変更する。2020/06/27現在、以下のコマンド実行で動作に問題なし。

```
!pip install --user -U keras==2.1.5
!pip install --user -U tensorflow_gpu==1.14.0
```

上記実行後、メニューの`ランタイム`から`ランタイムを再起動する`を実行する（再起動しないとライブラリの更新が反映されない）。再起動後、以下コマンドでライブラリのバージョンを確認すること。

```python
import tensorflow as tf
import keras
from tensorflow.python.client import device_lib

# tensorflow 1.14.0であることを確認する# %tensorflow_version 1.x
print(tf.__version__)

# keras 2.1.5であることを確認する
print(keras.__version__)
```

---

## Google Driveをマウント

ソースコードや学習データ、モデル等はGoolge Drive上に保存しておいた方が便利なため、ColaboratoryにGoogle Driveをマウントする。以下を実行後、Driveへのアクセスを承認する（画面の指示通りに実行すればOK）。

```python
from google.colab import drive
drive.mount('/content/drive')
```

---

## ディレクトリの移動

Google Driveをマウント後、ソースコードを展開したいディレクトリに移動する。`/content/drive/'My Drive'/` がGoogle Driveのルートディレクトリに該当する。

```
%cd /content/drive/'My Drive'/yourworkspace
```

---

## プロジェクトをclone

本プロジェクトを`clone`する。

```
!git clone https://github.com/farcpan/keras-yolo3.git
```

`clone`後、指定したディレクトリに `keras-yolo3` ディレクトリが作成されてソースコード一式を取得できたことを確認する。

---

## weightファイルの取得

以下を実行して `weight` ファイルを取得する。 `keras-yolo3` 直下でない場所に置いても良い。

```
!wget https://pjreddie.com/media/files/yolov3.weights
```

---

## cfgおよびweightファイルをh5ファイルに変換

以下を実行して `.h5` ファイルを作成する。

```
!python convert.py -w yolov3.cfg yolov3.weights model_data/yolo.h5
```

上記例では `model_data` 以下にファイルを出力しているが、パスやファイル名は変更してもよい。ただし、変更した場合にはソースコードの修正が必要になるので注意。

---

## annotationファイルおよびclassファイルの修正

訓練用のアノテーションファイルとクラスファイルを修正する。詳細については[元プロジェクト](https://github.com/farcpan/keras-yolo3/tree/develop_colaboratory)のREADMEを参照すること。

* アノテーションファイル: `training/annotation_sample.txt`

* クラスファイル: `training/annotation_sample.txt`

---

## 訓練

上記のファイル名やファイル配置ディレクトリを変更していない場合は、このまま `train.py` スクリプトを実行する。

```
!python train.py
```

変更した場合は以下の箇所を修正してから上記を実行。

* アノテーションファイルのパス: `train.py` 内 `_main` メソッドの以下箇所

    ```python
    # annotation data text file
    annotation_path = 'training/annotation_sample.txt'
    ```

* クラスパス: `train.py` 内 `_main` メソッドの以下箇所

    ```python
    # class definition
    classes_path = 'training/classes_sample.txt'
    ```

* 画像サイズ: `train.py` 内 `_main` メソッドの以下箇所

    ```python
    input_shape = (320, 320) # multiple of 32, hw
    ```

* `.h5` ファイルパス: `train.py` 内 `_main` メソッドの以下箇所

    ```python
    model = create_model(input_shape, anchors, num_classes, freeze_body=2, weights_path='model_data/yolo.h5')
    ```

---

## メモ

### CoreMLに変換する場合の注意点

`convert.py` によって生成される `.h5` ファイルは `save_weights` メソッドによって保存されているため、`coremltools`による変換がエラーになる。


以下手順でロードしてから保存し直すことで変換ができるようになる。

1. `.h5`ファイルをロードする。
    ```python
    from yolo3.model import yolo_body
    from keras.models import load_model

    num_anchors = 9
    num_classes = 80    # 自作モデルの場合にはそれに合わせた数値に変更すること

    yolo_model = yolo_body(Input(shape=(None,None,3)), num_anchors//3, num_classes)
    yolo_model.load_weights("./model_data/yolo.h5") # make sure model, anchors and classes match

    print(yolo_model.summary())
    ```

1. ロードしたモデルを保存する。
    ```python
    yolo_model.save("./model_data/resaved_yolo.h5")
    ```

* 参考: [YOLOv3-CoreML](https://github.com/Ma-Dan/YOLOv3-CoreML)

---
