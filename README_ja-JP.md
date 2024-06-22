# AMchat
<div align="center">

<img src="./assets/logo.png" width="200"/>
  <div align="center">
    <p><b><font size="5">AMchat</font></b></p>
  </div>

[![license][license-image]][license-url]
[![evaluation][evaluation-image]][evaluation-url]

[🤗HuggingFace][HuggingFace_Model-url] | [![OpenXLab_Model][OpenXLab_Model-image]][OpenXLab_Model-url] | [<img src="./assets/modelscope_logo.png" width="20px" /> ModelScope][ModelScope-url]

[![OpenXLab_App][OpenXLab_App-image]][OpenXLab_App-url] | [🆕更新情報](#-news) | [🤔問題報告][Issues-url] 丨 [![bilibili][bilibili-image]][bilibili-url]

[English](./README_en-US.md) | [简体中文](./README.md) | [日本語](./README_ja-JP.md)


[license-image]: ./assets/license.svg
[evaluation-image]: ./assets/compass_support.svg
[OpenXLab_Model-image]: https://cdn-static.openxlab.org.cn/header/openxlab_models.svg
[OpenXLab_App-image]: https://cdn-static.openxlab.org.cn/app-center/openxlab_app.svg
[bilibili-image]: https://img.shields.io/badge/AMchat-bilibili-%23fb7299

[license-url]: ./LICENSE
[evaluation-url]: https://github.com/internLM/OpenCompass/
[HuggingFace_Model-url]: https://huggingface.co/axyzdong/AMchat
[OpenXLab_Model-url]: https://openxlab.org.cn/models/detail/youngdon/AMchat
[ModelScope-url]: https://www.modelscope.cn/models/yondong/AMchat/summary
[OpenXLab_App-url]: https://openxlab.org.cn/apps/detail/youngdon/AMchat
[bilibili-url]: https://www.bilibili.com/video/BV14v421i7So/
[Issues-url]: https://github.com/AXYZdong/AMchat/issues

</div>

## 📝 目次

- [📖 紹介](#-紹介)
- [🚀 ニュース](#-ニュース)
- [🛠️ 使い方](#%EF%B8%8F-使い方)
  * [クイックスタート](#クイックスタート)
  * [再トレーニング](#再トレーニング)
    + [環境設定](#環境設定)
    + [XTuner微調整](#xtuner微調整)
    + [OpenXLabデプロイメント](#openxlabデプロイメント)
    + [LMDeploy量子化](#lmdeploy量子化)
    + [OpenCompass評価](#opencompass評価)
    + [LMDeploy & OpenCompass量子化と評価](#lmdeploy--opencompass量子化と評価)
- [💕 謝辞](#-謝辞)
- [🖊️ 引用](#%EF%B8%8F-引用)
- [ライセンス](#ライセンス)


## 📖 紹介

AM (Advanced Mathematics) Chatは、数学知識、高等数学の問題、およびその解決策を統合した大規模言語モデルです。このモデルは、Mathと高等数学の問題とその分析を組み合わせたデータセットを使用し、InternLM2-Math-7Bモデルに基づいており、高等数学の問題を解決するために特別に設計されたxtunerで微調整されています。

このプロジェクトが役立つと思われる場合は、⭐ スターを付けて、より多くの人に知ってもらいましょう！

<p align="center">
    <img src="assets/tech_route.svg" alt="route" width="100%">
</p>

## 🚀 ニュース

[2024.06.22] InternLM2-Math-Plus-1.8B モデルのファインチューニングを行い、小規模データセットをオープンソース化しました。

[2024.06.21] READMEを更新しました。InternLM2-Math-Plus-7B モデルのファインチューニングを行いました。

[2024.03.24] [2024 InternLM Challenge (Spring Split) | Innovation and Creativity Award](https://mp.weixin.qq.com/s/8Xh232cWplgg3qdfMdD0YQ).

[2024.03.14] モデルがHuggingFaceにアップロードされました。

[2024.03.08] READMEが強化され、目次と技術ロードマップが追加されました。また、新しいドキュメント、README_en-US.mdが作成されました。

[2024.02.06] Dockerデプロイメントがサポートされました。

[2024.02.01] AMchatの最初のバージョンが https://openxlab.org.cn/apps/detail/youngdon/AMchat でオンラインにデプロイされました 🚀



## 🛠️ 使い方

### クイックスタート

1. モデルのダウンロード

<details>
<summary>ModelScopeから</summary>

[モデルのダウンロード](https://www.modelscope.cn/docs/%E6%A8%A1%E5%9E%8B%E7%9A%84%E4%B8%8B%E8%BD%BD)を参照してください。

```bash
pip install modelscope
```

```python
from modelscope.hub.snapshot_download import snapshot_download
model_dir = snapshot_download('yondong/AMchat', cache_dir='./')
```

</details>

<details>
<summary>OpenXLabから</summary>

[モデルのダウンロード](https://openxlab.org.cn/docs/models/%E4%B8%8B%E8%BD%BD%E6%A8%A1%E5%9E%8B.html)を参照してください。

```bash
pip install openxlab
```

```python
from openxlab.model import download
download(model_repo='youngdon/AMchat', 
        model_name='AMchat', output='./')
```

</details>

2. ローカルデプロイメント

```bash
git clone https://github.com/AXYZdong/AMchat.git 
python start.py
```

3. Dockerデプロイメント

```bash
docker run -t -i --rm --gpus all -p 8501:8501 guidonsdocker/amchat:latest bash start.sh
```

### 再トレーニング

#### 環境設定

1. このプロジェクトをクローン

```bash
git clone https://github.com/AXYZdong/AMchat.git 
cd AMchat
```

2. 仮想環境を作成

```bash
conda env create -f environment.yml
conda activate AMchat
pip install xtuner
```

#### XTuner微調整

1. 設定ファイルを準備

```bash
# すべての組み込み設定をリストアップ
xtuner list-cfg

mkdir -p /root/math/data
mkdir /root/math/config && cd /root/math/config

xtuner copy-cfg internlm2_chat_7b_qlora_oasst1_e3 .
```

2. モデルのダウンロード

```bash
mkdir -p /root/math/model
```

`download.py`

```python
import torch
from modelscope import snapshot_download, AutoModel, AutoTokenizer
import os
model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm2-math-7b', cache_dir='/root/math/model')
```

3. 設定ファイルを変更

> GitHubのリポジトリでは、`config` ディレクトリの下に微調整された設定ファイルが提供されています。`internlm_chat_7b_qlora_oasst1_e3_copy.py`を参照してください。
> 直接使用できますが、`pretrained_model_name_or_path` と `data_path` のパスを変更するのをお忘れなく。

```bash
cd /root/math/config
vim internlm_chat_7b_qlora_oasst1_e3_copy.py
```

```python
# モデルをローカルパスに変更
- pretrained_model_name_or_path = 'internlm/internlm-chat-7b'
+ pretrained_model_name_or_path = './internlm2-math-7b'

# トレーニングデータセットをローカルパスに変更
- data_path = 'timdettmers/openassistant-guanaco'
+ data_path = './data'
```

4. 微調整を開始

```bash
xtuner train /root/math/config2/internlm2_chat_7b_qlora_oasst1_e3_copy.py
```

5. PTHモデルをHuggingFaceモデルに変換

```bash
xtuner convert pth_to_hf ./internlm2_chat_7b_qlora_oasst1_e3_copy.py \
                         ./work_dirs/internlm2_chat_7b_qlora_oasst1_e3_copy/epoch_3.pth \
                         ./hf
```

6. HuggingFaceモデルを大言語モデルにマージ

```bash
export MKL_SERVICE_FORCE_INTEL=1
export MKL_THREADING_LAYER='GNU'

# 元のモデルパラメータの場所
export NAME_OR_PATH_TO_LLM=/root/math/model/Shanghai_AI_Laboratory/internlm2-math-7b

# Hugging Face形式のパラメータの場所
export NAME_OR_PATH_TO_ADAPTER=/root/math/config/hf

# 最終的なマージ後のパラメータの場所
mkdir /root/math/config/work_dirs/hf_merge
export SAVE_PATH=/root/math/config/work_dirs/hf_merge

# パラメータマージを実行
xtuner convert merge \
    $NAME_OR_PATH_TO_LLM \
    $NAME_OR_PATH_TO_ADAPTER \
    $SAVE_PATH \
    --max-shard-size 2GB
```

7. デモ

```bash
streamlit run web_demo.py --server.address=0.0.0.0 --server.port 7860
```

#### OpenXLabデプロイメント

OpenXLabでAMchatをデプロイするには、このリポジトリをフォークし、OpenXLabで新しいプロジェクトを作成し、フォークしたリポジトリを新しく作成したプロジェクトに関連付けるだけです。

<p align="center">
    <img src="assets/deploy_2.png" alt="Demo" width="100%">
</p>

- AMchatとInternLM2-Math-7Bは、同じ積分問題に対して異なる回答をします。
  AMchatは正しく回答し、InternLM2-Math-7Bは誤って回答します。

<p align="center">
    <img src="assets/test_AMchat.png" alt="Demo" width="100%">
    <img src="assets/test_InternLM2-Math-7B.png" alt="Demo" width="100%">
</p>

#### LMDeploy量子化
- まず、LMDeployをインストール

```shell
pip install -U lmdeploy
```

- 次に、モデルを`turbomind`形式に変換

> --dst-path: 変換後のモデルの保存場所を指定できます。

```shell
lmdeploy convert internlm2-chat-7b  変換するモデルのアドレス --dst-path 変換後のモデルのアドレス
```

- LMDeploy Chat

```shell
lmdeploy chat turbomind 変換後のturbomindモデルのアドレス
```

#### OpenCompass評価
- OpenCompassをインストール

```shell
git clone https://github.com/open-compass/opencompass 
cd opencompass
pip install -e .
```

- データセットをダウンロードして解凍

```shell
cp /share/temp/datasets/OpenCompassData-core-20231110.zip /root/opencompass/
unzip OpenCompassData-core-20231110.zip
```

- 評価を開始！

```shell
python run.py \
    --datasets math_gen \
    --hf-path モデルのアドレス \
    --tokenizer-path トークナイザーのアドレス \
    --tokenizer-kwargs padding_side='left' truncation='left' trust_remote_code=True \
    --model-kwargs device_map='auto' trust_remote_code=True \
    --max-seq-len 2048 \
    --max-out-len 16 \
    --batch-size 2  \
    --num-gpus 1 \
    --debug
```

#### LMDeploy & OpenCompass量子化と評価

<details>
<summary><strong> W4 </strong> 量子化評価 </summary>

- `W4`量子化
```shell
lmdeploy lite auto_awq 量子化するモデルのアドレス --work-dir 量子化後のモデルのアドレス
```

- `TurbMind`に変換
```shell
lmdeploy convert internlm2-chat-7b 量子化後のモデルのアドレス  --model-format awq --group-size 128 --dst-path 変換後のモデルのアドレス
```

- 評価`config`の作成
```python
from mmengine.config import read_base
from opencompass.models.turbomind import TurboMindModel

with read_base():
 # データセットのリストを選択   
 from .datasets.ceval.ceval_gen import ceval_datasets 
 # 結果を選択した形式で出力
#  from .summarizers.medium import summarizer

datasets = [*ceval_datasets]

internlm2_chat_7b = dict(
     type=TurboMindModel,
     abbr='internlm2-chat-7b-turbomind',
     path='変換後のモデルのアドレス',
     engine_config=dict(session_len=512,
         max_batch_size=2,
         rope_scaling_factor=1.0),
     gen_config=dict(top_k=1,
         top_p=0.8,
         temperature=1.0,
         max_new_tokens=100),
     max_out_len=100,
     max_seq_len=512,
     batch_size=2,
     concurrency=1,
     #  meta_template=internlm_meta_template,
     run_cfg=dict(num_gpus=1, num_procs=1),
)
models = [internlm2_chat_7b]

```

- 評価を開始！
```shell
python run.py configs/eval_turbomind.py -w 結果を保存するパスを指定
```

</details>

<details>
<summary><strong> KV Cache </strong> 量子化評価</summary>

- `TurbMind`に変換
```shell
lmdeploy convert internlm2-chat-7b モデルのパス --dst-path 変換後のモデルのパス
```

- 量子化パラメータを計算して取得
```shell
# 計算
lmdeploy lite calibrate モデルのパス --calib-dataset 'ptb' --calib-samples 128 --calib-seqlen 2048 --work-dir パラメータを保存するパス
# 量子化パラメータを取得
lmdeploy lite kv_qparams パラメータを保存するパス 変換後のモデルのパス/triton_models/weights/ --num-tp 1
```

- `quant_policy`を`4`に変更し、上記の`config`内のパスを変更
- 評価を開始！
```shell
python run.py configs/eval_turbomind.py -w 結果を保存するパス
```

</details>

- 結果ファイルと評価データセットは、同じディレクトリの[results](./results)で入手できます。

## 💕 謝辞

[**InternLM-tutorial**](https://github.com/InternLM/tutorial)

[**InternStudio**](https://studio.intern-ai.org.cn/)

[**xtuner**](https://github.com/InternLM/xtuner)

[**InternLM-Math**](https://github.com/InternLM/InternLM-Math)


<a href="https://github.com/AXYZdong/AMchat/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=AXYZdong/AMchat" />
</a>

## 🖊️ 引用

```bibtex
@misc{2024AMchat,
    title={AMchat: 高等数学の概念、演習問題、および解決策を統合した大規模言語モデル},
    author={AMchat Contributors},
    howpublished = {\url{https://github.com/AXYZdong/AMchat}},
    year={2024}
}
```

## ライセンス
このプロジェクトは、[Apache License 2.0](https://github.com/InternLM/xtuner/blob/main/LICENSE)の下でリリースされています。また、使用されるモデルとデータセットのライセンスにも従ってください。
