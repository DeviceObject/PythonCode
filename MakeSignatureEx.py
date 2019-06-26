import sys
import datetime
import shutil
import hashlib
import zlib
import os
import pefile
import time
import commands

g_local_signature_server_input = "\\\\10.95.158.254\\input\\wanghui02"
g_local_signature_server_output = "\\\\10.95.48.22\\Sign\\wanghui02"
g_local_signature_config_filename = "\\sign_config.ini"
g_local_signature_success_filename = "\\upload.ok"
g_local_signature_filename = []

g_project_work = ""
g_inputwork = ""
g_cachework = ""
g_outputwork = ""


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
    f = file(filename,'rb')
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
    f = file(filename,'rb')
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
    f = file(filename, 'rb')
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
def runMakeCabCmdLine(ddfname):
    runCmdLine = "makecab.exe /f " + ddfname + ".ddf"
    curwork = os.getcwd()
    showinfo = os.system(runCmdLine)
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
    writelength = 0
    if os.path.exists(filename):
        os.remove(filename)
    try:
        cfgfile = open(filename, "wb+")
        cfgfile.write(writedat)
    except IOError:
        print("file is exist or write faild")
    else:
        cfgfile.close()
        return len(writedat)
def genCabFile(sigfilename):
    curworkdir = os.getcwd()
    if not os.path.exists(curworkdir + "\\" + sigfilename + ".inf"):
        print curworkdir + "\\" + sigfilename + ".inf" + "file isn't exist"
        return None
    if not os.path.exists(curworkdir + "\\" + sigfilename + ".sys"):
        print curworkdir + "\\" + sigfilename + ".sys" + "file isn't exist"
        return None
    makeCmd = genMakeCabCmdLine(sigfilename, curworkdir + "\\" + sigfilename + ".inf", curworkdir + "\\" + sigfilename + ".sys")
    if makeCmd:
        if writeFile(curworkdir + "\\" + sigfilename + ".ddf", makeCmd):
            cabfile = runMakeCabCmdLine(sigfilename)
            if cabfile:
                shutil.move(cabfile, g_project_work + "\\" + sigfilename + ".cab")
                return g_project_work + "\\" + sigfilename + ".cab"

def getFileSuffix(filename):
    index = filename.rfind('.')
    if index == -1:
        return None
    suffix = filename[index + 1:]
    return suffix


def genConfigInfo(filename, isEvSignature):
    sigCfgInfo = '[' + filename + ']' + "\r\n"
    sigCfgInfo += "path=" + "\"" + filename + "\"" + "\r\n"
    if isEvSignature == True:
        sigCfgInfo += "sign_type=" + "\"" + "360ev" + "\"" + "\r\n"
    else:
        sigCfgInfo += "sign_type=" + "\"" + "360,360s3,360esg" + "\"" + "\r\n"
    return sigCfgInfo


def genConfigFile(filename, writefileData):
    curWork = os.getcwd() + filename
    try:
        cfgfile = open(curWork, "ab+")
        writeLength = cfgfile.write(writefileData)
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

def startFileSignature(sigfilename):
    curworkdir = os.getcwd()
    if os.path.exists(g_project_work + "\\" + sigfilename + ".cab"):
        shutil.move(g_project_work + "\\" + sigfilename + ".cab", curworkdir + "\\" + sigfilename + ".cab")
    sigConfigData = makeSignatureConfigFile(sigfilename + ".cab")
    if sigConfigData:
        if os.path.exists(g_local_signature_server_input):
            shutil.copy2(curworkdir + "\\" + sigfilename + ".cab", g_local_signature_server_input + "\\" + sigfilename + ".cab")
            print "copy file " + sigfilename + ".cab" +" to signature server"
            genConfigFile(g_local_signature_config_filename, sigConfigData)
            print "gen " + g_local_signature_config_filename + " file success"
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
            if checkFileIsExist(10, g_local_signature_server_output + "\\" + sigfilename + ".cab"):
                shutil.copy2(g_local_signature_server_output + "\\" + sigfilename + ".cab", g_outputwork + "\\" + sigfilename + ".cab")
                print(sigfilename + ".cab" + " signature success")
                return True
    return False

def genFileSumValue(filename):
    filecrc32 = getFileCrc32(filename)
    if filecrc32:
        print("crc32: " + hex(filecrc32 & 0xffffffffL))
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
    
if __name__ == "__main__":
    print "start work"
    g_project_work = os.getcwd()
    g_inputwork = g_project_work + "\\input\\"
    if not os.path.exists(g_inputwork):
        print "input directory isn't exist"
        exit(0)
    g_cachework = g_project_work + "\\cache\\"
    if not os.path.exists(g_cachework):
        os.makedirs(g_cachework)
        print "gen cache file folder"
    g_outputwork = g_project_work + "\\output\\"
    if not os.path.exists(g_outputwork):
        os.makedirs(g_outputwork)
        print "gen output file folder"
    for i in range(1, len(sys.argv)):
        os.chdir(g_inputwork)
        print "make cab file"
        cabfile = genCabFile(sys.argv[i])
        print "gen " + cabfile     
        os.chdir(g_project_work)         
        if cabfile:
            os.chdir(g_cachework)
            print "signature cab file"
            success = startFileSignature(sys.argv[i])
            os.chdir(g_project_work)                   
            if success == True:
                print "signature success"
                os.remove(g_cachework + sys.argv[i] + ".cab")
                genFileSumValue(g_outputwork + sys.argv[i] + ".cab")


