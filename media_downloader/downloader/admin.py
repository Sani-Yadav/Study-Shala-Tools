from django.contrib import admin
from .models import (
    Category, Movie, WebSeries, Episode,
    UserProfile, SubscriptionPlan, Download, WatchHistory
)
from django.utils.html import format_html

# Custom Admin Classes
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1  # Number of empty forms to display
    fields = ('title', 'episode_number', 'season_number', 'duration', 'is_free')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'language', 'quality', 'is_featured', 'is_free')
    list_filter = ('language', 'quality', 'is_featured', 'is_free', 'categories')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'categories')
        }),
        ('Media Details', {
            'fields': ('thumbnail', 'banner', 'video_url')
        }),
        ('Metadata', {
            'fields': ('release_year', 'duration', 'language', 'quality', 'imdb_rating')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_free')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(WebSeries)
class WebSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'language', 'is_featured')
    list_filter = ('language', 'is_featured', 'categories')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)
    inlines = [EpisodeInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'web_series', 'season_number', 'episode_number', 'is_free')
    list_filter = ('season_number', 'is_free', 'web_series')
    search_fields = ('title', 'web_series__title')
    list_select_related = ('web_series',)

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'is_active')
    list_editable = ('price', 'duration_days', 'is_active')
    search_fields = ('name', 'description')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_premium', 'subscription_expiry')
    list_filter = ('is_premium',)
    search_fields = ('user__username', 'phone')
    readonly_fields = ('user',)

class DownloadAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'content_id', 'downloaded_at')
    list_filter = ('content_type', 'downloaded_at')
    search_fields = ('user__username',)
    readonly_fields = ('downloaded_at',)

class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'content_id', 'watched_at')
    list_filter = ('content_type', 'watched_at')
    search_fields = ('user__username',)
    readonly_fields = ('watched_at',)

# Register models
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(WatchHistory, WatchHistoryAdmin)

# Customize Admin Site
admin.site.site_header = 'StudyShala Media Admin'
admin.site.site_title = 'StudyShala Media Portal'
admin.site.index_title = 'Welcome to StudyShala Media Admin Panel'
