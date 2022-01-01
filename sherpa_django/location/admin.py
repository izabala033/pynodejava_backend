from django.contrib import admin

from location.models import SherpaUser, Location

class SherpaUserAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id','name','cp','city')

admin.site.register(SherpaUser, SherpaUserAdmin)
admin.site.register(Location, LocationAdmin)
