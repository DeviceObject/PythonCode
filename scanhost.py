from scapy.all import *
import os
import subprocess
import threading
import platform
import re
import sys
import argparse
import datetime

g_nmap_path = "nmap"

def is_system_type():
    sys_name = platform.system()
    if sys_name == "Windows":
        return "win"
    elif sys_name == "Linux":
        return "linux"
    else:
        return "other"
def run_cmd_line(cmd_line):
    print(cmd_line)
    out = os.popen(cmd_line)
    if out == None:
        return None
    stat_info = out.read();
    if stat_info == None:
        out.close()
        return None
    out.close()
    return stat_info
def get_sub_str(str_dat, start_name, end_name):
    ret_val = ""
    for i in range(0, len(str_dat)):
        if str_dat[i] == start_name:
            start_dat = str_dat[i + 1:]
            for j  in range(0, len(start_dat)):
                if start_dat[j] == end_name:
                    ret_val = start_dat[0:j]
                    return ret_val
    return ret_val
def get_ip_form_result(line_data):
    ip_list = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line_data)
    for ip in ip_list:
        return ip
    return ""
def get_ip_form_file(path, iplist):
    if not os.path.exists(path):
        return False
    file = open(path, 'r')
    if not file:
        return False
    while (True):
        one_line = file.readline()
        if not one_line:
            break
        ip = get_ip_form_result(one_line)
        if ip == None or 0 == len(ip):
            continue
        if ip in iplist:
            continue
        iplist.append(ip)
        print("find host ip: " + ip)
    return True
def scan_host_arp(ip, is_namp):
    #print("arp scan host " + ip)
    if is_namp == True:
        cmd_line = g_nmap_path + " -PR " + ip
        ret_info = run_cmd_line(cmd_line)
        if ret_info == None or 0 == len(ret_info):
            return False
        if "Host is up" in ret_info:
            print("arp scan host " + ip + " is active")
            return True
        else:
            print("arp scan host " + ip + " isn't valid")
            return False
    else:
        arpPkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst = ip)
        res = srp1(arpPkt, timeout=1, verbose=0)
        if res:
            return True
        else:
            return False
def scan_host_icmp(ip, is_namp):
    if is_namp == True:
        cmd_line = g_nmap_path + " -sP " + ip + " -disable-arp-ping"
        ret_info = run_cmd_line(cmd_line)
        if ret_info == None or 0 == len(ret_info):
            return False
        if "Host is up" in ret_info:
            print("icmp scan host " + ip + " is active")
            return True
        else:
            print("icmp scan host " + ip + " isn't valid")
            return False        
    else:
        return False
def scan_host_tcp_syn(ip, is_namp):
    if is_namp == True:
        cmd_line = g_nmap_path + " -sS " + ip
        ret_info = run_cmd_line(cmd_line)
        if ret_info == None or 0 == len(ret_info):
            return False
        if "Host is up" in ret_info:
            print("tcp syn scan host " + ip + " is active")
            return True
        else:
            print("tcp syn scan host " + ip + " isn't valid")
            return False        
    else:
        return False
def deep_scan_host(ip):
    print("deep_scan_host " + ip)
    cmd_line = g_nmap_path + " -O " + ip + " -p 22,23,135,139,445,3389 --max-os-tries 50 --max-hostgroup 10 --max-parallelism 2 --max-rtt-timeout 20 --osscan-guess"
    ret_info = run_cmd_line(cmd_line)
    if ret_info == None or 0 == len(ret_info):
        return ""
    return ret_info
class ParseArpCache(threading.Thread):
    def __init__(self, name, ip_list):
        threading.Thread.__init__(self)
        self.name = self.name
        self.platform = is_system_type()
        if self.platform == "win":
            self.cmd = "arp -a"
            self.separate = ','
            self.separate_num = 4
        elif self.platform == "linux":
            self.cmd = "arp -v"
            self.separate = ' '
            self.separate_num = 5
        else:
            self.cmd = "arp -a"
        self.ignore = "gateway"
        self.ip_list = ip_list
    def run(self):
        offset = 0;
        arp_buf = run_cmd_line(self.cmd)
        if arp_buf == None:
            return;
        for i in range(0, len(arp_buf)):
            if arp_buf[i] == '\n':
                one_line_data = arp_buf[offset : i]
                if self.ignore in one_line_data:
                    offset = i + 1;
                    continue
                #ip = get_sub_str(one_line_data, '(',')')
                if one_line_data == None or 0 == len(one_line_data):
                    continue
                ip = get_ip_form_result(one_line_data)
                if ip == None or 0 == len(ip):
                    continue
                #ip = one_line_data.split(",", 4);
                #print(type(ip))
                self.ip_list.append(ip)
                offset = i + 1
class ScanHost(threading.Thread):
    def __init__(self, name, ip_list, result):
        threading.Thread.__init__(self)
        self.ip_list = ip_list
        self.result = result
        self.active_host_list = []
    def run(self):
        offset = 0;
        is_active = False
        for host in self.ip_list:
            if host == None or 0 == len(host):
                continue
            is_active = scan_host_arp(host, True)
            if is_active == True:
                self.active_host_list.append(host)
            else:
                is_active = scan_host_icmp(host, False)
                if is_active == True:
                    self.active_host_list.append(host)
                else:
                    is_active = scan_host_tcp_syn(host, True)
                    if is_active == True:
                        self.active_host_list.append(host)
                    else:
                        continue
        for active_host in self.active_host_list:
            scan_result = deep_scan_host(active_host)
            for i in range(0, len(scan_result)):
                if scan_result[i] == '\n':
                    one_line = scan_result[offset : i + 1]
                    if "Running (JUST GUESSING):" in one_line:
                        system = one_line[len("Running (JUST GUESSING):"):]
                        pos = system.rfind(" ")
                        if pos:
                            system = system[0 : pos]
                        system = system.strip()
                        print(system)
                        if system == "" or system == None:
                            system = "unknow"
                        self.result.append(active_host)
                        self.result.append(system)
                        break
                    elif "Running:" in one_line:
                        system = one_line[len("Running:"):]
                        if system:
                            system = system.strip()
                            print(system)
                        if system == "" or system == None:
                            system = "unknow"
                        self.result.append(active_host)
                        self.result.append(system)
                        break
                    #else:
                    #    print("no found system info")
                    offset = i + 1
        return
class ConLogs(threading.Thread):
    def __init__(self, name, iplist):
        threading.Thread.__init__(self)
        self.name = name
        self.iplist = iplist
        self.log_list = []
        self.log_list.append("/var/log/secure")
    def run(self):
        print(self.name)
        for log_file in self.log_list:
            ret_val = get_ip_form_file(log_file, self.iplist)
            if ret_val == True:
                print("parse " + log_file + " success")
            else:
                print("parse " + log_file + " failed")
        return
            
def entry():
    host_ip = []
    result = []
    addr_range_list = []
    addr_start_list = []
    offset = 0
    
    parser = argparse.ArgumentParser(description = 'scan host script')
    parser.add_argument('-a', dest = 'address', metavar = 'ip', help = '192.168.1.1, 192.168.1-255')
    parser.add_argument('-t', dest = 'type', metavar = 'select check type', help = '1, arp cache\n2, connect log\n3, ip addr')
    args = parser.parse_args()
    if args.type == '1':
        parse_arp_thread = ParseArpCache("ParseArpCache", host_ip)
        parse_arp_thread.start()
        parse_arp_thread.join()        
    elif args.type == '2':
        conlogs_thread = ConLogs("ConLogs", host_ip)
        conlogs_thread.start()
        conlogs_thread.join()        
    elif args.type == '3':
        if args.address:
            if '-' in args.address:
                pos = args.address.find("-")
                start_ip = args.address[0 : pos]
                end_ip = args.address[pos + 1 : ]
                if '.' in end_ip:
                    for i in range(0, len(end_ip)):
                        if end_ip[i] == '.':
                            addr_range = end_ip[offset : i]
                            addr_range_list.append(addr_range)
                            offset = i + 1
                    addr_range = end_ip[offset : i + 1]
                    addr_range_list.append(addr_range)
                if '.' in start_ip:
                    addr_start_offset = len(start_ip)
                    for i in range(len(start_ip) - 1, 0, -1):
                        if start_ip[i] == '.':
                            addr_start = start_ip[i + 1 : addr_start_offset]
                            addr_start_offset = i
                            addr_start_list.append(addr_start)
                    addr_start = start_ip[i - 1 : addr_start_offset]
                    addr_start_list.append(addr_start)
                    addr_start_list.reverse()
                num_point = end_ip.count('.')
                if num_point == 2:
                    for a in range(int(addr_start_list[1]), int(addr_range_list[0])):
                        for b in range(int(addr_start_list[2]), int(addr_range_list[1])):
                            for c in range(int(addr_start_list[3]), int(addr_range_list[2])):
                                one_ip = addr_start_list[0] + '.' + str(a) + '.' + str(b) + '.' + str(c)
                                host_ip.append(one_ip)
                elif num_point == 1:
                    for b in range(int(addr_start_list[2]), int(addr_range_list[0])):
                        for c in range(int(addr_start_list[3]), int(addr_range_list[1])):
                            one_ip = addr_start_list[0] + '.' + addr_start_list[1] + '.' + str(b) + '.' + str(c)
                            host_ip.append(one_ip)             
                else:
                    #for c in range(int(addr_start_list[3]), int(addr_range_list[0])):
                    #    one_ip = addr_start_list[0] + '.' + addr_start_list[1] + '.' + str(b) + '.' + str(c)
                    #    host_ip.append(one_ip)
                    index = start_ip.rfind('.')
                    if index != -1:
                        splice_ip = start_ip[0 : index + 1]
                        splice_start = start_ip[index + 1:]
                        for i in range(int(splice_start), int(end_ip)):
                            one_ip = splice_ip + str(i)
                            host_ip.append(one_ip)                
            #else:
                #index = start_ip.rfind('.')
                #if index == -1:
                #    return
                #splice_ip = start_ip[0 : index + 1]
                #splice_start = start_ip[index + 1:]
                #for i in range(int(splice_start), int(end_ip)):
                #    one_ip = splice_ip + str(i)
                #    print(one_ip)
                #    host_ip.append(one_ip)
                #num = len(addr_num)
                #if num == 2:
                #    net_addr = start_ip + 
                #for i in range(0, len(addr_num)):
                #    for j in 
            else:
                host_ip.append(args.address)        
    else:
        parser.print_help()
    if "0.0.0.0" in host_ip:
        host_ip.remove("0.0.0.0")
        print("remove ip: 0.0.0.0")
    if "127.0.0.1" in host_ip:
        host_ip.remove("127.0.0.1")
        print("remove ip: 127.0.0.1")

    scan_thread = ScanHost("ScanHost", host_ip, result)
    scan_thread.start()
    scan_thread.join()
    
    for i in range(0, len(result), 2):
        print("host: " + result[i] + "\t" + result[i + 1])

if __name__ == "__main__":
    start = datetime.datetime.now()
    entry()
    end = datetime.datetime.now()
    print("running time: %s seconds " % (end - start))