from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import EditAccountForm

#Nao sugerida pelo curso mas necessária
#Pois o Date_joined deve ser somente leitura
#para a página do Admin funcionar
class MyUserAdmin(UserAdmin): 
    
    # adiciona um segundo Personal Info
    # fieldsets = UserAdmin.fieldsets + (('Personal info', {'fields': ('name',)}),)

    # x=UserAdmin.fieldsets
    # x[1][1]['fields'] = x[1][1]['fields']+('name',)    
    # fieldsets = x
    
    readonly_fields = ["date_joined"]


#admin.site.register(User, UserAdmin)
admin.site.register(User, MyUserAdmin)
