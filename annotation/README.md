# アノテーションJSONファイル変換スクリプト

VoTTを使ってエクスポートしたアノテーション情報を `keras-yolo3` で扱えるテキストファイルに変換するスクリプト。

VoTTのエクスポート形式は `Pascal VOC` であることを前提とする。また、 `keras-yolo3` 使用時には以下のディレクトリ構成で学習用画像ファイルを配置することを前提とする。 `traning` 直下に置く画像ファイルは `320x320` サイズ固定（詳細は後述）。

```
...
|
`------ train.py
|
`------ traning/
            |
            `----- ***.jpg
```

---

## スクリプト修正箇所

環境に合わせて以下のパスを適宜変更する。絶対パスまたは `convert.py` を基準とした相対パスを記述すること。ディレクトリ名の場合、終端に `/` を付加しないこと。

* VoTTがエクスポートしたJSONファイルのパス
    ```python
    # path for VoTT export json file
    path_jsons = "../annotation/*.json"
    ```

* 学習画像ファイルのパス
    ```python
    # input images directory
    image_in_dir = "../traffic-lights_20200806"
    ```

* リサイズ後の画像ファイル保存場所（ `keras-yolo3` では 320x320サイズの画像を学習に使うため、画像のリサイズ処理を行う）
    ```python
    # output images directory
    image_out_dir = "./images"
    ```

---

## スクリプト使用方法

`annotation` ディレクトリに移動してから実行する。引数は不要。スクリプトは結果を標準出力に出力するだけなので、必要であればリダイレクトしてテキストファイルに保存すること。

```
$ cd annotation
$ python convert.py > annotation.txt
```

---
