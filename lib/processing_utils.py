import multiprocessing
import sys

def beep():
    print('\007')

def getThreadCount(target=-1):
    cpuCount = multiprocessing.cpu_count()
    threads = min(target, cpuCount) if target > 0 else cpuCount
    return threads

def printCommand(command):
    pcommand = command[:]
    for i, p in enumerate(pcommand):
        if i > 1:
            if not p.startswith("-"):
                pcommand[i] = '"'+p+'"'
    print(" ".join(pcommand))

def printProgress(step, total, prepend=""):
    sys.stdout.write('\r')
    sys.stdout.write("%s%s%%" % (prepend, round(1.0*step/total*100,2)))
    sys.stdout.flush()
