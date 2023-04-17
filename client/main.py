# -*- coding=utf-8 -*-

"""
file: send.py
socket client
"""

import socket
import os
import sys
import struct
import win32ui
import cv2

capture = cv2.VideoCapture(0)


def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('10.197.22.153', 6666))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print(s.recv(1024).decode("utf-8"))

    while 1:
        # ret, frame = capture.read()
        # cv2.imwrite("C:/Users/***/Pictures/Saved Pictures/youtemp.jpg", frame)
        # capture.release()  # 释放摄像头
        # cv2.destroyAllWindows()
        dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
        dlg.SetOFNInitialDir('C:/')  # 设置打开文件对话框中的初始显示目录
        dlg.DoModal()

        filepath = dlg.GetPathName()  # 获取选择的文件名称
        print(filepath)

        # filepath = input('please input file path: ')
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack(
                '128sl',
                os.path.basename(filepath).encode(encoding="utf-8"),
                os.stat(filepath).st_size
            )
            print('client filepath: {0}'.format(filepath))
            s.send(fhead)

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print('{0} file send over...'.format(filepath))
                    break
                s.send(data)
        print(s.recv(1024).decode("utf-8"))
        print(s.recv(1024).decode("utf-8"))
        s.close()
        break


if __name__ == '__main__':
    socket_client()