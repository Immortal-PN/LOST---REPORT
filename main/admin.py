from django.contrib import admin

from .models import LostItem, FoundItem, ClaimRequest


@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):

    list_display = ('title', 'category', 'location', 'date_lost')

    search_fields = ('title', 'description', 'location')

    list_filter = ('category', 'date_lost')


@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):

    list_display = ('title', 'category', 'location', 'date_found')

    search_fields = ('title', 'description', 'location')

    list_filter = ('category', 'date_found')


@admin.register(ClaimRequest)
class ClaimRequestAdmin(admin.ModelAdmin):

    list_display = ('item', 'claimant', 'status', 'created_at')

    list_filter = ('status',)