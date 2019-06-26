import sys
import datetime
import shutil
import hashlib
import zlib
import os
import pefile

#parameter 1: need operate's file of abs path and has suffix
#parameter 1: save file path

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
def needCopyFile(absfilename, destfilepath, needfilename):
    if os.path.exists(absfilename):
        shutil.copy2(absfilename, destfilepath + "\\" + needfilename)
        print("copy" + absfilename + " to " + destfilepath + "\\" + needfilename)
def entry():
    if len(sys.argv) == 3:
        if not os.path.exists(sys.argv[1]):
            return
        needCopyFile(sys.argv[1], sys.argv[2], "360entbw_x64_6.0.sys")
        needCopyFile(sys.argv[1], sys.argv[2], "360entbw_x64_6.1.sys")
        needCopyFile(sys.argv[1], sys.argv[2], "360entbw_x64_6.2.sys")
        needCopyFile(sys.argv[1], sys.argv[2], "360entbw_x64_6.3.sys")
        fileversion = getFileVersion(sys.argv[1])
        now = datetime.datetime.now()
        index = sys.argv[1].rfind('.')
        suffix = str(sys.argv[1])[index:]
        timename = now.strftime('%Y-%m-%d-%H-%M-%S')
        if suffix in (".sys", ".Sys", ".SYS"):
            pdbpath = str(sys.argv[1])[0:index] + ".pdb"
            if os.path.isfile(pdbpath):
                newpdb = sys.argv[2] + timename + ".pdb"
                shutil.copy2(pdbpath, newpdb)
                print("new pdb: " + newpdb)
                if os.path.exists(r"D:\VMwareMachine\Windows7X86-LocalSym"):
                    shutil.copy2(pdbpath, r"D:\VMwareMachine\Windows7X86-LocalSym")
                    print("copy pdb to windows 7 x86 symbols path")
                if os.path.exists(r"D:\VMwareMachine\Windows7X86-LocalSym"):
                    shutil.copy2(pdbpath, r"D:\VMwareMachine\Windows7X64-LocalSym")
                    print("copy pdb to windows 7 x64 symbols path")
                if os.path.exists(r"D:\VMwareMachine\Windows8X86-LocalSym"):
                    shutil.copy2(pdbpath, r"D:\VMwareMachine\Windows8X86-LocalSym")
                    print("copy pdb to windows 8 x86 symbols path")
                if os.path.exists(r"D:\VMwareMachine\Windows8X64-LocalSym"):
                    shutil.copy2(pdbpath, r"D:\VMwareMachine\Windows8X64-LocalSym")
                    print("copy pdb to windows 8 x64 symbols path")
                if os.path.exists(r"D:\VMwareMachine\Windows8.1X86-LocalSym"):
                    shutil.copy2(pdbpath, r"D:\VMwareMachine\Windows8.1X86-LocalSym")
                    print("copy pdb to windows 8.1 x86 symbols path")
                if os.path.exists(r"D:\VMwareMachine\Windows8.1X64-LocalSym"):
                    shutil.copy2(pdbpath, r"D:\VMwareMachine\Windows8.1X64-LocalSym")
                    print("copy pdb to windows 8.1 x64 symbols path")
                if os.path.exists(r"D:\VMwareMachine\Windows10X86-LocalSym"):
                    shutil.copy2(pdbpath, r"D:\VMwareMachine\Windows10X86-LocalSym")
                    print("copy pdb to windows 10 x86 symbols path")
                if os.path.exists(r"D:\VMwareMachine\Windows10X64-LocalSym"):
                    shutil.copy2(pdbpath, r"D:\VMwareMachine\Windows10X64-LocalSym")
                    print("copy pdb to windows 10 x64 symbols path")
        newFile = sys.argv[2] + timename + suffix
        shutil.copy2(sys.argv[1], newFile)
        print(sys.argv[1] + " copy " + newFile)
        filecrc32 = getFileCrc32(newFile)
        if filecrc32:
            print("crc32: " + hex(filecrc32 & 0xffffffffL))
        filemd5 = getFileMd5(newFile)
        if filemd5:
            print("md5: " + filemd5)
        filesha1 = getFileSha(newFile,"sha1")
        if filesha1:
            print("sha1: " + filesha1)
        filesha224 = getFileSha(newFile,"sha224")
        if filesha224:
            print("sha224: " + filesha224)
        filesha256 = getFileSha(newFile,"sha256")
        if filesha256:
            print("sha256: " + filesha256)
        filesha384 = getFileSha(newFile,"sha384")
        if filesha384:
            print("sha384: " + filesha384)
        filesha512 = getFileSha(newFile,"sha512")
        if filesha512:
            print("sha512: " + filesha512)         
if __name__ == "__main__":
    entry()
