from functions import config
import os
a=config.configObject()
print(os.path.split(os.path.realpath(__file__)))
print(a.getConf())