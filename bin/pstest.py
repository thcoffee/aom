import psutil,os
try:
    p = psutil.Process(16732)
    print os.path.join(p.cwd(),p.name()),os.path.realpath(__file__)
except psutil.NoSuchProcess , a:
    print 'error',a