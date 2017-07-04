import os
import sys
import struct

def CheckSuffix(FileName,Suffix):
    if FileName == 0:
        return 0
    NameSuffix = os.path.splitext(FileName)
    if NameSuffix[1] == Suffix:
        print(FileName + " suffix " + "<" + NameSuffix[1] + ">")
        return True
    else:
        print(FileName + " suffix " + "<" +NameSuffix[1] + ">")
        return False
def SearchStringFromFile(FilePath,String,Index):
    searchfile = open(FilePath,'rb')
    filedat = searchfile.read()
    ret = filedat.find("PyldBioz",0)
    if ret != -1:
        searchfile.close()
        return True
    else:
        searchfile.close()
        return False
def EnumDirectory(Directory):
    print("Start scan Directory " + "\"" + Directory + "\"")
    if os.path.isdir(Directory):
        listdir = os.listdir(Directory)
        for filedir in listdir:
            filepath = os.path.join(Directory,filedir)
            if os.path.isdir(filepath):
                EnumDirectory(filepath)
            else:
                bIsExe = CheckSuffix(filedir.lower(),".exe")
                if bIsExe == True:
                    abspath = os.path.join(Directory,filedir)
                    if os.access(abspath,os.R_OK):
                        print("Analyze " + filedir)
                        if SearchStringFromFile(abspath,"PyldBioz",0) == True:
                            print(filedir + " Find BIOSUpdate Proramfile")
                    else:
                        print("Analyze " + filedir + " no access")
    else:
        print("Isn't Directory " + "\"" + Directory + "\"")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit()
    if os.path.exists(sys.argv[1]):
        EnumDirectory(sys.argv[1])
    else:
        print("Path" + "\"" + sys.argv[1] + "\"" + "isn't Directory")