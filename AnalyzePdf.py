import sys
import os

def analyzeCommand(argc, argv):
    if argc < 3:
        return None
    if not os.path.exists(argv[2]):
        return None
    if not os.path.isfile(argv[2]):
        return None
    return argv[2]
if __name__ == "__main":
    inputfile = analyzeCommand(len(sys.argv), sys.argv)
    if inputfile == None:
        print("isn't has input file")
    