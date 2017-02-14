from django.contrib import admin
from .models import CutURL


class CutURLManager(admin.ModelAdmin):
    list_display = ['url', 'shortlink', 'active', 'pub_date', ]
    list_display_links = ['url', ]
    list_editable = ['active', ]
    list_filter = ['url', ]

    search_fields = ['url', ]

admin.site.register(CutURL, CutURLManager)
