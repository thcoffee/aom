from django.contrib import admin

# Register your models here.

from .models import AomCustom
from .models import AomProject
from .models import AomApp
from .models import AomAppSt
from .models import AomEnvironment
from .models import AomNode


class AomAppStAdmin(admin.StackedInline):
    model = AomAppSt
    #max_num = 1
    
class AomAppAdmin(admin.ModelAdmin):
    inlines = [AomAppStAdmin]

admin.site.register(AomCustom)
admin.site.register(AomProject)
admin.site.register(AomApp,AomAppAdmin)
admin.site.register(AomEnvironment)
admin.site.register(AomNode)