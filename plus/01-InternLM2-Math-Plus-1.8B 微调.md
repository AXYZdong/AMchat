# 01-InternLM2-Math-Plus-1.8B 微调

## **环境搭建**

请参考[README.md](https://github.com/RoundCoral/AMChat_internlm2-math-plus-1.8b/blob/main/README.md), 本教程重点为如何微调新模型[InternLM2-Math-Plus-1.8B](https://modelscope.cn/models/Shanghai_AI_Laboratory/internlm2-math-plus-1_8b/summary).

## **XTuner微调**

1.准备配置文件

```SQL
# 拉取github上的AMchat代码模型
git clone https://github.com/AXYZdong/AMchat.git
# 将配置文件复制到自己的模型目录下
cp /root/Amath_xtuner/AMchat/config/internlm2_chat_7b_qlora_oasst1_e3_copy.py  /root/Amath_xtuner/config/
```

2.模型下载

创建python文件`/root/Amath_xtuner/data/data_download.py`

```SQL
import os
os.environ["HF_HOME"]='/group_share/hf'
os.environ["MODELSCOPE_CACHE"]='/group_share/modelscope_hub'
os.environ["MODELSCOPE_MODULES_CACHE"]='/group_share/modelscope_modules'

#模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm2-math-plus-1_8b',
                               cache_dir='/group_share/models')
```

将模型下载到指定的`cache_dir`目录下

3.修改配置文件

修改`/root/Amath_xtuner/config/internlm2_chat_7b_qlora_oasst1_e3_copy.py`配置文件：

```SQL
# 修改模型为本地路径
- pretrained_model_name_or_path = 'internlm/internlm-chat-7b'
+ pretrained_model_name_or_path = '/root/Amath_xtuner/model/internlm2-math-plus-1_8b'

# 修改训练数据集为本地路径
- data_path = 'timdettmers/openassistant-guanaco'
+ data_path = '/root/Amath_xtuner/data/math_xtuner.json'
```

4.开始微调

```Python
# 采用deepspeed_zero2节省更多显存, 降低微调硬件需求
xtuner train /root/Amath_xtuner/config/internlm2_chat_7b_qlora_oasst1_e3_copy.py --work-dir /root/Amath_xtuner/train_deepspeed --deepspeed deepspeed_zero2
```

5.`PTH` 模型转换为 `HuggingFace` 模型

```Python
xtuner convert pth_to_hf /root/Amath_xtuner/train_deepspeed/internlm2_chat_7b_qlora_oasst1_e3_copy.py /root/Amath_xtuner/train_deepspeed/epoch_3.pth /root/Amath_xtuner/huggingface
```

6.`HuggingFace` 模型合并到大语言模型

```Python
export MKL_SERVICE_FORCE_INTEL=1
export MKL_THREADING_LAYER='GNU'# 原始模型参数存放的位置export 
xtuner convert merge /root/Amath_xtuner/model/internlm2-math-plus-1_8b /root/Amath_xtuner/huggingface /root/Amath_xtuner/final_model
```

7.运行Demo

```Python
streamlit run /root/Amath_xtuner/web_demo/InternLM/chat/web_demo.py --server.address 127.0.0.1 --server.port 6006
```

8.微调后的模型下载地址

- openxlab: [高等数学解题小助手](https://openxlab.org.cn/models/detail/Round_coral/AMChat_internlm2-math-plus-1.8b)
- modelscope: [高等数学解题小助手](https://www.modelscope.cn/models/Roundcoral/AMChat_internlm2-math-plus-1.8b)