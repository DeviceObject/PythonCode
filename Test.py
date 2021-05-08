import struct
import binascii
import array
import os
import time

def entry():
    curTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print(curTime)
    #pieceInfectVbrFile("C:\\BuildServer\\Bin\\InfectVbr.exe","C:\\BuildServer\\InfectVbr\\VbrBootShlDrv.Bin",8192,"xVbrCode")
    pieceInfectFile("C:\\BuildServer\\Bin\\InfectMbr.exe","C:\BuildServer\InfectMbr\MbrLdr.Bin",1024,"xMbrLdr")
    pieceInfectFile("C:\\BuildServer\\Bin\\InfectMbr.exe","C:\BuildServer\InfectMbr\MbrCore.Bin",12288,"xMbrCore")

def pieceInfectFile(InfectFile,subFile,codeSize,signatureCode):
    if (os.path.exists(InfectFile) == False or \
        os.path.exists(subFile) == False):
        return False
    if (os.access(InfectFile,os.R_OK) == False or \
        os.access(subFile,os.R_OK) == False):
        return False
    infectFileSize = os.path.getsize(InfectFile)
    subFileSize = os.path.getsize(subFile)
    if (infectFileSize < codeSize or subFileSize > codeSize):
        return False
    fpSubFile = open(subFile,'rb')
    subFileDat = fpSubFile.read(subFileSize)
    fpSubFile.close()
    fpInfect = open(InfectFile,'rb')
    infectFileDat = fpInfect.read()
    searchDat = bytearray(infectFileDat)
    infectIndex = searchDat.index(signatureCode)
    newInfectDat = searchDat[0:infectIndex] + subFileDat + searchDat[(infectIndex + subFileSize):]
    fpInfect = open(InfectFile,'wb')
    fpInfect.write(newInfectDat)
    fpInfect.close()
    return True
    
if __name__ == "__main__":
    entry()