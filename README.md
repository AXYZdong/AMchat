# AMchat 高等数学大模型
<div align="center">

<img src="./assets/logo.png" width="200"/>
  <div align="center">
    <b><font size="5">AMchat</font></b>
  </div>

[![license][license-image]][license-url]
[![evaluation][evaluation-image]][evaluation-url]

[🤗HuggingFace][HuggingFace_Model-url] | [![OpenXLab_Model][OpenXLab_Model-image]][OpenXLab_Model-url] | [<img src="./assets/modelscope_logo.png" width="20px" /> ModelScope][ModelScope-url] | [🤗HuggingFace-GGUF][HuggingFace_Model-GGUF-url]

[![OpenXLab_App][OpenXLab_App-image]][OpenXLab_App-url] | [🆕Update News](#-news) | [🤔Reporting Issues][Issues-url] 丨 [![bilibili][bilibili-image]][bilibili-url]

[English](./README_en-US.md) | [简体中文](./README.md) | [日本語](./README_ja-JP.md)


[license-image]: ./assets/license.svg
[evaluation-image]: ./assets/compass_support.svg
[OpenXLab_Model-image]: https://cdn-static.openxlab.org.cn/header/openxlab_models.svg
[OpenXLab_App-image]: https://cdn-static.openxlab.org.cn/app-center/openxlab_app.svg
[bilibili-image]: https://img.shields.io/badge/AMchat-bilibili-%23fb7299

[license-url]: ./LICENSE
[evaluation-url]: https://github.com/internLM/OpenCompass/
[HuggingFace_Model-url]: https://huggingface.co/axyzdong/AMchat
[HuggingFace_Model-GGUF-url]: https://huggingface.co/axyzdong/AMchat-GGUF
[OpenXLab_Model-url]: https://openxlab.org.cn/models/detail/youngdon/AMchat
[ModelScope-url]: https://www.modelscope.cn/models/yondong/AMchat/summary
[OpenXLab_App-url]: https://openxlab.org.cn/apps/detail/youngdon/AMchat
[bilibili-url]: https://www.bilibili.com/video/BV14v421i7So/
[Issues-url]: https://github.com/AXYZdong/AMchat/issues

</div>

## 📝目录

- [📖 简介](#-简介)
- [🚀 News](#-news)
- [🛠️ 使用方法](#%EF%B8%8F-使用方法)
  * [快速开始](#快速开始)
  * [重新训练](#重新训练)
    + [环境搭建](#环境搭建)
    + [XTuner微调](#xtuner微调)
    + [OpenXLab应用部署](#openxlab应用部署)
    + [LMDeploy量化](#lmdeploy量化)
    + [OpenCompass评测](#opencompass评测)
    + [LMDeploy & OpenCompass量化以及量化评测](#lmdeploy--opencompass量化以及量化评测)
- [💕 致谢](#-致谢)
- [🖊️ Citation](#%EF%B8%8F-citation)
- [开源许可证](#开源许可证)


## 📖 简介

AM (Advanced Mathematics) chat 是一个集成了数学知识和高等数学习题及其解答的大语言模型。该模型使用 Math 和高等数学习题及其解析融合的数据集，基于 InternLM2-Math-7B 模型，通过 xtuner 微调，专门设计用于解答高等数学问题。

如果你觉得这个项目对你有帮助，欢迎 ⭐ Star，让更多的人发现它！

<p align="center">
    <img src="assets/tech_route.svg" alt="route" width="100%">
</p>

## 🚀 News

[2024.08.09] 我们发布了Q8_0量化模型 [AMchat-q8_0.gguf](https://huggingface.co/axyzdong/AMchat-GGUF)。

[2024.06.23] [InternLM2-Math-Plus-20B 模型微调](plus/03-InternLM2-Math-Plus-20B%20微调.md)。

[2024.06.22] [InternLM2-Math-Plus-1.8B 模型微调](plus/01-InternLM2-Math-Plus-1.8B%20微调.md)，开源[小规模数据集](dataset/AMchat_dataset.json)。

[2024.06.21] 更新README，[InternLM2-Math-Plus-7B 模型微调](plus/02-InternLM2-Math-Plus-7B%20微调.md)。

[2024.03.24] [2024浦源大模型系列挑战赛（春季赛）Top12](https://mp.weixin.qq.com/s/8Xh232cWplgg3qdfMdD0YQ)，创新创意奖。

[2024.03.14] 模型上传至HuggingFace。

[2024.03.08] 完善了README，增加目录、技术路线。增加README_en-US.md。

[2024.02.06] 支持了Docker部署。

[2024.02.01] AMchat第一版部署上线 https://openxlab.org.cn/apps/detail/youngdon/AMchat 🚀


## 🛠️ 使用方法

### 快速开始

1. 下载模型

<details>
<summary> 从 ModelScope </summary>

参考 [模型的下载](https://www.modelscope.cn/docs/%E6%A8%A1%E5%9E%8B%E7%9A%84%E4%B8%8B%E8%BD%BD) 。

```bash
pip install modelscope
```

```python
from modelscope.hub.snapshot_download import snapshot_download
model_dir = snapshot_download('yondong/AMchat', cache_dir='./')
```

</details>


<details>
<summary> 从 OpenXLab </summary>

参考 [下载模型](https://openxlab.org.cn/docs/models/%E4%B8%8B%E8%BD%BD%E6%A8%A1%E5%9E%8B.html) 。

```bash
pip install openxlab
```

```python
from openxlab.model import download
download(model_repo='youngdon/AMchat', 
        model_name='AMchat', output='./')
```

</details>

2. 本地部署

```bash
git clone https://github.com/AXYZdong/AMchat.git
python start.py
```

3. Docker部署

```bash
docker run -t -i --rm --gpus all -p 8501:8501 guidonsdocker/amchat:latest bash start.sh
```

### 重新训练

#### 环境搭建

1. clone 本项目

```bash
git clone https://github.com/AXYZdong/AMchat.git
cd AMchat
```

2. 创建虚拟环境

```bash
conda env create -f environment.yml
conda activate AMchat
pip install xtuner
```

#### XTuner微调

1. 准备配置文件

```bash
# 列出所有内置配置
xtuner list-cfg

mkdir -p /root/math/data
mkdir /root/math/config && cd /root/math/config

xtuner copy-cfg internlm2_chat_7b_qlora_oasst1_e3 .
```

2. 模型下载

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


3. 修改配置文件

> 仓库中 `config` 文件夹下已经提供了一个微调的配置文件，可以参考 `internlm_chat_7b_qlora_oasst1_e3_copy.py`。
> 可以直接使用，注意修改  `pretrained_model_name_or_path` 和 `data_path` 的路径。


```bash
cd /root/math/config
vim internlm_chat_7b_qlora_oasst1_e3_copy.py
```

```python
# 修改模型为本地路径
- pretrained_model_name_or_path = 'internlm/internlm-chat-7b'
+ pretrained_model_name_or_path = './internlm2-math-7b'

# 修改训练数据集为本地路径
- data_path = 'timdettmers/openassistant-guanaco'
+ data_path = './data'
```

4. 开始微调

```bash
xtuner train /root/math/config/internlm2_chat_7b_qlora_oasst1_e3_copy.py
```

5. PTH 模型转换为 HuggingFace 模型

```bash
mkdir hf
export MKL_SERVICE_FORCE_INTEL=1
export MKL_THREADING_LAYER=GNU
xtuner convert pth_to_hf ./internlm2_chat_7b_qlora_oasst1_e3_copy.py \
                         ./work_dirs/internlm2_chat_7b_qlora_oasst1_e3_copy/epoch_3.pth \
                         ./hf
```

6. HuggingFace 模型合并到大语言模型
```bash
# 原始模型参数存放的位置
export NAME_OR_PATH_TO_LLM=/root/math/model/Shanghai_AI_Laboratory/internlm2-math-7b

# Hugging Face格式参数存放的位置
export NAME_OR_PATH_TO_ADAPTER=/root/math/config/hf

# 最终Merge后的参数存放的位置
mkdir /root/math/config/work_dirs/hf_merge
export SAVE_PATH=/root/math/config/work_dirs/hf_merge

# 执行参数Merge
xtuner convert merge \
    $NAME_OR_PATH_TO_LLM \
    $NAME_OR_PATH_TO_ADAPTER \
    $SAVE_PATH \
    --max-shard-size 2GB
```

7. Demo

```bash
streamlit run web_demo.py --server.address=0.0.0.0 --server.port 7860
```

#### OpenXLab应用部署

仅需要 Fork 本仓库，然后在 OpenXLab 上创建一个新的项目，将 Fork 的仓库与新建的项目关联，即可在 OpenXLab 上部署 AMchat。

<p align="center">
    <img src="assets/deploy_2.png" alt="Demo" width="100%">
</p>

- AMchat 与 InternLM2-Math-7B 在积分问题上对于同一问题的解答。 
  AMchat 回答正确，InternLM2-Math-7B 回答错误。
  
<p align="center">
    <img src="assets/test_AMchat.png" alt="Demo" width="100%">
    <img src="assets/test_InternLM2-Math-7B.png" alt="Demo" width="100%">
</p>

#### LMDeploy量化
- 首先安装LMDeploy

```shell
pip install -U lmdeploy
```

- 然后转换模型为`turbomind`格式

> --dst-path: 可以指定转换后的模型存储位置。

```shell
lmdeploy convert internlm2-chat-7b  要转化的模型地址 --dst-path 转换后的模型地址
```

- LMDeploy Chat 对话

```shell
lmdeploy chat turbomind 转换后的turbomind模型地址
```
#### OpenCompass评测
- 安装 OpenCompass

```shell
git clone https://github.com/open-compass/opencompass
cd opencompass
pip install -e .
```

- 下载解压数据集

```shell
cp /share/temp/datasets/OpenCompassData-core-20231110.zip /root/opencompass/
unzip OpenCompassData-core-20231110.zip
```

- 评测启动！

```shell
python run.py \
    --datasets math_gen \
    --hf-path 模型地址 \
    --tokenizer-path tokenizer地址 \
    --tokenizer-kwargs padding_side='left' truncation='left'     trust_remote_code=True \
    --model-kwargs device_map='auto' trust_remote_code=True \
    --max-seq-len 2048 \
    --max-out-len 16 \
    --batch-size 2  \
    --num-gpus 1 \
    --debug
```
  
#### LMDeploy & OpenCompass量化以及量化评测  

<details>
<summary><strong> W4 </strong> 量化评测 </summary>

- `W4`量化
```shell
lmdeploy lite auto_awq 要量化的模型地址 --work-dir 量化后的模型地址
```

- 转化为`TurbMind`
```shell
lmdeploy convert internlm2-chat-7b 量化后的模型地址  --model-format awq --group-size 128 --dst-path 转换后的模型地址
```

- 评测`config`编写  

```python
from mmengine.config import read_base
from opencompass.models.turbomind import TurboMindModel

with read_base():
 # choose a list of datasets   
 from .datasets.ceval.ceval_gen import ceval_datasets 
 # and output the results in a choosen format
#  from .summarizers.medium import summarizer

datasets = [*ceval_datasets]

internlm2_chat_7b = dict(
     type=TurboMindModel,
     abbr='internlm2-chat-7b-turbomind',
     path='转换后的模型地址',
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

- 评测启动！
```shell
python run.py configs/eval_turbomind.py -w 指定结果保存路径
```

</details>

<details>
<summary> <strong> KV Cache </strong> 量化评测 </summary>

- 转换为`TurbMind`
```shell
lmdeploy convert internlm2-chat-7b  模型路径 --dst-path 转换后模型路径
```
- 计算与获得量化参数
```shell
# 计算
lmdeploy lite calibrate 模型路径 --calib-dataset 'ptb' --calib-samples 128 --calib-seqlen 2048 --work-dir 参数保存路径
# 获取量化参数
lmdeploy lite kv_qparams 参数保存路径 转换后模型路径/triton_models/weights/ --num-tp 1
```
- 更改`quant_policy`改成`4`,更改上述`config`里面的路径
- 评测启动！
```shell
python run.py configs/eval_turbomind.py -w 结果保存路径
```

</details>

- 结果文件与评测数据集可在同目录文件[results](./results)中获取。


## 💕 致谢

### 项目成员

- 张友东-项目负责人 （Datawhale成员 书生·浦语实战营助教 负责模型训练，OpenXlab应用部署，数据收集，RAG内容整理，InternLM2-Math-Plus微调规划）
- 宋志学-项目负责人 （Datawhale成员 书生·浦语实战营助教 负责项目规划，RAG框架）
- 肖鸿儒-项目负责人 （Datawhale成员 同济大学 书生·浦语实战营助教 负责数据收集，数据集整理及增强，模型量化与评测，RAG推理与验证）
- 程宏 （书生·浦语实战营助教&Datawhale鲸英助教 InternLM2-Math-Plus-7B 模型微调&部署）
- 莫宝琪（玉柴工程研究院 InternLM2-Math-Plus-1.8B 模型微调）
- 陈辅元（甘肃政法大学 InternLM2-Math-Plus-20B 模型微调）
- 龚鹤扬 （中国科学技术大学统计学博士 LMDeploy 模型量化）
- 揭熔阳 （Datawhale成员 哈尔滨工业大学(威海) 数据收集 RAG内容整理）
- 彭琛 （Datawhale成员 数据收集）
- 王新茗 （数据收集）
- 刘志文 （Datawhale成员 山东女子学院 数据收集）
- 王睿玥 （Northeastern University 数据收集）
- 陈逸涵 （Datawhale成员 北京邮电大学 数据收集）
- guidons （东北大学 docker部署）
- eltociear （Board member at I-Tecnology Co., Ltd.，增加 Japanese README）

### 特别鸣谢

<div align="center">

***感谢上海人工智能实验室组织的 书生·浦语实战营 学习活动~***

***感谢 OpenXLab 对项目部署的算力支持~***

***感谢 浦语小助手 对项目的支持~***

***感谢上海人工智能实验室推出的书生·浦语大模型实战营，为我们的项目提供宝贵的技术指导和强大的算力支持！***

[**InternLM-tutorial**](https://github.com/InternLM/tutorial)、[**InternStudio**](https://studio.intern-ai.org.cn/)、[**xtuner**](https://github.com/InternLM/xtuner)、[**InternLM-Math**](https://github.com/InternLM/InternLM-Math)

<a href="https://github.com/AXYZdong/AMchat/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=AXYZdong/AMchat" />
</a>

</div>

## 🖊️ Citation

```bibtex
@misc{2024AMchat,
    title={AMchat: A large language model integrating advanced math concepts, exercises, and solutions},
    author={AMchat Contributors},
    howpublished = {\url{https://github.com/AXYZdong/AMchat}},
    year={2024}
}
```

## 开源许可证

该项目采用 [Apache License 2.0 开源许可证](https://github.com/AXYZdong/AMchat/blob/main/LICENSE) 同时，请遵守所使用的模型与数据集的许可证。
