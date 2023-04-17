import binascii


# 图片转为16进制
def Image2Hex(path):
    with open(path, 'rb') as f:
        content = f.read()
        print(content)
    print(binascii.hexlify(content))
    print(type(binascii.hexlify(content)))

    with open("aaa.txt", 'w') as f:   # 写入txt的内容形式为：b'ffd8...ffd9'
        f.write(str(binascii.hexlify(content)))


# 16进制转为图片
def Hex2Image(path_txt, path_pic):
    # payload为十六进制字符串，如：“ffd8ffe111e0457869...ffd9”；经过如下代码转换，可将pic存储为图片形式并可以正常打开

    with open(path_txt, "r") as read_pic:
        payload = read_pic.read()   # 读出txt的内容形式为：b'ffd8...ffd9'，payload要求的格式为字符串ffd8...ffd9，所以要进行以下两部操作
        payload = payload.replace("b", '', 1)  # 去除第一个字母b
        payload = payload.replace("'", '')  # 去除单引号
    print(payload)
    f = open(path_pic, "ab")  # filepath为你要存储的图片的全路径
    pic = binascii.a2b_hex(payload.encode())
    f.write(pic)
    f.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Image2Hex('test.jpg')
    # Hex2Image("aaa.txt", "1.jpg")

