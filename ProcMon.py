import sys
import os
import subprocess
import argparse
import threading
import time
import shutil
import hashlib
import zlib

g_exitFlag = 0
g_IgnoreFileList = []
class ProcMonThread (threading.Thread):
    def __init__(self, threadID, name, directory):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.directory = directory
    def run(self):
        print("start thread: " + self.name)
        dowork(self.name, self.directory)
        print("thread: " + self.name + " exit")
        
def dowork(threadName, directory):
    while True:
        if g_exitFlag:
            threadName.exit()
        getDirectoryFileHash(directory)
        print("%s: %s" % (threadName, time.ctime(time.time())))

def parse_cmd_line():
    parser = argparse.ArgumentParser(description='parse input command')
    parser.add_argument('-n', type = int, help = 'run proc num')
    parser.add_argument('-c', help = 'run command line')
    parser.add_argument('-d', help = 'command line for directory')
    parser.print_help()
def getFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(4096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()
def getFileSha(filename, algorithm):
    if not os.path.isfile(filename):
        return
    if algorithm in ('SHA1', 'sha1'):
        myhash = hashlib.sha1()
    elif algorithm in ('SHA224', 'sha224'):
        myhash = hashlib.sha224()
    elif algorithm in ('SHA256', 'sha256'):
        myhash = hashlib.sha256()
    elif algorithm in ('SHA384', 'sha384'):
        myhash = hashlib.sha384()
    elif algorithm in ('SHA512', 'sha512'):
        myhash = hashlib.sha512()
    f = file(filename,'rb')
    while True:
        b = f.read(4096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()
def getFileCrc32(filename):
    if not os.path.isfile(filename):
        return
    if os.path.islink(filename):
        return
    f = file(filename,'rb')
    if not f:
        return
    return zlib.crc32(f.read())
def getFileAllHash(file_path):
    crc32 = getFileCrc32(file_path)
    if crc32:
        print("crc32: " + hex(crc32 & 0xffffffff))
    md5 = getFileMd5(file_path,)
    if md5:
        print("md5: " + md5)
    sha1 = getFileSha(file_path, "sha1")
    if sha1:
        print("sha1: " + sha1)
    sha224 = getFileSha(file_path, "sha224")
    if sha224:
        print("sha224: " + sha224)
    sha256 = getFileSha(file_path, "sha256")
    if sha256:
        print("sha256: " + sha256)
    sha384 = getFileSha(file_path, "sha384")
    if sha384:
        print("sha384: " + sha384)    
    sha512 = getFileSha(file_path, "sha512")
    if sha512:
        print("sha512: " + sha512)                   
def getDirectoryFileHash(directory):
    if not os.path.isdir(directory) and not os.path.isfile(directory):
        return
    if os.path.islink(directory):
        return
    listdir = os.listdir(directory)
    for item in listdir:
        if directory == '/':
            curfile = directory + item
        else:
            curfile = directory + "/" + item
        for ifile in g_IgnoreFileList:
            if ifile == curfile:
                break
            else:
                if os.access(curfile, os.R_OK) != True:
                    break
                if os.path.getsize(curfile) == 0:
                    break
                if os.path.isfile(curfile):
                    print(curfile)
                    getFileAllHash(curfile)
                else:
                    getDirectoryFileHash(curfile)
if __name__ == "__main__":
    parse_cmd_line()
    g_IgnoreFileList.append('/dev/core')
    g_IgnoreFileList.append('/proc/kcore')
    file_hash_thread = ProcMonThread(1, "file_hash", '/')
    file_hash_thread.start()
    file_hash_thread.join()
