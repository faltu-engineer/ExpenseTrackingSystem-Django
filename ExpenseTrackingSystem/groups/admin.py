from django.contrib import admin
from groups.models import Profile, Wallet, Group, GroupMember
# Register your models here.
admin.site.register(Profile)
admin.site.register(Wallet)
admin.site.register(Group)
admin.site.register(GroupMember)