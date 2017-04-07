import salt.utils.event
event = salt.utils.event.MasterEvent('/var/run/salt/master')
print 'waiting'
for data in event.iter_events(full=True):
    print data,type(data),data['data'].has_key('jid')
    if data['data'].has_key('jid'):
        print data['data'].has_key('return')
        if data['data']['jid']=='20170301134852766778' and data['data'].has_key('return'):
            print 'huilaile',data['data']['return']
            
    print '------'
