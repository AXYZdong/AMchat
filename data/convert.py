from pdf2image import convert_from_path

def pdf_to_images(pdf_path, output_folder):
    # 将 PDF 转换为图片
    images = convert_from_path(pdf_path, dpi=300)
    
    # 保存每一页图片
    for i, image in enumerate(images):
        image_path = f"{output_folder}/page_{i+1}.jpg"  # 图片保存路径，可以根据需要修改格式
        image.save(image_path, "PNG")  # 将图片保存为 JPEG 格式

if __name__ == "__main__":
    pdf_path = "demo.pdf"  # 输入 PDF 文件路径
    output_folder = "./output"  # 输出图片文件夹路径
    
    # 调用函数进行转换
    pdf_to_images(pdf_path, output_folder)
