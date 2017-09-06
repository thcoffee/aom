from django.contrib import admin

# Register your models here.

from .models import AomCustom
from .models import AomProject
from .models import AomApp
from .models import AomAppSt
from .models import AomEnvironment
from .models import AomNode
from .models import AomOs
from .models import AomAppserverType
from .models import AomAppserver
from .models import AomAppserverTomcat
from .models import AomApp2Jvm
from .models import AomNginx

class AomAppStAdmin(admin.StackedInline):
    model = AomAppSt
    #max_num = 1
    
class AomAppAdmin(admin.ModelAdmin):
    inlines = [AomAppStAdmin]
    
class AomAppserverTomcatAdmin(admin.StackedInline):
    model =  AomAppserverTomcat

class AomAppserverAdmin(admin.ModelAdmin):
    inlines = [AomAppserverTomcatAdmin]
    

admin.site.register(AomCustom)
admin.site.register(AomProject)

admin.site.register(AomApp,AomAppAdmin)

admin.site.register(AomEnvironment)
admin.site.register(AomNode)
admin.site.register(AomOs)
admin.site.register(AomAppserverType)
admin.site.register(AomAppserver,AomAppserverAdmin)
admin.site.register(AomApp2Jvm)
admin.site.register(AomNginx)