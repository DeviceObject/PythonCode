import os
import json
import urllib
import xlrd
import xlwt
import time
import bs4
import requests
import zipfile
from xlutils.copy import copy

def collect_info_from_json_field(input_json_file):
    if not os.path.exists(input_json_file):
        return
    with open(input_json_file, 'r', encoding='utf-8') as file_json:
        file_data = file_json.read()
    file_json.close()
    json_data = json.loads(file_data)
    for item in json_data.items():
        if item[0] == "CVE_Items":
            for i in range(len(item[1])):
                for sub_item in item[1][i].items():
                    if sub_item[0] == "cve":
                        for third_item in sub_item[1]:
                            if third_item[0] == "CVE_data_meta":
                                print(third_item[1])
def extract_all_file(origal_directory):
    file_list = os.listdir()
    for findfile in file_list:
        cur_file = os.path.join(origal_directory, findfile)
        extract_file(cur_file, origal_directory, "")
def extract_file(origal_file, dest_directory, password):
    if not os.path.exists(origal_file):
        return
    zip_file = zipfile.ZipFile(origal_file)
    try:
        zip_file.extractall(path = dest_directory, pwd = password)
    except RuntimeError as e:
        print(e)
    zip_file.close()
def fetch_file_from_url(url, file_type, cache_directory):
    find_url_list = []
    if not os.path.exists(cache_directory):
        os.mkdir(cache_directory)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as exc:
        print(exc)
    soup = bs4.BeautifulSoup(response.content)
    href = soup.select("a[target=_blank]")
    for i in range(len(href)):
        cur_url = href[i].get("href")
        print(cur_url)
        find_url_list.append(cur_url)
    for i in range(len(find_url_list)):
        if find_url_list[i].endswith(file_type):
            print("start download file: " + find_url_list[i])
            downloadfile(find_url_list[i], cache_directory)
            print(find_url_list[i] + "download file complete")
def downloadfile(url, saveDirectory):
    cur_length = 0
    response = urllib.request.urlopen(url)
    save_file_path = os.path.join(saveDirectory, os.path.basename(url))
    print(save_file_path)
    cache_file_path = save_file_path + ".download"
    print(cache_file_path)
    if not os.path.exists(save_file_path):
        with open(cache_file_path, 'wb') as new_file:
            while(cur_length <= response.length):
                buffer = response.read()
                new_file.write(buffer)
                cur_length = cur_length + len(buffer)
            new_file.close()
            os.renames(cache_file_path, save_file_path)
    else:
        if os.path.getsize(save_file_path) != response.length:
            os.remove(save_file_path)
            with open(cache_file_path, 'wb') as new_file:
                while(cur_length <= response.length):
                    buffer = response.read(1024)
                    new_file.write(buffer)
                new_file.close()
                os.renames(cache_file_path, save_file_path)
        else:
            print("file is exist")
def write_excel(excel_file, write_data):
    if not os.path.exists(excel_file):
        line_title = ["RuleId", "CVE Number", "CWE", "BID", "Descript"]
        new_file = xlwt.Workbook(encoding='utf-8')
        new_sheet = new_file.add_sheet('RuleInfo',cell_overwrite_ok = True)
        for i in range(len(line_title)):
            if line_title[i] == "CVE Number" and line_title[i] == "Descript":
                new_sheet.write(0, i, line_title[i], set_style('Times New Roman', 500 , True))
            else:
                new_sheet.write(0, i, line_title[i], set_style('Times New Roman', 300 , True))
        for i in range(len(write_data)):
            new_sheet.write(1, i, write_data[i])
        new_file.save(excel_file)
    else:
        workbook = xlrd.open_workbook(excel_file)
        sheets = workbook.sheet_names()
        worksheet = workbook.sheet_by_name(sheets[0])
        rows_old = worksheet.nrows
        new_workbook = copy(workbook)
        new_worksheet = new_workbook.get_sheet(0)
        for i in range(len(write_data)):
            new_worksheet.write(rows_old, i, write_data[i])
        new_workbook.save(excel_file)
def set_style(name, height, bold = False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style
def search_signature(origal_data, start_signature, endsignature):
    find_signature = []
    cur_origal_data = origal_data
    while (True):
        index = cur_origal_data.find(start_signature)
        if index == -1:
            break
        sub_index = cur_origal_data[index:].find(endsignature)
        if sub_index == -1:
            break
        find_signature.append(cur_origal_data[index + len(start_signature):index + sub_index])
        cur_origal_data = cur_origal_data[index + sub_index:]
    return find_signature
def fetch_cve_number(input_json_file, output_file):
    if not os.path.exists(input_json_file):
        print("json file isn't exist")
        return False
    with open(input_json_file, 'r', encoding='utf-8') as file_json:
        file_data = file_json.read()
    file_json.close()
    json_data = json.loads(file_data)
    for item in json_data.items():
        origal_id = item[0]
        for sub_item in item[1].items():
            if sub_item[0] == "product_feature":
                for third_item in sub_item[1].items():
                    rule_type = third_item[0]
                    if third_item[0] == "agentless":
                        continue
                    # elif third_item[0] == "agent_windows":
                    #     continue
                    # elif third_item[0] == "agent_linux":
                    #     continue
                    # else:
                    #     print("unknow platfrom")
                    for fourth_item in third_item[1].items():
                        if fourth_item[0] == "platform":
                            platform = fourth_item[1]
                        elif fourth_item[0] == "cvss":
                            cvss = fourth_item[1]
                        elif fourth_item[0] == "orig_rule":
                            origal_rule = fourth_item[1]
                            cve_list = []
                            cve_list = search_signature(origal_rule, "reference:cve,", ";")
                            cve_name = ""
                            for cve_item in cve_list:
                                cve_name = cve_name + "CVE-" + cve_item + " "
                        elif fourth_item[0] == "desc_zh":
                            rule_desc = fourth_item[1]
                        elif fourth_item[0] == "rule_id":
                            rule_id = fourth_item[1]
                        else:
                            #print(str(fourth_item[0]) + " " + str(fourth_item[1]))
                            cwe_name = ""
                            bid_name = ""
                    write_data = []
                    write_data.append(rule_id)
                    write_data.append(cve_name)
                    write_data.append(cwe_name)
                    write_data.append(bid_name)
                    write_data.append(rule_desc)
                    write_excel(output_file, write_data)
                    #rule_info = str(origal_id) + " " + str(rule_id) + " " + rule_type + " " + platform + " " + cvss + " " + cve_name + " " + rule_desc
                    #print(rule_info)
    return True
if __name__ == "__main__":
    #downloadfile()
    collect_info_from_json_field("D:\\MyCodeLibrary\\mycode\\PythonCode\\cache1\\nvdcve-1.1-2020.json\\nvdcve-1.1-2020.json")
    fetch_file_from_url("https://nvd.nist.gov/vuln/data-feeds#JSON_FEED", ".zip", os.path.join(os.getcwd(), "cache1"))
    extract_all_file(os.path.join(os.getcwd(), "cache1"))
    fetch_cve_number(os.sys.argv[1], os.path.join(os.getcwd(), "New_Output.xls"))
