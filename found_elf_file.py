#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import subprocess
import shutil

elf_file_list = []

def constructElfListInfo(name, path, length, info):
    elf_file_list = {}
    elf_file_list.setdefault('name', '')
    elf_file_list.setdefault('path', '')
    elf_file_list.setdefault('info', '')
    elf_file_list.setdefault('len', 0)
    
    elf_file_list['name'] = name
    elf_file_list['path'] = path
    elf_file_list['info'] = info
    elf_file_list['len'] = length
    return elf_file_list
def zip_decompression(zip_full_path, dest_full_path, password):
    print("decompression file: " + zip_full_path)
    print("decompression dest full path: " +  dest_full_path)
    cmd = "unzip -o -P " + password + " " + zip_full_path + " -d " + dest_full_path
    ret_val = os.system(cmd)
    print(ret_val)
    return True
def is_elf_file(path):
    ret_val = False
    print("file check: " + path)
    try:
        with open(path, 'rb') as file:
            magic_number = file.read(4)
            if magic_number == b'\x7FELF':
                ret_val = True
            else:
                ret_val = False
    except:
        ret_val = False
    return ret_val
def copy_file(src, dst):
    try:
        shutil.copyfile(src, dst)
        #print("copy " + src + " to " + dst + " success.")
    except IOError as e:
        print("copy " + src + " to " + dst + " failed.")
        print(e)
def create_dir(dir):
    ret_val = False
    if not os.path.isdir(dir):
        try:
            os.makedirs(dir)
            print("create dir: " + dir + " success")
            ret_val = True
        except OSError as e:
            print("create dir: " + dir + " failed")
            ret_val = False
    else:
        print("dir: " + dir + " is exist")
        ret_val = True
    return ret_val
def searchElfFiles(path, list_elf_files):
    print("search path: " + path)
    count = 0
    if not os.path.isdir(path):
        return None
    file_list = os.listdir(path)
    for file in file_list:
        full_path = os.path.join(path, file)
        if os.path.isdir(full_path):
            count = searchElfFiles(full_path, list_elf_files)        
        if not os.path.isfile(full_path):
            continue
        index = file.rfind(".zip")
        if index != -1:
            decompression_path = full_path[:full_path.rfind(".zip")]
            is_decompression = zip_decompression(full_path, decompression_path, "infected")
            if is_decompression == True:
                searchElfFiles(decompression_path, list_elf_files)
        is_elf = is_elf_file(full_path)
        if is_elf == False:
            continue
        file_stat = os.stat(full_path)
        info = get_elf_file_info(full_path)
        name = path[path.rfind('/') + 1:]
        list_elf = constructElfListInfo(name, full_path, file_stat.st_size, info)
        list_elf_files.append(list_elf)
def get_elf_file_info(path):
    cmd = "file " + path
    ret_cmd_info = os.popen(cmd)
    info = ret_cmd_info.read()
    return info
def main():
    global elf_file_list
    out_dir = "/root/elf_ransomware/"
    create_dir(out_dir)
    searchElfFiles(sys.argv[1], elf_file_list)
    for elf_file in elf_file_list:
        print(str(elf_file))
        print("")
        tmp_path = str(elf_file['path'])
        dst_file = out_dir + tmp_path[tmp_path.rfind('/') + 1:]
        copy_file(str(elf_file['path']), dst_file)
    elf_file_num = len(elf_file_list)
    print("found elf ransomware num: " + str(elf_file_num))
    return
if __name__ == "__main__":
    main()
