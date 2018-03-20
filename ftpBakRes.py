import sys
import os
import string
import ftplib

buffer_size = 8192

def entry():
    if (len(sys.argv) < 3):
        sys.exit()
    if (sys.argv[1] == "upload"):
        if (sys.argv[4] == "anonymous" or sys.argv[5] == "anonymous"):
            ftp = connectFTP(sys.argv[2],sys.argv[3],None,None)
        else:
            ftp = connectFTP(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
        if (None == ftp):
            sys.exit()
        filename = os.path.split(sys.argv[6])[-1]
        ret = uploadfiletoftp(ftp,sys.argv[6],filename)
        if (ret == True):
            print('upload file "%s" success' % filename)
    elif (sys.argv[1] == "download"):
        if (sys.argv[4] == "anonymous" or sys.argv[5] == "anonymous"):
            ftp = connectFTP(sys.argv[2],sys.argv[3],None,None)
        else:
            ftp = connectFTP(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
        if (None == ftp):
            sys.exit()
        filename = os.path.split(sys.argv[6])[-1]
        ret = downloadfiletoftp(ftp,filename,sys.argv[6])
        if (ret == True):
            print('download file "%s" success' % filename)        
    else:
        defaultAddress = input("input ftp address")
        if (defaultAddress == None):
            sys.exit()
        defaultPort = input("input ftp port")
        if (defaultPort == None):
            defaultPort = 21
        defaultUser = input("input ftp user")
        defaultPwd = input("input ftp password")
        ftp = connectFTP(defaultAddress,defaultPort,defaultUser,defaultPwd)
        if (None == ftp):
            sys.exit()
        while True:
            selecttype = input('input "upload" or "download" and "quit" terminate program')
            if (selecttype == "upload"):
                filepath = input('input upload file path')
                filename = os.path.split(filepath)[-1]
                ret = uploadfiletoftp(ftp,filepath,filename)
                if (ret == True):
                    print('upload file "%s" success' % filename)                
            elif (selecttype == "download"):
                filepath = input('input download file path')
                filename = os.path.split(filepath)[-1]
                ret = downloadfiletoftp(ftp,filename,filepath)
                if (ret == True):
                    print('download file "%s" success' % filename)                
            elif (selecttype == "quit"):
                break
            else:
                print("again input")
            break
    disconnectFTP(ftp)

def disconnectFTP(ftp):
    ftp.quit()

def connectFTP(ftpAddress,ftpPort,ftpUser,ftpPwd):
    if (ftpAddress == None):
        return None
    ftp = ftplib.FTP()
    ftp.set_debuglevel(2)
    try:
        ftp.connect(ftpAddress,ftpPort)
        ftp.login(ftpUser,ftpPwd)
        return ftp
    except (socket.error,socket.gaierror):
        print("connect failed")
    return None

def uploadfiletoftp(ftp,filepath,filename):
    if (filename == None):
        return False
    if (os.path.exists(filepath) == False):
        return False
    fp = open(filepath,"rb")
    #filename = os.path.split(filepath)[-1]
    if (findFTPfile(ftp,filename)):
        ftp.delete(filename)
    try:
        ftp.storbinary('STOR %s'%filename,fp,buffer_size)
        print('upload file "%s" success' % filename)
    except ftplib.error_perm:
        return False
    return True

def downloadfiletoftp(ftp,filename,savefilepath):
    if (savefilepath == None):
        return False
    if (os.path.exists(savefilepath)):
        os.unlink(savefilepath)  
    fp = open(savefilepath,"wb").write
    try:
        ftp.retrbinary("RETR %s"%filename,fp,buffer_size)
        print('download file "%s" success' % filename)
    except ftplib.error_perm:
        return False
    return True

def findFTPfile(ftp,filename):
    ftpfilelist = ftp.nlst()
    if (filename in ftpfilelist):
        return True
    else:
        return False

if __name__ == "__main__":
    entry()