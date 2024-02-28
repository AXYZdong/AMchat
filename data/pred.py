from pix2text import Pix2Text, merge_line_texts

img_fp = 'img_path'
p2t = Pix2Text(device='cpu')
outs = p2t.recognize(img_fp, resized_shape=768)  # 也可以使用 `p2t(img_fp)` 获得相同的结果
print(outs)
# 如果只需要识别出的文字和Latex表示，可以使用下面行的代码合并所有结果
only_text = merge_line_texts(outs, auto_line_break=True)
print(only_text)