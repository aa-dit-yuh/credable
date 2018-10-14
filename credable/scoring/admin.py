# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import LoanApplication, Vouching


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Vouching)
class VouchingAdmin(admin.ModelAdmin):
    pass
