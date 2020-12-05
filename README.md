# YOLO-v3をColaboratoryで使用するためのプロジェクト

[keras-yolo3](https://github.com/qqwweee/keras-yolo3)をforkしたプロジェクト。

Colaboratory環境で動作させるための修正を適宜加えている。

---

## Colaboratory上で動作させるライブラリのバージョン

[keras-yolo3](https://github.com/qqwweee/keras-yolo3) は`tensorflow 2.0`や`keras 2.2`以降に対応していないため、Colaboratory上のライブラリバージョンを変更する。

- 2020/06/27現在、以下のコマンド実行で動作に問題なし
- 2020/12/05現在、Tensorflowのバージョンは1.15.0で問題なし

```
!pip install --user -U keras==2.1.5
!pip install --user -U tensorflow_gpu==1.15.0
```

上記実行後、メニューの`ランタイム`から`ランタイムを再起動する`を実行する（再起動しないとライブラリの更新が反映されない）。再起動後、以下コマンドでライブラリのバージョンを確認すること。

```python
import tensorflow as tf
import keras
from tensorflow.python.client import device_lib

# tensorflow 1.15.0であることを確認する# %tensorflow_version 1.x
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

## プロジェクトをclone

ソースコードは `/content/` 直下に `clone` する。

本プロジェクトを`clone`する。

```
%%bash
git clone https://github.com/farcpan/keras-yolo3.git
cd keras-yolo3
git checkout develop_colaboratory
```

`clone`後、指定したディレクトリに `keras-yolo3` ディレクトリが作成されてソースコード一式を取得できたことを確認する。

---

## weightファイルの取得

以下を実行して `weight` ファイルを取得する。以下は `keras-yolo3/model_data` 直下にファイルを展開する場合。

```
%%bash
cd /content/keras-yolo3/model_data/
wget https://pjreddie.com/media/files/yolov3.weights
```

---

## cfgおよびweightファイルをh5ファイルに変換

以下を実行して `.h5` ファイルを作成する。

```
%%bash
cd /content/keras-yolo3/
python convert.py -w yolov3.cfg model_data/yolov3.weights model_data/yolo.h5
```

上記例では `model_data` 以下にファイルを出力しているが、パスやファイル名は変更してもよい。ただし、変更した場合にはソースコードの修正が必要になるので注意。

---

## annotationファイルおよびclassファイルの修正

訓練用のアノテーションファイルとクラスファイルを修正する。詳細については[元プロジェクト](https://github.com/farcpan/keras-yolo3/tree/develop_colaboratory)のREADMEを参照すること。

* アノテーションファイル: `training/annotation_sample.txt`

* クラスファイル: `training/annotation_sample.txt`

なお、画像サイズは`320x320`を想定している。アノテーションを行う画像ファイルはこのサイズで統一すること。

---

## 訓練

`keras-yolo3` 直下に移動してからスクリプトを実行する。

```
%cd /content/keras-yolo3/
```

`train.py` スクリプトを実行する。

```
python train.py  \
    /content/keras-yolo3/model_data/trafficlights_annotation.txt \
    /content/keras-yolo3/model_data/tiny_yolo_anchors.txt \
    /content/keras-yolo3/model_data/trafficlights_classes.txt \
    /content/keras-yolo3/model_data/yolo-tiny.h5 \
    output.h5 \
    --size 320 --log_dir /content/logs --batch_size_1 16 --epoch_1 10 --batch_size_2 4 --epoch_2 20
```

指定するパラメータは以下の通り。

* アノテーションファイルのパス
    * `trafficlights_annotation.txt` 

* アンカー定義ファイルのパス
    * デフォルトでは `keras-yolo3/model_data/yolo_anchors.txt` を使用する
    * `tiny`モデルの場合は `tiny-yolo_anchors.txt`

* クラス定義ファイルのパス
    * `trafficlights_classes.txt`

* モデル（ `.h5` ）ファイルパス
    * `convert.py` を実行して作成した `.h5` ファイルのパスを指定する

* 学習結果（ `.h5` ）ファイル名
    * `output.h5` 
    * `--log_dir` オプションで指定したディレクトリ以下に、上記名前のファイルを出力する

以下はオプションで指定する。

* `--size`
    * 画像サイズ（デフォルトは416）
    * 現状は縦/横に同じ値しか指定できない
    * 32の倍数を指定すること
    
* `--log_dir`
    * 学習結果を出力するディレクトリ（デフォルトは `logs/000`）
    * 最終的なモデルファイル（ `.h5` ）はここで指定したディレクトリの下に保存される

* `--batch_size_1`
    * 学習の第1ステップのミニバッチサイズ（デフォルトは32）
    * Colaboratoryで動作させる場合、16程度にしないとGPUメモリ不足になるので注意

* `--epoch_1`
    * 学習の第1ステップのエポック数（デフォルトは50）

* `--batch_size_2`
    * 学習の第2ステップのミニバッチサイズ（デフォルトは32）
    * Colaboratoryで動作させる場合、4程度にしないとGPUメモリ不足になるので注意
     
* `--epoch_2`
    * 学習の第1ステップと第2ステップのエポック数（デフォルトは100）
    *  `--epoch_1 50`, `--epoch_2 100` とした場合、第1ステップを50エポック実施した後、51〜100エポックを第2ステップで実行する

---

## 推論の実施

デフォルトの学習結果を使って推論を実行する場合。

```python
from yolo import YOLO
from predict import Prediction

# モデルをロードしてYOLOインスタンスを生成
yolo_instance = YOLO(
        model_path="./model_data/yolo.h5", 
        anchors_path="./model_data/yolo_anchors.txt",
        classes_path="./model_data/coco_classes.txt")

# 推論用のインスタンスを生成
pred = Prediction(image_path="your_image_path")
pred.detect_img(yolo_instance)    
```

---

## メモ

### CoreMLに変換する場合の注意点

`convert.py` によって生成される `.h5` ファイルは `save_weights` メソッドによって保存されているため、`coremltools`による変換がエラーになる。

以下手順でロードしてから保存し直すことで変換ができるようになる。

1. `.h5`ファイルをロードする。
    ```python
    from keras.layers import Input
    from keras.models import load_model
    from yolo3.model import yolo_body

    num_anchors = 9
    num_classes = 6    # 自作モデルの場合にはそれに合わせた数値に変更すること

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
