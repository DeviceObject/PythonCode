#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

video_list = []

def constructVideoInfo(name, path, length):
    video_dict = {}
    video_dict.setdefault('name', '')
    video_dict.setdefault('path', '')
    video_dict.setdefault('length', 0)
    
    video_dict['name'] = name
    video_dict['path'] = path
    video_dict['length'] = length
    return video_dict
def renameDirFiles(path, is_left, sub_name):
    print("argv[1]: " + path)
    print("argv[2]: " + sub_name)
    count = 0
    if not os.path.isdir(path):
        return None
    file_list = os.listdir(path)
    for file in file_list:
        old_full_path = os.path.join(path, file)
        if os.path.isdir(old_full_path):
            count = renameDirFiles(old_full_path, is_left, sub_name)        
        if not os.path.isfile(old_full_path):
            continue
        if is_left == True:
            index = file.find(sub_name)
            if index == -1:
                continue            
            new_name = file[index + len(sub_name):]
        else:
            index = file.rfind(sub_name)
            if index == -1:
                continue   
            new_name = file[:index + len(sub_name)]
        new_full_path = os.path.join(path, new_name)
        if os.path.exists(new_full_path):
            old_stat = os.stat(old_full_path)
            new_stat = os.stat(new_full_path)
            if new_stat.st_size > old_stat.st_size:
                print("exist file name: " + new_name)
                print("del file: " + old_full_path)
                os.remove(old_full_path)
            elif new_stat.st_size < old_stat.st_size:
                print("exist file name: " + new_name)
                print("del file: " + new_full_path)                
                os.remove(new_full_path)
                os.rename(old_full_path, new_full_path)
                count = count + 1
                print("rename " + file + " to " + new_name)
            else:
                print("exist file name: " + new_name)
                new_name = input("input new file name or del(del origal file):")
                if new_name == "del":
                    os.remove(new_full_path)
                else:
                    new_full_path = os.path.join(path, new_name)
                os.rename(old_full_path, new_full_path)
                count = count + 1
                print("rename " + file + " to " + new_name)
        else:
            os.rename(old_full_path, new_full_path)
            count = count + 1
            print("rename " + file + " to " + new_name)
    return count
def main():
    global video_list
    videoInfo = constructVideoInfo('test', 'test', 1234)
    video_list.append(videoInfo)
    count = renameDirFiles(sys.argv[1], True, sys.argv[2])
    print("rename total: " + str(count))
    return
if __name__ == "__main__":
    main()
    