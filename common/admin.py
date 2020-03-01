from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Factory, FactoryFilter, Alias

# Register your models here.


class FacroryAliasAdmin(admin.TabularInline):
    model = Alias
    fields = ('property', )


class FacroryFilterAdmin(admin.TabularInline):
    model = FactoryFilter
    fields = ('property', 'entity')


class FactoryAdmin(admin.ModelAdmin):
    fields = ('category_name', 'language')
    inlines = (FacroryAliasAdmin, FacroryFilterAdmin)


admin.site.register(User, UserAdmin)
admin.site.register(Factory, FactoryAdmin)