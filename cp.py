import salt.client
import yaml
client=salt.client.LocalClient()
#a=client.cmd('test207','cp.get_dir',['salt://adcc/app','/root'])
#a=client.cmd('test254','disk.usage')
#print(a,type(a))
#for i in a['test207']:
#    print(a['test207'][i])

#a=client.cmd('test207','appserver.getpid',['nihaoa'])
#a=client.cmd_async('test207','appserver.getpid',['piterchen'])
#a=client.get_cache_returns('20170228160345940577')
#a=client.cmd('test207','state.sls',['sfile.test'])
#print yaml.dump(a,default_flow_style=False)        
a=client.cmd('test207','test.ping')
print a
