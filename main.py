# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys   # 导入程序运行必须模块
from time import sleep

from PyQt5.QtCore import pyqtSignal   # PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow
from tcpServer import Ui_Form  # 导入designer工具生成的模块

import socket
import threading
import os
import struct


class MyMainForm(QMainWindow, Ui_Form):
    tcp_signal_write_info = pyqtSignal(str, str)
    tcp_signal_ip_and_port = pyqtSignal(str, int)

    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.open_Button.clicked.connect(self.get_ip_and_port)  # 添加登录按钮信号和槽。注意display函数不加小括号()  # 按鈕點擊動作，綁定要執行的函數
        self.close_Button.clicked.connect(self.close)  # 添加退出按钮信号和槽。调用close函数

        self.tcp_signal_write_info.connect(self.receive_display)
        # self.tcp_signal_ip_and_port.connect(self.tcpServer_start)

        self.tcp_socket = None
        self.sever_th = None
        self.client_th = None
        self.client_socket_list = list()

    def get_ip_and_port(self):
        ip = self.IP_lineEdit.text()  # 利用line Edit控件对象text()函数获取界面输入
        port = self.port_lineEdit.text()
        if ip != "" and port != "":
            self.tcp_signal_ip_and_port.emit(ip, int(port))
        # else:
        #     self.receive_textBrowser.setText("錯誤，請檢查IP地址和端口號")
            # pass   # 這裡很重要，如果沒有else這句，點擊按鈕後會自動退出程序

    def tcpServer_start(self, ip: str, port: int):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 取消主动断开连接四次握手后的TIME_WAIT状态
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设定套接字为非阻塞式
        self.tcp_socket.setblocking(False)
        self.tcp_socket.bind((ip, port))
        self.tcp_socket.listen(5)  # 限制最大连接数
        self.sever_th = threading.Thread(target=self.tcp_server_concurrency)
        self.sever_th.start()
        # print("正在監聽端口：", 6666)

    def tcp_server_concurrency(self):
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
            # 轮询客户端套接字列表，接收数据
            for client, address in self.client_socket_list:
                try:
                    recv_msg = client.recv(4096)
                except Exception as ret:
                    pass
                else:
                    if recv_msg:
                        info = recv_msg.decode("utf-8")
                        print("来自" + address[0] + ":" + str(address[1]) + "的消息:")
                        print(info)

                        msg = f"来自IP:{address[0]}端口:{address[1]}:\n"
                        self.tcp_signal_write_info.emit(msg, info)
                        # self.tcp_signal_write_info.emit(msg)
                        # self.tcp_signal_write_info.emit(info)

                    else:
                        client.close()
                        self.client_socket_list.remove((client, address))

    def receive_display(self, msg: str, info: str):  # 顯示接收到的消息
        # ip = self.IP_lineEdit.text()  # 利用line Edit控件对象text()函数获取界面输入
        # port = self.port_lineEdit.text()
        # print(type(username))   # 類型為str
        # self.user_textBrowser.setText(msg)  # 会覆盖
        # self.user_textBrowser.setText(info)
        self.receive_textBrowser.insertPlainText(msg)
        self.receive_textBrowser.insertPlainText(info + '\n')


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    myWin = MyMainForm()  # 初始化
    myWin.show()  # 将窗口控件显示在屏幕上
    sys.exit(app.exec_())  # 程序运行，sys.exit方法确保程序完整退出
