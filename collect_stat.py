import os
import thread
import time

#list_system_stat = []

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
def parse_proc_stat(index_nums, stat_buf, proc_name, list_proc_stat):
    cpu_stat = ""
    mem_stat = ""
    list_stat = parse_system_stat(stat_buf, proc_name)
    for stat_info in list_stat:
        list_item = parse_one_item(stat_info)
        if list_item == None:
            continue
        dict_item = parse_app_top(list_item)
        if len(dict_item):
            list_proc_stat.append(dict_item)
        # cpu_stat = dict_item.get('CPU')
        # mem_stat = dict_item.get('MEM')
        # print(cpu_stat)
        # print(mem_stat)
    cpu_max, cpu_mid, cpu_min = find_list_max_value(list_proc_stat, 'CPU')
    mem_max, mem_mid, mem_min = find_list_max_value(list_proc_stat, 'MEM')
    info = str(index_nums) + " " + proc_name + " Cpu max: " + str(cpu_max) + " mid: " + str(cpu_mid) + " min: " + str(cpu_min) + \
    " mid: " + str(mem_mid) + " min: " + str(mem_min)
    #" Mem max: " + str(mem_max) +  + " cur: " + mem_stat
    print(info)
    with open(proc_name + '_stat.txt', 'w', encoding='utf-8') as f:
        f.write(info)
    return info
def thread_task_top(threadName, delay):
    list_agent_main_stat = []
    list_agent_update_stat = []
    list_agent_ResidentPlugin_stat = []
    list_agent_wsssr_defence_daemon_stat = []
    list_agent_wsssr_defence_service_stat = []
    list_agent_NetPortPlugin_stat = []
    list_agent_SystemAccountPlugin_stat = []
    count = 0
    while True:
        stat_buf = run_cmd_line("top -b -n 1")
        if stat_buf:
            parse_proc_stat(count, stat_buf, "agent_main", list_agent_main_stat)
            parse_proc_stat(count, stat_buf, "agent_update", list_agent_update_stat)
            parse_proc_stat(count, stat_buf, "ResidentPlugin", list_agent_ResidentPlugin_stat)
            parse_proc_stat(count, stat_buf, "wsssr_defence_d", list_agent_wsssr_defence_daemon_stat)
            parse_proc_stat(count, stat_buf, "wsssr_defence_s", list_agent_wsssr_defence_service_stat)
            parse_proc_stat(count, stat_buf, "SystemAccountPl", list_agent_SystemAccountPlugin_stat)
            parse_proc_stat(count, stat_buf, "NetPortPlugin", list_agent_NetPortPlugin_stat)
            print("")
        #     list_stat = parse_system_stat(stat_buf, "agent_main")
        #     for stat_info in list_stat:
        #         list_item = parse_one_item(stat_info)
        #         if list_item == None:
        #             continue
        #         dict_item = parse_app_top(list_item)
        #         if dict_item:
        #             list_system_stat.append(dict_item)
        # cpu_max, cpu_mid, cpu_min = find_list_max_value(list_system_stat, 'CPU')
        # print(str(count) + " Cpu max: " + str(cpu_max) + " mid: " + str(cpu_mid) + " min: " + str(cpu_min))
        # mem_max, mem_mid, mem_min = find_list_max_value(list_system_stat, 'MEM')
        # print(str(count) + " Mem max: " + str(mem_max) + " mid: " + str(mem_mid) + " min: " + str(mem_min))
        count = count + 1
        time.sleep(delay)
        #print "%s: %s" % (threadName,time.ctime(time.time()))
if __name__ == "__main__":
    print("collect system status info")
    try:
        thread.start_new_thread(thread_task_top, ("thread_task_top", 0.1,))
    except:
        print "Error: unable to start thread"
    while True:
        # inbuff = raw_input("input \'q\' quit:")
        # if(inbuff == 'q'):
        #     break
        # print(inbuff)
        time.sleep(60 * 60)
    #os.system("top")
