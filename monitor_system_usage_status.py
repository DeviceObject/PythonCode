import os
import time
import argparse
import threading

#list_system_stat = []
g_exitFlag = 0
class MonSysThread (threading.Thread):
    def __init__(self, name, filename, cpu, mem, diskio, delay):
        threading.Thread.__init__(self)
        self.name = name
        self.filename = filename
        self.cpu = cpu
        self.mem = mem
        self.diskio = diskio
        self.delay = delay
    def run(self):
        print("start thread: " + self.name)
        collect(self.name, self.filename, self.cpu, self.mem, self.diskio, self.delay)
        print("thread: " + self.name + " exit")
def collect(threadName, filename, cpu, mem, diskio, delay):
    count = 0
    list_monitor_status = []
    cpu_show = ""
    mem_show = ""
    info_show = ""
    cmd_line = "top -b -n 1 | grep " + filename
    while True:
        if g_exitFlag:
            threadName.exit()
        stat_buf = run_cmd_line(cmd_line)
        if stat_buf:
            list_stat = parse_system_stat(stat_buf, filename)
            for stat_info in list_stat:
                list_item = parse_one_item(stat_info)
                if list_item == None:
                    continue
                dict_item = parse_app_top(list_item)
                if len(dict_item):
                    list_monitor_status.append(dict_item)
                if cpu:
                    cpu_max, cpu_mid, cpu_min = find_list_max_value(list_monitor_status, 'CPU')
                    cpu_show = " Cpu: " + str(cpu_max) + " " + str(cpu_mid) + " " + str(cpu_min)
                if mem:
                    mem_max, mem_mid, mem_min = find_list_max_value(list_monitor_status, 'MEM')
                    mem_show = " Mem: " + str(mem_max) + " " + str(mem_mid) + " " + str(mem_min)
                info_show = str(count) + " " + cpu_show + " " + mem_show
                print(info_show)
            count = count + 1
            time.sleep(delay)
def parse_system_stat(stat_info, proc_name):
    count = 0
    offset = 0
    list_stat = []
    if stat_info == None or proc_name == None:
        return None
    total_length = len(stat_info)
    for i in range(0,total_length):
        if stat_info[i] == '\n':
            proc_stat_info = stat_info[offset : i]
            if proc_name in proc_stat_info:
                list_stat.append(proc_stat_info)
                #print(proc_stat_info)
            offset = i + 1;
    return list_stat
def parse_one_item(stat_item):
    list_item = []
    offset = 0
    next_offset = 0
    for i in range(0, len(stat_item)):
        if offset == 0:
            if stat_item[i] == ' ':
                continue
            else:
                offset = i
                continue
        if next_offset == 0 and offset:
            if stat_item[i] == ' ':
                next_offset = i
        if offset and next_offset:
            list_item.append(stat_item[offset:next_offset])
            offset = next_offset = 0
    if len(list_item):
        return list_item
    else:
        return None
def parse_app_top(item_stat_list):
    dict_item = {}
    i = 0
    for item in item_stat_list:
        if i == 0:
            dict_item['PID'] = item
        elif i == 1:
            dict_item['USER'] = item
        elif i == 2:
            dict_item['PR'] = item
        elif i == 3:
            dict_item['NI'] = item
        elif i == 4:
            dict_item['VIRT'] = item
        elif i == 5:
            dict_item['RES'] = item
        elif i == 6:
            dict_item['SHR'] = item
        elif i == 7:
            dict_item['S'] = item
        elif i == 8:
            dict_item['CPU'] = item
        elif i == 9:
            dict_item['MEM'] = item
        elif i == 10:
            dict_item['TIME'] = item
        elif i == 11:
            dict_item['COMMAND'] = item
        i = i + 1
    if len(dict_item):
        return dict_item
    else:
        return None
def run_cmd_line(cmd_line):
    out = os.popen(cmd_line)
    if out == None:
        return None
    stat_info = out.read();
    if stat_info == None:
        out.close()
        return None
    out.close()
    return stat_info
def find_list_max_value(list_stat_info, key_name):
    max_value = 0.0
    min_value = 0.0
    mid_value = 0.0
    total_value = 0.0
    count = 0;
    for dict_item in list_stat_info:
        value = dict_item.get(key_name)
        if value == None:
            continue
        if max_value < value:
            max_value = value
        if min_value > value:
            min_value = value
        if value:
            total_value = total_value + float(value)
            count = count + 1
    if total_value:
        mid_value = total_value/count
    return max_value, mid_value, min_value
def parse_cmd_line():
    parser = argparse.ArgumentParser(description='run a program file, monitor systen status')
    parser.add_argument('-e', dest = 'monitor_file', metavar = 'filename', help = 'monitor program file')
    parser.add_argument('-m', dest = 'monitor_memory', metavar = 'memory status', default = True, type = bool, help = 'system memory status')
    parser.add_argument('-c', dest = 'monitor_cpu', metavar = 'cpu status', default = True, type = bool, help = 'system cpu status')
    parser.add_argument('-d', dest = 'monitor_diskio', metavar = 'diskio status', default = True, type = bool, help = 'system diskio status')
    args = parser.parse_args()
    parser.print_help()
    return args.monitor_file, args.monitor_cpu, args.monitor_memory, args.monitor_diskio
if __name__ == "__main__":
    monitor_file, cpu, memory, diskio = parse_cmd_line()
    monitor_file = monitor_file.strip()
    print("collect system status info")
    monitor_system_thread = MonSysThread("MonSysThread", monitor_file, cpu, memory, diskio, 0.1)
    monitor_system_thread.start()
    monitor_system_thread.join()
