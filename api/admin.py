from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserActivity, LandingPage

class UserActivityInline(admin.TabularInline):
    model = UserActivity
    extra = 0
    readonly_fields = ('date', 'keystrokes', 'coins_earned')
    can_delete = False

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'total_coins', 'current_streak')
    readonly_fields = ('last_activity_date',)
    fieldsets = UserAdmin.fieldsets + (
        ('Key2Coin Stats', {'fields': ('total_keystrokes', 'total_coins', 'current_streak', 'last_activity_date')}),
    )
    inlines = [UserActivityInline]
    ordering = ('-total_coins',)

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'keystrokes', 'coins_earned')
    list_filter = ('date', 'user')
    search_fields = ('user__username', 'source_app')
    date_hierarchy = 'date'

@admin.register(LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_editable = ('is_active',)
    prepopulated_fields = {"title": ("description",)}