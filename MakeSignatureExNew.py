import sys
import datetime
import shutil
import hashlib
import zlib
import os
import pefile
import time

g_local_signature_server_input = "\\\\10.95.158.254\\input\\wanghui02"
g_local_signature_server_output = "\\\\10.95.48.22\\Sign\\wanghui02"
g_local_signature_config_filename = "\\sign_config.ini"
g_local_signature_success_filename = "\\upload.ok"
g_local_signature_filename = []

g_project_work = ""
g_inputwork = ""
g_userwork = ""
g_outputwork = ""

g_isSigSys = False
g_isSigCab = False
g_isSigCat = False

g_isDefault = False
g_DefaultSigName = "DefaultName"


class SignatureFileInfo:
    def __init__(self):
        self.filename = ""
        self.shortname = ""
        self.output = ""
        self.infpath = ""
        self.md5sum = ""
        self.signature_md5sum = ""
def getFileCrc32(filename):
    if not os.path.isfile(filename):
        return
    f = open(filename,'rb')
    if not f:
        return
    return zlib.crc32(f.read())

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
    f = open(filename,'rb')
    while True:
        b = f.read(4096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def getFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(4096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()
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
def runMakeCat():
    runCmdLine = "Inf2Cat.exe /driver:./ /os:Vista_X86,Vista_X64,7_X86,7_X64,Server2008_X64,Server2008_X86,"
    runCmdLine2 = "Server2008R2_X64,Server8_X64,8_X86,8_X64,Server6_3_X64,6_3_X64,6_3_X86,Server10_X64,10_X64,10_X86,"
    runCmdLine3 = "10_AU_X86,10_AU_X64,Server2016_X64,10_RS2_X86,10_RS2_X64,ServerRS2_X64"
    os.system(runCmdLine + runCmdLine2 + runCmdLine3)
def runMakeCabCmdLine(ddfname):
    runCmdLine = "makecab.exe /f " + ddfname + ".ddf"
    curwork = os.getcwd()
    os.system(runCmdLine)
    if os.path.exists(curwork + "\\" + "disk1" + "\\" + ddfname + ".cab"):
        shutil.move(curwork + "\\" + "disk1" + "\\" + ddfname + ".cab", curwork + "\\" + ddfname + ".cab")
        os.rmdir(curwork + "\\" + "disk1")
    if os.path.exists(curwork + "\\" + "setup.inf"):
        os.remove(curwork + "\\" + "setup.inf")
    if os.path.exists(curwork + "\\" + "setup.rpt"):
        os.remove(curwork + "\\" + "setup.rpt")
    if os.path.exists(curwork + "\\" + ddfname + ".cab"):
        return curwork + "\\" + ddfname + ".cab"
    else:
        return None
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
def genCabFile(sigfilename):
    curworkdir = os.getcwd()
    if not os.path.exists(curworkdir + "\\" + sigfilename + ".inf"):
        print(curworkdir + "\\" + sigfilename + ".inf" + "file isn't exist")
        return None
    if not os.path.exists(curworkdir + "\\" + sigfilename + ".sys"):
        print(curworkdir + "\\" + sigfilename + ".sys" + "file isn't exist")
        return None
    makeCmd = genMakeCabCmdLine(sigfilename, curworkdir + "\\" + sigfilename + ".inf", curworkdir + "\\" + sigfilename + ".sys")
    if makeCmd:
        if writeFile(curworkdir + "\\" + sigfilename + ".ddf", makeCmd):
            cabfile = runMakeCabCmdLine(sigfilename)
            if cabfile and os.path.exists(cabfile):
                os.remove(curworkdir + "\\" + sigfilename + ".ddf")
                return cabfile

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
def getLastFolderName(filename):
    index = filename.rfind('\\')
    if index == -1:
        return None
    index2 = filename[:index].rfind('\\')
    if index2 == -1:
        return None
    folderName = filename[index2:index]
    return folderName

def genConfigInfo(filename, isEvSignature):
    sigCfgInfo = '[' + filename + ']' + "\r\n"
    sigCfgInfo += "path=" + "\"" + filename + "\"" + "\r\n"
    if isEvSignature == True:
        sigCfgInfo += "sign_type=" + "\"" + "ev" + "\"" + "\r\n"
    else:
        sigCfgInfo += "sign_type=" + "\"" + "s3,esg" + "\"" + "\r\n"
    return sigCfgInfo


def genConfigFile(filename, writefileData):
    curWork = os.getcwd() + filename
    try:
        cfgfile = open(curWork, "a+")
        cfgfile.write(writefileData)
    except IOError:
        print("read or write file faild")
    else:
        cfgfile.close()
        return len(writefileData)

def genFile(filename):
    curWork = os.getcwd() + filename
    if os.path.exists(curWork):
        return False
    try:
        cfgfile = open(curWork, "w")
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
def getDirectoryAllFiles(inDirectory):
    filelist = []
    if os.path.exists(inDirectory):
        listdir = os.listdir(inDirectory)
        for i in range(len(listdir)):
            curfile = inDirectory + "\\" + listdir[i]
            if os.path.isfile(curfile):
                filelist.append(curfile)
            else:
                filelist.append(curfile)
                subfilelist = getDirectoryAllFiles(curfile)
                for j in range(len(subfilelist)):
                    filelist.append(subfilelist[j])
    return filelist

def cleanOutputDirectory(inDirectory):
    if os.path.exists(inDirectory):
        if os.path.isdir(inDirectory):
            filedirlist = getDirectoryAllFiles(inDirectory)
            filedirlist.reverse()
            for i in range(len(filedirlist)):
                if os.path.isfile(filedirlist[i]):
                    os.remove(filedirlist[i])
                if os.path.isdir(filedirlist[i]):
                    os.rmdir(filedirlist[i])
    return len(filedirlist)
def checkFileIsExist(delayTimes, checkFileName):
    retValue = False
    countTimes = 0
    while True:
        time.sleep(delayTimes)
        countTimes = countTimes + delayTimes
        print("check file: " + checkFileName)
        if os.path.exists(checkFileName):
            retValue = True
            break
        if countTimes >= 3600:
            break
    return retValue

def startFileSignature(sigfilename, fileSuffix):
    curworkdir = os.getcwd()
    #if os.path.exists(g_project_work + "\\" + sigfilename + fileSuffix):
    #    shutil.move(g_project_work + "\\" + sigfilename + fileSuffix, curworkdir + "\\" + sigfilename + fileSuffix)
    sigConfigData = makeSignatureConfigFile(sigfilename + fileSuffix)
    if sigConfigData:
        if os.path.exists(g_local_signature_server_input):
            shutil.copy2(curworkdir + "\\" + sigfilename + fileSuffix, g_local_signature_server_input + "\\" + sigfilename + fileSuffix)
            print("copy file " + sigfilename + fileSuffix +" to signature server")
            genConfigFile(g_local_signature_config_filename, sigConfigData)
            print("gen " + g_local_signature_config_filename + " file success")
            print("clean Output directory files")
            cleanOutputDirectory(g_local_signature_server_output)
            shutil.copy2(curworkdir + g_local_signature_config_filename, g_local_signature_server_input + g_local_signature_config_filename)
            print("copy file " + g_local_signature_config_filename + " to Input directory")
            os.remove(curworkdir + g_local_signature_config_filename)
            if not os.path.exists(curworkdir + g_local_signature_success_filename):
                genFile(g_local_signature_success_filename)      
            shutil.copy2(curworkdir + g_local_signature_success_filename, g_local_signature_server_input + g_local_signature_success_filename)
            print("copy upload.ok file to Input directory") 
            os.remove(curworkdir + g_local_signature_success_filename)
            if checkFileIsExist(10, g_local_signature_server_output + "\\" + sigfilename + fileSuffix):
                shutil.copy2(g_local_signature_server_output + "\\" + sigfilename + fileSuffix, curworkdir + "\\" + sigfilename + fileSuffix)
                print(sigfilename + fileSuffix + " signature success")
                return True
    return False

def genFileSumValue(filename):
    filecrc32 = getFileCrc32(filename)
    if filecrc32:
        print("crc32: " + hex(filecrc32 & 0xffffffff))
    filemd5 = getFileMd5(filename)
    if filemd5:
        print("md5: " + filemd5)
    filesha1 = getFileSha(filename,"sha1")
    if filesha1:
        print("sha1: " + filesha1)
    filesha224 = getFileSha(filename,"sha224")
    if filesha224:
        print("sha224: " + filesha224)
    filesha256 = getFileSha(filename,"sha256")
    if filesha256:
        print("sha256: " + filesha256)
    filesha384 = getFileSha(filename,"sha384")
    if filesha384:
        print("sha384: " + filesha384)
    filesha512 = getFileSha(filename,"sha512")
    if filesha512:
        print("sha512: " + filesha512)

def genCatFile():
    runMakeCat()
def startWork(sigName, isSigSys, isSigCat, isSigCab):
    bret = False
    curDir = os.getcwd()
    listDir = os.listdir(curDir)
    for i in range(0, len(listDir)):
        filename = getFileName(listDir[i])
        tmpFile = curDir + "\\" + filename
        if not os.path.exists(tmpFile + ".inf"):
            print("isn't has inf file")
            break
        if not os.path.exists(tmpFile + ".sys"):
            print("isn't has sys file")
            break
        fileSuffix = getFileSuffix(listDir[i])
        if fileSuffix == "inf":
            infName = getFileName(listDir[i])
            print("inf name: " + infName)
        elif fileSuffix == "sys":
            drvName = getFileName(listDir[i])
            print("drv name: " + drvName)
        else:
            print(listDir[i])
    if infName != drvName:
        print("error: inf name isn't equal drv name")
        return bret
    if isSigSys == True:
        bret = startFileSignature(filename, ".sys")
        if bret == True:
            print("signature Sys file success")
    if isSigCab == True:
        print("make cab file")
        cabfile = genCabFile(filename)
        print("gen " + cabfile)
        if cabfile and os.path.exists(cabfile):
            print("signature cab file")
            bret = startFileSignature(filename, ".cab")
            if bret == True:
                print("signature cab file success")
    if isSigCat == True:   
        genCatFile()
        if os.path.exists(tmpFile + ".cat"):
            bret = startFileSignature(filename, ".cat")
            if bret == True:
                print("signed " + filename + ".cat" + " success")
    return bret                

def isGenSigCatFile():
    binput = input("is gen cat file: ")
    if binput == 'Y' or binput == 'y':
        return True
    else:
        False
def isGenSigCabFile():
    binput = input("is gen cab file: ")
    if binput == 'Y' or binput == 'y':
        return True
    else:
        False
def isSigSysFile():
    binput = input("is gen Sys file: ")
    if binput == 'Y' or binput == 'y':
        return True
    else:
        False 
if __name__ == "__main__":
    print("start work")
    global g_project_work
    global g_inputwork
    global g_userwork
    global g_outputwork
    global g_isSigSys
    global g_isSigCab
    global g_isSigCat
    sigName = ""
    g_project_work = os.getcwd()
    g_inputwork = g_project_work + "\\input\\"
    if not os.path.exists(g_inputwork):
        print("input directory isn't exist")
        exit(0)
    g_userwork = g_project_work + "\\user\\"
    if not os.path.exists(g_userwork):
        os.makedirs(g_userwork)
        print("gen user file folder")
    g_outputwork = g_project_work + "\\output\\"
    if not os.path.exists(g_outputwork):
        os.makedirs(g_outputwork)
        print("gen output file folder")
    if g_isDefault == False:
        try:
            sigName = input("input Signature Name: ")
        except Exception as ex:
            print("sigName is null")
    else:
        sigName = g_DefaultSigName
    listDir = os.listdir(g_userwork)
    for i in range(0, len(listDir)):
        filename = getFileName(listDir[i])
        if not os.path.exists(g_inputwork + filename):
            os.mkdir(g_inputwork + filename)
        filesuffix = getFileSuffix(listDir[i])
        if filename and filesuffix:
            shutil.copy2(g_userwork + listDir[i], g_inputwork + filename + "\\" + sigName + "." + filesuffix)
    if g_isDefault == False:
        g_isSigSys = isSigSysFile()
        g_isSigCab = isGenSigCabFile()
        g_isSigCat = isGenSigCatFile()
    else:
        g_isSigCab = True
    listDir = os.listdir(g_inputwork)
    for i in range(0, len(listDir)):
        filepath = g_inputwork + "\\" + listDir[i]
        if os.path.isdir(filepath):
            os.chdir(filepath)
            startWork(filepath, g_isSigSys, g_isSigCat, g_isSigCab)
    listDir = os.listdir(g_inputwork)
    for i in range (0, len(listDir)):
        folderName = listDir[i]
        subDir = g_inputwork + "\\" + folderName
        sublistDir = os.listdir(subDir)
        for j in range (0, len(sublistDir)):
            subPath = sublistDir[j]
            suffix = getFileSuffix(subPath)
            if suffix == "inf":
                continue
            shutil.copy2(g_inputwork + "\\" + folderName + "\\" + subPath, g_outputwork + "\\" + folderName + "." + suffix)
            print("copy file " + g_inputwork + "\\" + folderName + "\\" + subPath + " to " + g_outputwork + "\\" + folderName + "." + suffix)
    print("work success")


