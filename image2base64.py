import base64

# 读取图标文件（PNG 或 ICO）
with open(r"C:\Users\17728\Pictures\Saved Pictures\高木.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

# 打印 Base64 编码
print(encoded_string)