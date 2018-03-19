import sys
import os
import string

def entry():
    if (len(sys.argv) < 3):
        exit()
    if (sys.argv[1] == "export"):
        exportSvnBak(sys.argv[2],sys.argv[3])
    elif (sys.argv[1] == "import"):
        if (sys.argv[2] == "all"):
            importAllBak(sys.argv[3],sys.argv[4])
        else:
            importSvnBak(sys.argv[2],sys.argv[3])
    else:
        print("exit()")
def importAllBak(svnRepositoriesPath,svnBakPath):
    if (os.path.exists(svnRepositoriesPath) == False):
        print("Repositories path isn't exist.")
    if (os.path.exists(svnBakPath) == False):
        print("Svn bak path isn't exist.")
    allDir = os.listdir(svnBakPath)
    for svnLibName in allDir:
        nOffsetIndex = svnLibName.find(".")
        if (nOffsetIndex):
            newSvnRepositoriesPath = svnRepositoriesPath + "\\" + svnLibName[0:nOffsetIndex]
            if (os.path.exists(newSvnRepositoriesPath) == False):
                continue            
            newSvnBakPath = svnBakPath + "\\" + svnLibName
            if (os.path.exists(newSvnBakPath) == False):
                continue
            command = "svnadmin" + " " + "load" + " " + newSvnRepositoriesPath + " < " + newSvnBakPath
            print(command)
            os.system(command)
def importSvnBak(svnRepositoriesPath,svnBakPath):
    if (os.path.exists(svnRepositoriesPath) == False):
        print("Repositories path isn't exist.")
    if (os.path.exists(svnBakPath) == False):
        print("Svn bak path isn't exist.")
    command = "svnadmin" + " " + "load" + " " + svnRepositoriesPath + " < " + svnBakPath
    print(command)
    os.system(command)
def exportSvnBak(svnRepositoriesPath,svnBakPath):
    if (os.path.exists(svnRepositoriesPath) == False):
        print("Repositories path isn't exist.")
    if (os.path.exists(svnBakPath) == False):
        print("Svn bak path isn't exist.")
    listdir = os.listdir(svnRepositoriesPath)
    for svnLibName in listdir:
        newLibName = svnRepositoriesPath + '\\' + svnLibName
        if (os.path.exists(newLibName) == False):
            continue
        newBakName = svnBakPath + '\\' + svnLibName + ".SVN.Bak"
        if (os.path.isdir(newLibName)):
            command = "svnadmin" + " " + "dump" + " " + newLibName + " > " + newBakName
            print(command)
            os.system(command)
        else:
            print("is file")
if __name__ == "__main__":
    entry()