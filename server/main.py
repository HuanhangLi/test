# -*- coding=utf-8 -*-

"""
file: recv.py
socket service
"""
import socket
import threading
import time
import sys
import os
import struct


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('10.197.22.153', 6666))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Waiting connection...')

    while 1:
        conn, addr = s.accept()
        print(conn)
        print(addr)
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()


def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))
    # conn.settimeout(500)
    conn.send('Hi, Welcome to the server!'.encode("utf-8"))

    while 1:
        fileinfo_size = struct.calcsize('128sl')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.strip(b"\x00").decode("utf-8")
            new_filename = os.path.join('./', 'new_' + fn)
            print(new_filename, filesize)
            print('file new name is {0}, filesize if {1}'.format(new_filename, filesize))

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print('start receiving...')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)

            print(data,"\n",type(data))


            fp.close()
            print('end receive...')
        conn.send('已发送'.encode("utf-8"))
        print(conn.recv(1024).decode('utf-8'))
        conn.close()
        break


if __name__ == '__main__':
    socket_service()















# import socket
# # TCP连接
# # 创建 socket
# tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # AF_INET IPv4；AF_INET6 IPv6；SOCK_STREAM 数据流，面向连接的(TCP)； SOCK_DGRAM 数据报，无连接的(UDP)
#
# # 配置ip和端口
# host = socket.gethostname()  # 本地计算机名
# ip = socket.gethostbyname(host)   # 获取本地IP
# port = 2022  # 设置可用端口
#
# # 绑定ip和端口
# tcp_server.bind((ip, port))    # bind函数绑定端口，有两个括号是因为参数传入的是元组，其中包含IP和端口号
#
# # 监听
# tcp_server.listen(2)   # 2(int)参数为backlog,代表同时最多接收n个客户端的连接申请
#
# #  accept函数等待连接，若连接成功返回conn和address， conn为新的套接字用于连接后的消息传输，address 连接上的客户端的地址
# conn, addr = tcp_server.accept()
# print(addr, "连接上了")
#
# # 单次接收处理
# data = conn.recv(1024)   # 接收数据，1024 -- bufsize参数为接收的最大数据量
# print(data.decode())  # 以字符串编码解析
# # decode函数 解码：将接收到的bytes类型二进制数据转换为str类型
# conn.send("ok".encode())  # 发送数据给客户端
# # encode函数 编码：将str类型转为bytes类型二进制数据去传输
#
# # 循环接收处理
# '''
# while True:
#     data = conn.recv(1024)
#     if not data:
#         print("消息已读完")
#         break
#     operation = data.decode()
#     print(operation)
#     conn.send("ok".encode())
#
# '''
# tcp_server.close()  # 关闭套接字
