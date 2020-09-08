import os
import sys
import shutil

g_cur_path = ""
def writeFile(filename, writedat):
    if os.path.exists(filename):
        os.remove(filename)
    try:
        cfgfile = open(filename, "w+")
        cfgfile.write(writedat)
    except IOError:
        print("file is exist or write faild")
    else:
        cfgfile.close()
        return len(writedat)
def getFileSuffix(filename):
    index = filename.rfind('.')
    if index == -1:
        return None
    suffix = filename[index + 1:]
    return suffix
def getFileName(filepath):
    index = filepath.rfind('.')
    if index == -1:
        return None
    index2 = filepath.rfind('\\')
    if index2 == -1:
        name = filepath[0:index]
    else:
        name = filepath[index2 + 1:index]
    return name
def genMakeCabCmdLine(cabname, infpath, syspath):
    makeCmdLine = ""
    makeCmdLine += ".OPTION EXPLICIT"
    makeCmdLine += "\r\n"
    makeCmdLine += ".Set CabinetFileCountThreshold = 0"
    makeCmdLine += "\r\n"
    makeCmdLine += ".Set FolderFileCountThreshold = 0"
    makeCmdLine += "\r\n"
    makeCmdLine += ".Set FolderSizeThreshold = 0"
    makeCmdLine += "\r\n"
    makeCmdLine += ".Set MaxCabinetSize = 0"
    makeCmdLine += "\r\n"
    makeCmdLine += ".Set MaxDiskFileCount = 0"
    makeCmdLine += "\r\n"
    makeCmdLine += ".Set MaxDiskSize = 0"
    makeCmdLine += "\r\n"
    makeCmdLine += ".Set CompressionType = MSZIP"
    makeCmdLine += "\r\n"
    makeCmdLine += ".Set Cabinet = on"
    makeCmdLine += "\r\n"
    makeCmdLine += ".Set Compress = on"
    makeCmdLine += "\r\n"
    makeCmdLine += ".Set CabinetNameTemplate = " + cabname + ".cab"
    makeCmdLine += "\r\n"
    makeCmdLine += ".Set DestinationDir = " + cabname
    makeCmdLine += "\r\n"
    makeCmdLine += infpath
    makeCmdLine += "\r\n"
    makeCmdLine += syspath
    makeCmdLine += "\r\n"
    return makeCmdLine
def runMakeCabCmdLine(filepath, ddfname):
    curdir = os.getcwd()
    os.chdir(filepath)
    runCmdLine = "makecab.exe /f " + filepath + "\\" + ddfname + ".ddf"
    os.system(runCmdLine)
    if os.path.exists(filepath + "\\" + "disk1" + "\\" + ddfname + ".cab"):
        shutil.move(filepath + "\\" + "disk1" + "\\" + ddfname + ".cab", filepath + "\\" + ddfname + ".cab")
        os.rmdir(filepath + "\\" + "disk1")
    if os.path.exists(filepath + "\\" + "setup.inf"):
        os.remove(filepath + "\\" + "setup.inf")
    if os.path.exists(filepath + "\\" + "setup.rpt"):
        os.remove(filepath + "\\" + "setup.rpt")
    if os.path.exists(filepath + "\\" + ddfname + ".cab"):
        os.chdir(curdir)
        return ddfname + ".cab"
    else:
        os.chdir(curdir)
        return None
def genCabFile(parentpath, sigfilename):
    if not os.path.exists(parentpath + "\\" + sigfilename + ".inf"):
        print(parentpath + "\\" + sigfilename + ".inf" + " file isn't exist")
        return None
    if not os.path.exists(parentpath + "\\" + sigfilename + ".sys"):
        print(parentpath + "\\" + sigfilename + ".sys" + " file isn't exist")
        return None
    makeCmd = genMakeCabCmdLine(sigfilename, parentpath + "\\" + sigfilename + ".inf", parentpath + "\\" + sigfilename + ".sys")
    if makeCmd:
        if writeFile(parentpath + "\\" + sigfilename + ".ddf", makeCmd):
            cabfile = runMakeCabCmdLine(parentpath, sigfilename)
            if cabfile and os.path.exists(parentpath + "\\" + cabfile):
                os.remove(parentpath + "\\" + sigfilename + ".ddf")
                return cabfile
def doCabModule(filepath):
    sigCfgInfo = ""
    if os.path.isdir(filepath):
        for filename in os.listdir(filepath):
            filesuffix = getFileSuffix(filename)
            if filesuffix == None or filesuffix != "sys":
                continue
            shortname = getFileName(filename)
            if shortname == None:
                continue
            if not os.path.exists(filepath + "\\" + shortname + ".inf"):
                continue
            if not os.path.exists(filepath + "\\" + shortname):
                os.mkdir(filepath + "\\" + shortname)            
            index = shortname.find('_')
            if index == -1:
                continue
            newfilename = shortname[:index]
            shutil.copy2(filepath + "\\" + filename, filepath + "\\" + shortname + "\\" + newfilename + "." + filesuffix)
            shutil.copy2(filepath + "\\" + shortname + ".inf", filepath + "\\" + shortname + "\\" + newfilename + ".inf")
            cabfile = genCabFile(filepath + "\\" + shortname, newfilename)
            if cabfile == None:
                continue
            if os.path.exists(filepath + "\\" + shortname + "\\" + cabfile):
                shutil.move(filepath + "\\" + shortname + "\\" + cabfile, filepath + "\\" + shortname + "." + getFileSuffix(cabfile))
            if not os.path.exists(filepath + "\\" + "sign_config.ini"):
                if not genFile(filepath + "\\" + "sign_config.ini"):
                    continue
                sigCfgInfo += genConfigInfo(shortname + "." + getFileSuffix(cabfile), True)
            else:
                sigCfgInfo += genConfigInfo(shortname + "." + getFileSuffix(cabfile), True)
        genConfigFile(filepath + "\\" + "sign_config.ini", sigCfgInfo)
    else:
        curdir = os.getcwd()
        filesuffix = getFileSuffix(filepath)
        if filesuffix == None or filesuffix != "sys":
            return False        
        shortname = getFileName(filepath)
        if shortname == None:
            return False        
        cabfile = genCabFile(curdir, shortname)
        if cabfile == None:
            return False
        if not os.path.exists(curdir + "\\" + "sign_config.ini"):
            if not genFile(curdir + "\\" + "sign_config.ini"):
                return False
            sigCfgInfo += genConfigInfo(cabfile, True)
        else:
            sigCfgInfo += genConfigInfo(cabfile, True)
        genConfigFile(curdir + "\\" + "sign_config.ini", sigCfgInfo)        
def runMakeCat():
    runCmdLine = "Inf2Cat.exe /driver:./ /os:Vista_X86,Vista_X64,7_X86,7_X64,Server2008_X64,Server2008_X86,"
    runCmdLine2 = "Server2008R2_X64,Server8_X64,8_X86,8_X64,Server6_3_X64,6_3_X64,6_3_X86,Server10_X64,10_X64,10_X86,"
    runCmdLine3 = "10_AU_X86,10_AU_X64,Server2016_X64,10_RS2_X86,10_RS2_X64,ServerRS2_X64"
    os.system(runCmdLine + runCmdLine2 + runCmdLine3)
def genConfigInfo(filename, isEvSignature):
    sigCfgInfo = '[' + filename + ']' + "\n"
    sigCfgInfo += "path=" + "\"" + filename + "\"" + "\n"
    if isEvSignature == True:
        sigCfgInfo += "sign_type=" + "\"" + "ev" + "\"" + "\n"
    #elif isEvSignature == "esg":
    #    sigCfgInfo += "sign_type=" + "\"" + "s3" + "\"" + "\n"
    else:
        sigCfgInfo += "sign_type=" + "\"" + "s3,esg" + "\"" + "\n"
    return sigCfgInfo
def genConfigFile(filename, writefileData):
    try:
        cfgfile = open(filename, "a+")
        cfgfile.write(writefileData)
    except IOError:
        print("read or write file faild")
    else:
        cfgfile.close()
        return len(writefileData)
def genFile(filename):
    if os.path.exists(filename):
        return False
    try:
        cfgfile = open(filename, "w")
    except IOError:
        print("file is exist or write faild")
    else:
        cfgfile.close()
    return True

def makeSignatureConfigFile(filename):
    suffix = getFileSuffix(filename)
    if str(suffix).lower() in ["exe", "dll", "sys"]:
        return genConfigInfo(filename, False)
    elif str(suffix).lower() in ["cat", "cab"]:
        return genConfigInfo(filename, True)
    else:
        return None

def main(argc, argv):
    print("select function module")
    print("input 1 gen cab file")
    select = input("input num code:")
    if select == '1':
        doCabModule(os.getcwd())
    
if __name__ == "__main__":
    main(len(sys.argv), sys.argv)