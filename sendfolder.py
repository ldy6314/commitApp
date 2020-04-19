import os
import struct
import json
import hashlib
import socket


class SendFolder:
    def __init__(self):
        self.skt = None
        self.pathlen = None
        self.totsize = 0
        self.has_send = 0

    def connect(self, address, port):
        self.skt.connect((address, port))

    def get_content(self, dirname):
        self.totsize = 0
        dirname = dirname.replace('\\', '/')
        dlst, flst = [], []
        path = "/".join(dirname.split("/")[:-1])
        pathlen = len(path)

        def tradir(dirname, dlst, flst):
            dlst.append(dirname[pathlen + 1:])
            lst = os.listdir(dirname)
            for elem in lst:
                curname = dirname + "/" + elem
                if os.path.isfile(curname):
                    flst.append(curname[pathlen + 1:])
                    self.totsize += os.stat(curname).st_size
                else:
                    tradir(curname, dlst, flst)

        tradir(dirname, dlst, flst)
        return dlst, flst

    def send_file(self, filename):
        # print(filename)
        name = filename[self.pathlen+1:]
        md_obj = hashlib.md5()
        f = open(filename, 'rb')
        data = f.read()
        md_obj.update(data)
        file_size = len(data)
        md5 = md_obj.hexdigest()
        head_info = {'name': name, 'file_size': file_size, 'md5': md5}
        head_byte = json.dumps(head_info)
        head_len = len(head_byte)
        head_len = struct.pack('q', head_len)
        self.skt.send(head_len)
        self.skt.send(head_byte.encode())
        buffersize = 4*1024*1024
        f.seek(0)
        while True:
            datapiece = f.read(buffersize)
            self.skt.send(datapiece)
            if len(datapiece) < buffersize:
                break
        f.close()
        res = self.skt.recv(1)
        if res == b'1':
            self.has_send += file_size
            self.show_progress()
            return True
        else:
            return False

    def send_all(self, dirname):
        self.send_disable()
        dlst, lst = self.get_content(dirname)
        intlen = struct.calcsize('2q')
        dlstinfo = json.dumps(dlst)
        dlst_info_len = len(dlstinfo)
        dlst_info_len_bytes = struct.pack('2q', dlst_info_len, self.totsize)
        self.skt.send(dlst_info_len_bytes)
        self.skt.send(dlstinfo.encode())
        res = self.skt.recv(1)
        if res == b'0':
            self.show_has_exist()
            return
        else:
            pass
            # print('文件夹建立成功')
        # print('-----------------------------------------------------------------')
        filenum = len(lst)
        num = struct.pack('q', filenum)
        self.skt.send(num)
        dirname = dirname.replace('\\', '/')
        path = '/'.join(dirname.split('/')[:-1])
        self.pathlen = len(path)
        for filename in lst:
            while True:
                res = self.send_file(path+'/'+filename)
                if res:
                    break
        self.send_able()
        self.complete()

    def send_disable(self):
        pass

    @staticmethod
    def show_has_exist():
        print("文件夹已经存在")

    def send_able(self):
        pass

    @staticmethod
    def complete():
        print('\r传输完成')

    def show_progress(self):
        # pct = '▇'
        pct = self.has_send/self.totsize
        print('\r|'+int(pct*20)*'▇', f'{pct:.2%}')


if __name__ == '__main__':
    sender = SendFolder()
    sender.skt = socket.socket()
    sender.connect('192.168.2.216', 8888)
    sender.send_all('E:\\Users\\Desktop\\tj')

