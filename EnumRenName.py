import os
import sys
import shutil

def EnumDirectory(directory,copypath):
    count = 0
    print("Start scan Directory " + "\"" + directory + "\"")
    if os.path.isdir(directory):
        listdir = os.listdir(directory)
        for filedir in listdir:
            filepath = os.path.join(directory,filedir)
            if os.path.isfile(filepath):
                newfile = filepath[filepath.rfind("\\"):]
                destfile = copypath + newfile[:len(newfile) - 4] + ".exe"
                if newfile[len(newfile) - 4:len(newfile)] != ".i64":
                    shutil.copy(filepath,destfile)
                    count = count + 1
                    print ("count:%08x copy %s -> %s", count, filepath, destfile)
                    
                    
def backDirectory(directory,copypath):
    count = 0
    print("Start scan Directory " + "\"" + directory + "\"")
    if os.path.isdir(directory):
        listdir = os.listdir(directory)
        for filedir in listdir:
            filepath = os.path.join(directory,filedir)
            if os.path.isfile(filepath):
                newfile = filepath[filepath.rfind("\\"):]
                destfile = copypath + newfile[:len(newfile) - 4] + ".efi"
                if newfile[len(newfile) - 4:len(newfile)] != ".i64":
                    shutil.copy(filepath,destfile)
                    count = count + 1
                    print (count, filepath, destfile)
                    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit()
    if os.path.exists(sys.argv[1]):
        backDirectory(sys.argv[1],sys.argv[2])
    #if os.path.exists(sys.argv[1]):
    #    EnumDirectory(sys.argv[1],sys.argv[2])
    else:
        print("Path" + "\"" + sys.argv[1] + "\"" + "isn't Directory")