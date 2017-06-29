import sys
import datetime
import shutil

def entry():
    if len(sys.argv) == 2:
        now = datetime.datetime.now()
        newFile = now.strftime('%Y-%m-%d-%H-%M-%S.Exe')
        shutil.move(sys.argv[1],newFile)
        print(sys.argv[1] + " rename " + newFile)
if __name__ == "__main__":
    entry()