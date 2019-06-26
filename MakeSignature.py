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


class SignatureFileInfo:
     def __init__(self):
          self.filename = ""
          self.output = ""
          self.md5sum = ""
          self.signature_md5sum = ""


def getFileNameFromFullPath(fullpath):
    index = str(fullpath).rfind('\\')
    if index == -1:
        return fullpath
    return fullpath[index + 1:]


def getFileVersion(filename):
    if not os.path.isfile(filename):
        return
    mype = pefile.PE(filename)
    fileversion = ""
    productversion = ""

    if hasattr(mype, 'VS_VERSIONINFO'):
        if hasattr(mype, 'FileInfo'):
            for entry in mype.FileInfo:
                if hasattr(entry, 'StringTable'):
                    for st in entry.StringTable:
                        for k, v in st.entries.items():
                            if k == u"FileVersion":
                                fileversion = v
                            elif k == u"ProductVersion":
                                productversion = v
    if not fileversion:
        fileversion = None
    if not productversion:
        productversion = None
    return (fileversion, productversion)


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
     f = file(filename,'rb')
     while True:
          b = f.read(4096)
          if not b:
               break
          myhash.update(b)
     f.close()
     return myhash.hexdigest()


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
    writeLength = 0
    curWork = os.getcwd() + filename
    try:
        cfgfile = open(curWork, "ab+")
        writeLength = cfgfile.write(writefileData)
    except IOError:
        print("read or write file faild")
    else:
        cfgfile.close()
    return writeLength


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


def getSignatureFileList(argc, argv):
    filelist = []
    sigfileinfo = SignatureFileInfo()
    for i in range(argc):
        indexo = str(argv[i]).find("-o ")
        if indexo == -1:
            continue
        indexf = str(argv[i]).find(" -f ")
        sigfileinfo.output = str(argv[i])[indexo + len("-o "):indexf]
        sigfileinfo.filename = str(argv[i])[indexf + len(" -f "):]
        # filelist.append(str(argv[i])[indexo + len("-o "):indexf])
        # filelist.append(str(argv[i])[indexf + len(" -f "):])
        filelist.append(sigfileinfo)
    return filelist


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

def saveOrigalFileAndPdb(filename, savepath):
     if not os.path.exists(savepath):
          os.makedirs(savepath)
     if os.path.exists(filename):
          shutil.copy2(filename, savepath)
          print("save origal file success")
     index = filename.rfind('.')
     pdbfile = filename[:index + 1] + "pdb"
     if os.path.exists(pdbfile):
          shutil.copy2(pdbfile, savepath)
          print("save origal pdb file success")

if __name__ == "__main__":
    sigCfgList = []
    sigFileNameList = []
    sigFileList = getSignatureFileList(len(sys.argv), sys.argv)
    for i in range(len(sigFileList)):
        if not os.path.exists(sigFileList[i].filename):
            print("file " + sigFileList[i].filename + "isn't exist")
            continue
        filename = getFileNameFromFullPath(sigFileList[i].filename)
        if filename == None:
            continue
        sigFileNameList.append(filename)
        print("make signature config file")
        sigConfigData = makeSignatureConfigFile(filename)
        if sigConfigData != None:
            print(sigConfigData)
            sigCfgList.append(sigConfigData)
        saveOrigalFileAndPdb(sigFileList[i].filename, sigFileList[i].output + "\\origal")
        if os.path.exists(g_local_signature_server_input):
            shutil.copy2(sigFileList[i].filename, g_local_signature_server_input + "\\" + filename)
    curWorkDirectory = os.getcwd()
    print(curWorkDirectory)     
    for i in range(len(sigCfgList)):
        genConfigFile(g_local_signature_config_filename, sigCfgList[i])
    print("clean Output directory files")
    cleanOutputDirectory(g_local_signature_server_output)
    print("copy file to Input directory")
    shutil.copy2(curWorkDirectory + g_local_signature_config_filename, g_local_signature_server_input + g_local_signature_config_filename)
    os.remove(curWorkDirectory + g_local_signature_config_filename)
    if not os.path.exists(curWorkDirectory + g_local_signature_success_filename):
        genFile(g_local_signature_success_filename)
    print("copy upload.ok file to Input directory")
    shutil.copy2(curWorkDirectory + g_local_signature_success_filename, g_local_signature_server_input + g_local_signature_success_filename)
    os.remove(curWorkDirectory + g_local_signature_success_filename)
    for i in range(len(sigFileNameList)):
         if checkFileIsExist(10, g_local_signature_server_output + "\\" + sigFileNameList[i]):
              if not os.path.exists(sigFileList[i].output):
                   try:
                        os.makedirs(sigFileList[i].output)
                   except IOError:
                        print("directory exist")
                   else:
                        print("directory create success")
              shutil.copy2(g_local_signature_server_output + "\\" + sigFileNameList[i], sigFileList[i].output + "\\" + sigFileNameList[i])
              print(sigFileNameList[i] + " signature success")
              filecrc32 = getFileCrc32(sigFileList[i].output + "\\" + sigFileNameList[i])
              if filecrc32:
                   print("crc32: " + hex(filecrc32 & 0xffffffffL))
              filemd5 = getFileMd5(sigFileList[i].output + "\\" + sigFileNameList[i])
              if filemd5:
                   print("md5: " + filemd5)
              filesha1 = getFileSha(sigFileList[i].output + "\\" + sigFileNameList[i],"sha1")
              if filesha1:
                   print("sha1: " + filesha1)
              filesha224 = getFileSha(sigFileList[i].output + "\\" + sigFileNameList[i],"sha224")
              if filesha224:
                   print("sha224: " + filesha224)
              filesha256 = getFileSha(sigFileList[i].output + "\\" + sigFileNameList[i],"sha256")
              if filesha256:
                   print("sha256: " + filesha256)
              filesha384 = getFileSha(sigFileList[i].output + "\\" + sigFileNameList[i],"sha384")
              if filesha384:
                   print("sha384: " + filesha384)
              filesha512 = getFileSha(sigFileList[i].output + "\\" + sigFileNameList[i],"sha512")
              if filesha512:
                   print("sha512: " + filesha512)

