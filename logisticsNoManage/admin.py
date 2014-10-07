#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from logisticsNoManage.models import billStatus,logistics


class billStatusAdmin(admin.ModelAdmin):
    pass

class logisticsAdmin(admin.ModelAdmin):
    pass
	

admin.site.register(billStatus, billStatusAdmin)
admin.site.register(logistics, logisticsAdmin)