#!/usr/bin/python
# -*-coding:utf-8 -*-

import paramiko
import os
import time


def get_all_files_in_local_dir(local_dir):
    """递归获取当前目录下所有文件目录"""
    all_files = []
    # 获取当前指定目录下的所有目录及文件，包含属性值
    files = os.listdir(local_dir)
    for x in files:
        # local_dir目录中每一个文件或目录的完整路径
        filename = os.path.join(local_dir, x)
        # 如果是目录，则递归处理该目录
        if os.path.isdir(filename):
            all_files.extend(get_all_files_in_local_dir(filename))
        else:
            all_files.append(filename)
    return all_files


class Dossh:
    def __init__(self, ip, port, uname, passwd):
        self.ip = ip
        self.port = port
        self.uname = uname
        self.passwd = passwd
        self.sshclt = paramiko.SSHClient()
        self.sshclt.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclt.connect(hostname=self.ip, port=self.port, username=self.uname, password=self.passwd,
                            allow_agent=False, look_for_keys=False)
        self.t = paramiko.Transport((self.ip, self.port))
        self.t.connect(username=self.uname, password=self.passwd)
        self.sftp = paramiko.SFTPClient.from_transport(self.t)

    def getssh(self):
        return self.sshclt

    def close_ssh(self):
        self.sshclt.close()
        self.sftp.close()

    def uploadfile_path(self, local_path, remote_path):
        """
        :param local_path:待上传文件夹路径
        :param remote_path:远程路径
        :return:
        """
        # 待上传目录名
        local_pathname = os.path.split(local_path)[-1]
        # 上传远程后的目录名
        real_remote_Path = remote_path + '/' + local_pathname
        ##判断是否存在，不存在则创建
        try:
            self.sftp.stat(remote_path)
        except Exception as e:
            self.sshclt.exec_command("mkdir -p %s" % remote_path)
        self.sshclt.exec_command("mkdir -p %s" % real_remote_Path)
        # 获取本地文件夹下所有文件路径
        all_files = get_all_files_in_local_dir(local_path)
        # 依次判断远程路径是否存在，不存在则创建，然后上传文件
        for file_path in all_files:
            # 统一win和linux 路径分隔符
            file_path = file_path.replace("\\", "/")
            ##用本地根文件夹名分隔本地文件路径，取得相对的文件路径
            off_path_name = file_path.split(local_pathname)[-1]
            # 取得本地存在的嵌套文件夹层级
            abs_path = os.path.split(off_path_name)[0]
            # 生产期望的远程文件夹路径
            reward_remote_path = real_remote_Path + abs_path
            # 判断期望的远程目录是否存在，不存在则创建
            try:
                self.sftp.stat(reward_remote_path)
            except Exception as e:
                self.sshclt.exec_command("mkdir -p %s" % reward_remote_path)
            # 待上传的文件名
            abs_file = os.path.split(file_path)[1]
            # 上传后的远端路径，文件名不变
            to_remote = reward_remote_path + '/' + abs_file
            time.sleep(0.1)
            self.sftp.put(file_path, to_remote)
            print(file_path, to_remote)


if __name__ == "__main__":
    ma_ip='192.168.80.149'
    ma_port=22
    ma_user='root'
    ma_passwd='123456'
    sshclent = Dossh(ma_ip,int(ma_port),ma_user,ma_passwd)
    sshclent.uploadfile_path("../reports",'/home')
    
