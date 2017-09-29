from jinja2 import Template 
with open('/home/deployuser/aom/templates/tomcat/server.xml','r') as myfile:
    template = Template(myfile.read()) 
    print(template.render({'httpport':80,
                           'shutdownport':8005,
                           'ajpport':8009,
                           'appbase':'/home/deployuser/adcc/software/tomcat/webapps',
                           'app':[],
                          })) 