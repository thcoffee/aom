import salt.client
import yaml
import time
client=salt.client.LocalClient()
#a=client.cmd('test207','test.test')
#a=client.cmd_async('test207','appserver.getpid',['piterchen'])
#a=client.get_cache_returns('20170228160345940577')
#a=client.cmd('test207','state.sls',['sfile.nginx'])
#b={'tgt':['test207','test208','test254'],'fun':'cmd.run','arg':['sleep 10&&ls -l'],'expr_form':'list'}
b={'tgt':['test208','test207','test254'],'fun':'appserver.getdate','expr_form':'list','batch':'80%',}
#b={'tgt':'test207','fun':'state.sls','arg':['sfile.test1','ls -l']}
#b={'tgt':'*','fun':'appserver.zu','arg':[{'name':'tom'}]}
#b={'tgt':'*','fun':'cmd.run','arg':['sleep 10&&ls -l'],'timeout':5}
#b={'tgt':'*','fun':'appserver.zu','kwarg':{'name':'zu'}}
a=client.cmd(**b)
#a=client.cmd_batch(**b)
#c=client.cmd_async(**b)
#while 1:
#    print c
#    a=client.get_cache_returns(c)
#    print yaml.dump(a,default_flow_style=False)
#    time.sleep(2)
print yaml.dump(a,default_flow_style=False) 
#for i in a:
#    print 'neirong:',yaml.dump(i,default_flow_style=False)
