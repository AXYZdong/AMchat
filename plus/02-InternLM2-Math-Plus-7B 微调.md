# 02-InternLM2-Math-Plus-7B 微调

## 环境搭建

请参考README.md, 本教程重点为如何微调新模型InternLM2-Math-Plus-7B.

## XTuner微调

1. 准备配置文件

```bash
# 列出所有内置配置, 复制internlm2_chat_7b_qlora_oasst1_e3为internlm_chat_7b_qlora_oasst1_e3_copy.py
xtuner list-cfg
xtuner copy-cfg internlm2_chat_7b_qlora_oasst1_e3 .
```

2. 模型下载

`download.py`

```python
import torch
from modelscope import snapshot_download, AutoModel, AutoTokenizer
import os
model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm2-math-plus-7b', cache_dir='/group_share/models')
```

然后运行`python download.py`即可下载模型权重到指定`cache_dir`


3. 修改配置文件

```bash
vim internlm_chat_7b_qlora_oasst1_e3_copy.py
```

```python
# 修改模型为本地路径
- pretrained_model_name_or_path = 'internlm/internlm-chat-7b'
+ pretrained_model_name_or_path = '/root/group_share/models/Shanghai_AI_Laboratory/internlm2-math-plus-7b'

# 修改训练数据集为本地路径
- data_path = 'timdettmers/openassistant-guanaco'
+ data_path = './data/math_xtuner.json'
```

4. 开始微调

```bash
# 采用deepspeed_zero2节省更多显存, 降低微调硬件需求
xtuner train /root/math/config2/internlm2_chat_7b_qlora_oasst1_e3_copy.py  --deepspeed deepspeed_zero2
```

5. PTH 模型转换为 HuggingFace 模型


```bash
mkdir /group_share/hf_7b
xtuner convert pth_to_hf ./internlm2_chat_7b_qlora_oasst1_e3_copy.py \
                         ./work_dirs/internlm2_chat_7b_qlora_oasst1_e3_copy/epoch_3.pth \
                         ./hf_7b
```

6. HuggingFace 模型合并到大语言模型
```bash
export MKL_SERVICE_FORCE_INTEL=1
export MKL_THREADING_LAYER='GNU'

# 原始模型参数存放的位置
export NAME_OR_PATH_TO_LLM=/root/group_share/models/Shanghai_AI_Laboratory/internlm2-math-plus-7b

# Hugging Face格式参数存放的位置
export NAME_OR_PATH_TO_ADAPTER=/group_share/hf_7b

# 最终Merge后的参数存放的位置
mkdir /group_share/hf_7b_merge
export SAVE_PATH=/group_share/hf_7b_merge

# 执行参数Merge
xtuner convert merge \
    $NAME_OR_PATH_TO_LLM \
    $NAME_OR_PATH_TO_ADAPTER \
    $SAVE_PATH \
    --max-shard-size 2GB
```

7. Demo

```bash
streamlit run web_demo_7b_plus.py --server.address=0.0.0.0 --server.port 7860
```

8. 微调后的模型下载地址
- openxlab: https://openxlab.org.cn/models/detail/chg0901/AMChat_internlm2-math-plus-7b_Hong/tree/main
- modelscope: https://modelscope.cn/models/chg0901/AMChat_internlm2-math-plus-7b_Hong/files
