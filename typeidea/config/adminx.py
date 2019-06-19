import xadmin
from django.contrib import admin
from .models import Link, SideBar


# Register your models here.


# @admin.register(Link)
@xadmin.sites.register(Link)
class LinkAdmin:
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')

    def save_model(self):
        # obj.owner = request.user
        self.new_obj.owner = self.request.user
        # return super(LinkAdmin, self).save_model(request, obj, form, change)
        return super().save_model()

# @admin.register(SideBar)
@xadmin.sites.register(SideBar)
class SideBarAdmin:
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')

    def save_model(self):
        # obj.owner = request.user
        # return super(SideBarAdmin, self).save_model(request, obj, form, change)
        self.new_obj.owner = self.request.user
        # return super(LinkAdmin, self).save_model(request, obj, form, change)
        return super().save_model()
