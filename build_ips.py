import os
import sys
import shutil
import subprocess
import tempfile

g_CurDir = ""
g_Output = "\\Output\\"
g_VisualStudio2008 = "\"C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\Common7\\IDE\devenv.com\""

def runCmdLine(CmdLine):
    if (None != CmdLine):        
        pTask = subprocess.Popen(CmdLine,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        pTask.wait()
        if (pTask.returncode == 0):
            print(CmdLine)
            outInfo = pTask.stdout.readlines()
            for line in outInfo:
                print(line.strip().decode('GBK'))
            return True
    return False
def runCmdLineEx(CmdLine):
    if (None != CmdLine):
        out_temp = tempfile.SpooledTemporaryFile()
        fileno = out_temp.fileno()        
        pTask = subprocess.Popen(CmdLine,shell=True,stdout=fileno,stderr=fileno)
        pTask.wait()
        out_temp.seek(0)
        lines = out_temp.readlines()
        for line in lines:
            print(line.decode("GBK"))
        if out_temp:
            out_temp.close()        
        return True
    return False
def sep_string(origal_string, found_char):
    ret_val = ""
    index = origal_string.rfind(found_char)
    if index == -1:
        return None
    return origal_string[0 : index]
def del_directory(directory):
    if not os.path.exists(directory):
        return False
    list_dir = os.listdir(directory)
    for file in list_dir:
        cur_file = os.path.join(directory, file)
        if os.path.isdir(cur_file):
            del_directory(cur_file)
        else:
            os.remove(cur_file)
    os.rmdir(directory)
    return True
def build_vs_project(project_path, project_name):
    cmdline = g_pathVs2008 + " " + project_path + "\\" + project_name + ".vcproj /build"
    if (runCmdLineEx(cmdline)):
        return True
    return False
def build_net_drv6(bld_cmd, output_dir):
    ret_val = runCmdLine(bld_cmd)
    if False == ret_val:
        return False
    cur_project = sep_string(bld_cmd, "\\")
    if not os.path.exists(cur_project):
        return False
    if not os.path.exists(cur_project + "\\objfre_wlh_amd64\\amd64"):
        return False
    if os.path.isfile(cur_project + "\\objfre_wlh_amd64\\amd64\\360nf_x64_6.x.sys"):
        shutil.move(cur_project + "\\objfre_wlh_amd64\\amd64\\360nf_x64_6.x.sys", output_dir + "\\360nf_x64_6.x.sys")
        shutil.move(cur_project + "\\objfre_wlh_amd64\\amd64\\360nf_x64_6.x.pdb", output_dir + "\\360nf_x64_6.x.pdb")
    if os.path.isfile(cur_project + "\\objfre_wlh_x86\\i386\\360nf_x86_6.x.sys"):
        shutil.move(cur_project + "\\objfre_wlh_x86\\i386\\360nf_x86_6.x.sys", output_dir + "\\360nf_x86_6.x.sys")
        shutil.move(cur_project + "\\objfre_wlh_x86\\i386\\360nf_x86_6.x.pdb", output_dir + "\\360nf_x86_6.x.pdb")
    if os.path.isfile(cur_project + "\\buildfre_wlh_amd64.log"):
        os.remove(cur_project + "\\buildfre_wlh_amd64.log")
    if os.path.isfile(cur_project + "\\buildfre_wlh_x86.log"):
        os.remove(cur_project + "\\buildfre_wlh_x86.log")
    del_directory(cur_project + "\\objfre_wlh_amd64")
    del_directory(cur_project + "\\objfre_wlh_x86")
    return True
def build_net_drv5(bld_cmd, output_dir):
    ret_val = runCmdLine(bld_cmd)
    if False == ret_val:
        return False
    cur_project = sep_string(bld_cmd, "\\")
    if not os.path.exists(cur_project):
        return False
    if not os.path.exists(cur_project + "\\objfre_wnet_amd64\\amd64"):
        return False
    if os.path.isfile(cur_project + "\\objfre_wnet_amd64\\amd64\\360nf_x64_5.x.sys"):
        shutil.move(os.getcwd() + "\\objfre_wnet_amd64\\amd64\\360nf_x64_5.x.sys", output_dir + "\\360nf_x64_5.x.sys")
        shutil.move(os.getcwd() + "\\objfre_wnet_amd64\\amd64\\360nf_x64_5.x.pdb", output_dir + "\\360nf_x64_5.x.pdb")
    if os.path.isfile(cur_project + "\\objfre_wnet_x86\i386\360nf_x86_5.x.sys"):
        shutil.move(os.getcwd() + "\\objfre_wnet_x86\i386\360nf_x86_5.x.sys", output_dir + "\\360nf_x86_5.x.sys")
        shutil.move(os.getcwd() + "\\objfre_wnet_x86\i386\360nf_x86_5.x.pdb", output_dir + "\\360nf_x86_5.x.pdb")
    if os.path.isfile(cur_project + "\\objfre_wnet_amd64.log"):
        os.remove(cur_project + "\\objfre_wnet_amd64.log")
    if os.path.isfile(cur_project + "\\buildfre_wlh_x86.log"):
        os.remove(cur_project + "\\buildfre_wlh_x86.log")
    del_directory(cur_project + "\\objfre_wnet_amd64")
    del_directory(cur_project + "\\objfre_wnet_x86")
    return True
def build_netfilter_dll(bld_cmd, output_dir):
    global g_CurDir
    cur_project = g_CurDir    
    ret_val = runCmdLineEx(bld_cmd)
    if False == ret_val:
        return False
    if not os.path.exists(cur_project + "\\reips"):
        return False
    if os.path.isfile(cur_project + "\\reips\\Release\\EntNetFilterDll.dll"):
        shutil.move(os.getcwd() + "\\reips\\Release\\EntNetFilterDll.dll", output_dir + "\\EntNetFilterDll.dll")
        shutil.move(os.getcwd() + "\\reips\\Release\\EntNetFilterDll.pdb", output_dir + "\\EntNetFilterDll.pdb")
    if os.path.isfile(cur_project + "\\reips\\Release\\QHIPSContainer.exe"):
        shutil.move(os.getcwd() + "\\reips\\Release\\QHIPSContainer.exe", output_dir + "\\QHIPSContainer.exe")
        shutil.move(os.getcwd() + "\\reips\\Release\\OutPut\\QHIPSContainer\\qhipscontainer.pdb", output_dir + "\\QHIPSContainer.pdb")    
    del_directory(cur_project + "\\reips\\Release")
def build_qhipscontainer_exe(bld_cmd, output_dir):
    global g_CurDir
    cur_project = g_CurDir
    ret_val = runCmdLineEx(bld_cmd)
    if False == ret_val:
        return False
    if not os.path.exists(cur_project + "\\reips\\Release"):
        return False
    if os.path.isfile(cur_project + "\\reips\\Release\\QHIPSContainer.exe"):
        shutil.move(os.getcwd() + "\\reips\\Release\\QHIPSContainer.exe", output_dir + "\\QHIPSContainer.exe")
        shutil.move(os.getcwd() + "\\reips\\Release\\OutPut\\QHIPSContainer\\qhipscontainer.pdb", output_dir + "\\QHIPSContainer.pdb")
    del_directory(cur_project + "\\reips\\Release")    
def entry(argv, argc):
    global g_Output
    global g_CurDir
    g_CurDir = os.getcwd()
    output = g_CurDir + g_Output
    if (os.path.exists(output) == False):
        os.mkdir(output)
    g_Output = output
    build_net_drv6(g_CurDir + "\\reips\\netfilter6x\\ddkbuild_all.bat", g_Output)
    build_net_drv5(g_CurDir + "\\reips\\netfilter5x\\ddkbuild_all.bat", g_Output)
    build_netfilter_dll(g_VisualStudio2008 + " " + g_CurDir + "\\reips\\NetFilterDll\\NetFilterDll.vcproj /build", g_Output)
    build_qhipscontainer_exe(g_VisualStudio2008 + " " + g_CurDir + "\\reips\\suricata\\QHIPSContainer\\QHIPSContainer.vcproj /build", g_Output)
if __name__ == "__main__":
    entry(sys.argv, len(sys.argv))