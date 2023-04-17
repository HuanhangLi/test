# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys  # 导入程序运行必须模块
from time import sleep

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal  # PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow
from tcpServer_ui import Ui_Form  # 导入designer工具生成的模块

import StopThreading

import socket
import threading
import os
import struct

import binascii
import time


class MyMainForm(QMainWindow, Ui_Form):
    # 信号
    tcp_signal_write_info = pyqtSignal(str, str)
    tcp_signal_ip_and_port = pyqtSignal(str, int)

    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.open_Button.clicked.connect(self.get_ip_and_port)  # 添加登录按钮信号和槽。注意display函数不加小括号()  # 按鈕點擊動作，綁定要執行的函數
        # self.close_Button.clicked.connect(self.tcp_close)  # 添加退出按钮信号和槽。调用close函数
        self.pushButton_send.clicked.connect(self.send_data)  # 发送数据

        self.close_Button.clicked.connect(self.display_image)  # test

        self.tcp_signal_write_info.connect(self.receive_display)
        self.tcp_signal_ip_and_port.connect(self.tcpServer_start)

        self.tcp_socket = None
        self.sever_th = None
        self.client_th = None
        self.client_socket_list = list()
        self.flag_tcp_opened = False

    def get_ip_and_port(self):  # 获取IP地址和端口号
        ip = self.IP_lineEdit.text()  # 利用line Edit控件对象text()函数获取界面输入
        port = self.port_lineEdit.text()
        if ip != "" and port != "":
            self.tcp_signal_ip_and_port.emit(ip, int(port))
        else:
            # self.receive_textBrowser.setText("錯誤，請檢查IP地址和端口號")
            self.label_tip.setText("錯誤，請檢查IP地址和端口號")

    def tcpServer_start(self, ip: str, port: int):  # 如果IP地址和端口号不为空，则开启服务器
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 取消主动断开连接四次握手后的TIME_WAIT状态
        self.tcp_socket.setblocking(False)  # 设定套接字为非阻塞式
        self.tcp_socket.bind((ip, port))
        self.tcp_socket.listen(5)  # 限制最大连接数
        self.sever_th = threading.Thread(target=self.tcp_server_concurrency)
        self.sever_th.start()
        self.flag_tcp_opened = True

        self.label_status.setText("已开启")
        self.label_tip.setText("正在監聽端口：" + str(port))

        print("正在監聽端口：" + str(port))

    def tcp_server_concurrency(self):  # 数据接收，只接收str
        """
        功能函数，供创建线程的方法；
        使用子线程用于监听并创建连接，使主线程可以继续运行，以免无响应
        使用非阻塞式并发用于接收客户端消息，减少系统资源浪费，使软件轻量化
        :return: None
        """
        while True:
            try:
                client_socket, client_address = self.tcp_socket.accept()
            except Exception as ret:
                sleep(0.002)
            else:
                client_socket.setblocking(False)
                # 将创建的客户端套接字存入列表,client_address为ip和端口的元组
                self.client_socket_list.append((client_socket, client_address))
                print("TCP服务端已连接IP:" + client_address[0] + "  端口：" + str(client_address[1]))
                # msg = f"TCP服务端已连接IP:{client_address[0]}端口:{client_address[1]}\n"
                # self.tcp_signal_write_msg.emit(msg)
                print(len(self.client_socket_list))

            # 轮询客户端套接字列表，接收数据
            for client, address in self.client_socket_list:
                try:
                    recv_msg = client.recv(4096)
                except Exception as ret:
                    pass
                else:   # try如果没有异常，则执行else这一块
                    # if recv_msg:
                    #     info = recv_msg.decode("utf-8")
                    #     print("来自" + address[0] + ":" + str(address[1]) + "的消息:")
                    #     print(info)
                    #
                    #     msg = f"来自IP:{address[0]}端口:{address[1]}:\n"
                    #     self.tcp_signal_write_info.emit(msg, info)
                    #     # self.tcp_signal_write_info.emit(msg)
                    #     # self.tcp_signal_write_info.emit(info)

                    if recv_msg:
                        # print(len(recv_msg))  # test
                        time_now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                        f = open('test'+time_now+'.jpg', "ab")  # filepath为你要存储的图片的全路径
                        f.write(recv_msg)  # 将图片数据写入文件，保存到文件夹
                        f.close()

                    else:
                        client.close()
                        self.client_socket_list.remove((client, address))

    def Hex2Image(self, data):

        # with open(path_txt, "r") as read_pic:
        #     payload = read_pic.read()  # 读出txt的内容形式为：b'ffd8...ffd9'，payload要求的格式为字符串ffd8...ffd9，所以要进行以下两部操作
        #     payload = payload.replace("b", '', 1)  # 去除第一个字母b
        #     payload = payload.replace("'", '')  # 去除单引号
        # payload = data.replace("b", '', 1)  # 去除第一个字母b
        print(data)

        f = open('test.jpg', "ab")  # filepath为你要存储的图片的全路径
        # pic = binascii.a2b_hex(payload.encode())
        f.write(data)
        f.close()

    def receive_display(self, msg: str, info: str):  # 顯示接收到的消息
        # ip = self.IP_lineEdit.text()  # 利用line Edit控件对象text()函数获取界面输入
        # port = self.port_lineEdit.text()
        # print(type(username))   # 類型為str
        # self.user_textBrowser.setText(msg)  # 会覆盖
        # self.user_textBrowser.setText(info)
        self.receive_textBrowser.insertPlainText(msg)
        self.receive_textBrowser.insertPlainText(info + '\n')

    def tcp_close(self):  # 關閉服務，關閉socket server，停止線程
        """
        功能函数，关闭网络连接的方法
        """
        if self.flag_tcp_opened:  # 需要根據已開啟的標誌做判斷，不然執行.close()方法會導致程序結束
            for client, address in self.client_socket_list:
                client.shutdown(socket.SHUT_RDWR)
                client.close()
            self.client_socket_list = list()  # 把已连接的客户端列表重新置为空列表
            self.tcp_socket.close()
            # msg = "已断开网络\n"
            # self.tcp_signal_write_msg.emit(msg)
            self.flag_tcp_opened = False
            print("已断开网络\n")
            self.label_tip.setText("服務已關閉")

            try:
                StopThreading.stop_thread(self.sever_th)
            except Exception as ret:
                pass
        else:
            self.label_status.setText("未开启")
            self.label_tip.setText("服務未开启")

    def display_image(self):

        # pixmap.load("picture_test/test.jpg")
        # QPixmap("picture_test/test.jpg")
        self.label_image.setPixmap(QPixmap("picture_test\\test.jpg"))
        # self.label_image.setFixedSize(256, 256)
        # self.label_image.setScaledContents(true)

    def send_data(self):
        # data = self.send_textEdit.toPlainText()

        # if len(client_socket_list) > 0 and data != '':
        #     # 轮询客户端套接字列表，接收数据
        #     for client, address in self.client_socket_list:
        #         # self.tcp_socket.send(data)
        #         client.send(data.encode())

        tcpclient, addr = self.tcp_socket.accept()
        tcpclient.send("hello".encode())

        # tcp_socket

        # if self.flag_tcp_opened and
        # st1 = input(">>")
        # # sendto(需要发送的数据,(IP地址,端口号))
        # # 发送数据,encode()将字符串转化为二进制,
        # self.tcp_socket.sendto(st1.encode("GBK"), ("10.197.22.153", 6666))


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    myWin = MyMainForm()  # 初始化
    myWin.show()  # 将窗口控件显示在屏幕上
    sys.exit(app.exec_())  # 程序运行，sys.exit方法确保程序完整退出
