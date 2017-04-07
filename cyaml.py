import yaml
a={'testcmd':{'cmd.run':[{'cwd':'/root'},{'names':['ls -l']}]}}
print yaml.dump(a,default_flow_style=False)
with open('/srv/salt/sfile/test.sls','w') as myfile:
    myfile.write(yaml.dump(a,default_flow_style=False))
