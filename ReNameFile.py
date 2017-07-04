import sys
import datetime
import shutil

def entry():
    if len(sys.argv) == 3:
        now = datetime.datetime.now()
        newFile = now.strftime('%Y-%m-%d-%H-%M-%S.Exe')
        shutil.move(sys.argv[1],sys.argv[2] + '\\' + newFile)
        print(sys.argv[1] + " rename " + newFile)
if __name__ == "__main__":
    entry()
