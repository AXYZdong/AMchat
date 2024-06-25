# 03-InternLM2-Math-Plus-20B 微调

## 环境搭建

请参考[README.md](../README.md), 本教程重点为如何微调新模型[InternLM2-Math-Plus-7B](https://modelscope.cn/models/Shanghai_AI_Laboratory/internlm2-math-plus-7b).

## XTuner微调

1. 准备配置文件

```bash
# 列出所有内置配置, 复制internlm2_chat_7b_qlora_oasst1_e3为internlm_chat_7b_qlora_oasst1_e3_copy.py
xtuner list-cfg
xtuner copy-cfg internlm2_chat_7b_qlora_oasst1_e3 .
mv internlm2_chat_7b_qlora_oasst1_e3_copy.py  internlm2_chat_7b_qlora_math_e3.py
```

2. 模型下载

用InternStudio 平台默认提供的

```
cp -r /root/share/model_repos/internlm2-math-plus-20b /root/model/Shanghai_AI_Laboratory
```

`download.py`

```python
import torch
from modelscope import snapshot_download, AutoModel, AutoTokenizer
import os
model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm2-math-plus-20b', cache_dir='/root/model')
```

然后运行`python download.py`即可下载模型权重到指定`cache_dir`


3. 修改配置文件

```python
# 修改模型为本地路径
- pretrained_model_name_or_path = 'internlm/internlm-chat-7b'
+ pretrained_model_name_or_path = '/root/model/Shanghai_AI_Laboratory/internlm2-math-plus-20b'

# 修改训练数据集为本地路径
- data_path = 'timdettmers/openassistant-guanaco'
+ data_path = 'root/math/data/math_xtuner.json'
```

4. 开始微调

```bash
# 采用deepspeed_zero2节省更多显存, 降低微调硬件需求
xtuner train internlm2_chat_7b_qlora_oasst1_e3_copy.py  --deepspeed deepspeed_zero2
```

5. 模型转换：将训练后的pth格式参数转Hugging Face格式


```bash
# 创建用于存放Hugging Face格式参数的hf文件夹
mkdir /root/math/config/work_dirs/hf
export MKL_SERVICE_FORCE_INTEL=1
# 配置文件存放的位置
export CONFIG_NAME_OR_PATH=/root/math/config/internlm2_chat_7b_qlora_math_e3.py 
# 模型训练后得到的pth格式参数存放的位置
export PTH=/root/math/config/work_dirs/internlm2_chat_7b_qlora_math_e3/epoch_3.pth
# pth文件转换为Hugging Face格式后参数存放的位置
export SAVE_PATH=/root/math/config/work_dirs/hf
# 执行参数转换
xtuner convert pth_to_hf $CONFIG_NAME_OR_PATH $PTH $SAVE_PATH
```

6. 模型合并：将微调后的模型参数合并到基座模型中

```bash
xtuner convert merge /root/model/Shanghai_AI_Laboratory/internlm2-math-plus-20b   /root/math/config/work_dirs/hf   /root/math/config/work_dirs/hf_merge  --max-shard-size 2GB
```

7. Demo

可以自行对比微调后的模型和微调之前的效果差

```bash
streamlit run /root/cmed2/code/InternLM/chat/web_demo_finetune.py --server.address 127.0.0.1 --server.port 6006
```

8. 微调后的模型下载地址

- openxlab: [AMchat-plus-20b](https://openxlab.org.cn/models/detail/element/AMChat_internlm2-math-plus-20b_Yuan/tree/main)
- modelscope: [AMchat-plus-20b](https://www.modelscope.cn/models/CFYuan/AMChat_internlm2-math-plus-20b_Yuan/files)

