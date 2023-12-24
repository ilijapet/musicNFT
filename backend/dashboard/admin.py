from django.contrib import admin

from backend.dashboard.models import NftMetadata, OrderHistory

admin.site.register(NftMetadata)
admin.site.register(OrderHistory)
