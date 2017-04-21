import psutil

def checkP(pid,pname):
    try:
        p = psutil.Process(pid)
        print ap.name()
    except psutil.NoSuchProcess , a:
        print 'error',a