#/bin/env python
# -*- encoding: utf-8 -*-
import argparse
import os
import sys
import subprocess
import re


def get_so_func_map(path):
    func_map = {}

    try:
        return_info = subprocess.Popen('nm -D ' + path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #return_info.wait()

        for binfos in return_info.stdout:
            func_info = []

            # 2列
            pattern_column_2 = re.compile(r'^(\s+)(\S)\s+(\S+)', re.S)
            match_name_2 = pattern_column_2.match(binfos)
            if match_name_2 is not None:
                func_info.append("")                    # 实现文件
                func_info.append(match_name_2.group(2)) #
                func_info.append(match_name_2.group(3)) # 
                func_map[func_info[2]] = func_info      #
                #print(str.format('\033[31m {}', func_info))

            # 3列
            pattern_column_3 = re.compile(r'^(\S+)\s+(\S)\s+(\S+)', re.S)
            match_name_3 = pattern_column_3.match(binfos)
            if match_name_3 is not None:
                func_info.append(os.path.basename(path))
                func_info.append(match_name_3.group(2))
                func_info.append(match_name_3.group(3))
                func_map[func_info[2]] = func_info
                #print(str.format('\033[32m {}', func_info))

    except subprocess.CalledProcessError:
        pass

    return func_map

def get_ldd_so_lib(path):
    so_paths = []

    try:
        return_info = subprocess.Popen('ldd ' + path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #return_info.wait()

        for binfos in return_info.stdout:
            pattern_so_path = re.compile(r'^\s+\S+\s=>\s(/\S+)\s', re.S)
            match_so_path = pattern_so_path.match(binfos)
            if match_so_path is not None:
                so_paths.append(match_so_path.group(1))

    except subprocess.CalledProcessError:
        print("err")
        pass
    
    return so_paths

def get_ldd_so_lib_ex(path):
    so_paths = set()

    try:
        return_info = subprocess.Popen('ldd ' + path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #return_info.wait()

        for binfos in return_info.stdout:
            pattern_so_path = re.compile(r'^\s+\S+\s=>\s(/\S+)\s', re.S)
            match_so_path = pattern_so_path.match(binfos)
            if match_so_path is not None:
                so_paths.add(match_so_path.group(1))
                so_paths.union(so_paths, get_ldd_so_lib(match_so_path.group(1)))

    except subprocess.CalledProcessError:
        print("err")
        pass
    
    return so_paths


def get_rpath_so_lib(path):
    rpaths = []
    so_paths = []
    all_so_paths = []

    try:
        return_info = subprocess.Popen('readelf -d ' + path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #return_info.wait()

        for binfos in return_info.stdout:
            pattern_rpath = re.compile(r'.*\s+Library\srpath:\s\[(\S+)\]', re.S)
            match_rpath = pattern_rpath.match(binfos)
            if match_rpath is not None:
                rpaths.append(match_rpath.group(1))

            pattern_lib = re.compile(r'.*\s+Shared\slibrary:\s\[(\S+)\]', re.S)
            match_lib = pattern_lib.match(binfos)
            if match_lib is not None:
                so_paths.append(match_lib.group(1))

    except subprocess.CalledProcessError:
        pass

    if 0 != len(rpaths):
        for rpath in rpaths:
            try:
                return_info = subprocess.Popen('ls ' + rpath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                for binfos in return_info.stdout:
                    if( -1 != binfos.decode().find(".so")):
                        so_path = rpath + "/" + binfos
                        so_path = so_path.strip()
                        all_so_paths.append(so_path)

            except subprocess.CalledProcessError:
                pass

    return rpath, so_paths, all_so_paths


def fill_map(so_paths, func_map):
    for so_path in so_paths:
        tmp_map = get_so_func_map(so_path)
        for k, v in tmp_map.items():
            if "" != v[0] and func_map.has_key(k):
                func_map[k][0] = v[0]
    return func_map


def print_fun_info(show_err, func_map):
    for k, v in func_map.items():
        if "" == v[0]:
            print(str.format('\033[31m{} {} {}', '{: <40}'.format(v[0]), '{: <5}'.format(v[1]), '{: <100}'.format(v[2])))

        if "NO" == show_err and "" != v[0]:
            print(str.format('\033[32m{} {} {}', '{: <40}'.format(v[0]), '{: <5}'.format(v[1]), '{: <100}'.format(v[2])))

def print_test():
    print('\033[0m这是显示方式0')
    print('\033[1m这是显示方式1')
    print('\033[4m这是显示方式4')
    print('\033[5m这是显示方式5')
    print('\033[7m这是显示方式7')
    print('\033[8m这是显示方式8')
    print('\033[30m这是前景色0')
    print('\033[31m这是前景色1')
    print('\033[32m这是前景色2')
    print('\033[33m这是前景色3')
    print('\033[34m这是前景色4')
    print('\033[35m这是前景色5')
    print('\033[36m这是前景色6')
    print('\033[37m这是前景色7')
    print('\033[40m这是背景色0')
    print('\033[41m这是背景色1')
    print('\033[42m这是背景色2')
    print('\033[43m这是背景色3')
    print('\033[44m这是背景色4')
    print('\033[45m这是背景色5')
    print('\033[46m这是背景色6')
    print('\033[47m这是背景色7')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--file', default='/usr/test.so', help='so file path')
    parser.add_argument('--err', default='NO', help='show all func info')
    parser.add_argument('--ex', default='NO', help='ex rpath')
    args = parser.parse_args()

    # 获取当前so库函数信息
    func_map = get_so_func_map(args.file)

    # 获取依赖so
    so_paths = get_ldd_so_lib(args.file)

    # 合并数据
    func_map = fill_map(so_paths, func_map)

    # 超级模式
    if "NO" != args.ex:
        _, _, all_so_paths = get_rpath_so_lib(args.file)
        func_map = fill_map(all_so_paths, func_map)

    # 打印函数
    print_fun_info(args.err, func_map)

