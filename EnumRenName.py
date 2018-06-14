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
                    
def scanFiles(directory):
    for root, xdirectory, paths in os.walk(directory):
        for path in paths:
            filename, filesuffix = os.path.splitext(path)
            print(filename, filesuffix)
def copyfilestodirectory(filepath, directory):
    countentries = 0;
    if os.path.exists(directory) == False:
        print(directory + " isn't exist")
        os.makedirs(directory)
        print("create directory " + directory)
    if os.path.isdir(filepath):
        for root, xdirectory, paths in os.walk(filepath):
            for path in paths:
                filename, filesuffix = os.path.splitext(path)
                sourcefile = root + "\\" + path;
                destfile = directory + "\\" + path
                if os.access(sourcefile, os.R_OK):
                    print(countentries, sourcefile, destfile)   
                    shutil.copy(sourcefile, destfile)
                    countentries = countentries + 1
                else:
                    print(sourcefile + " isn't access")
    else:
        print(filepath + "isn't a directory")
if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit()
    #if os.path.exists(sys.argv[1]):
    #    backDirectory(sys.argv[1],sys.argv[2])
    #if os.path.exists(sys.argv[1]):
    #    EnumDirectory(sys.argv[1],sys.argv[2])
    #scanFiles(sys.argv[1])
    copyfilestodirectory(sys.argv[1],sys.argv[2])
    #else:
    #   print("Path" + "\"" + sys.argv[1] + "\"" + "isn't Directory")