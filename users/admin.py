from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from users.models import UserProfile, Department, Position

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'

# Define a new User admin


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'parent',
        'manager',
        'active',
    )
    list_filter = (
        'parent',
        'customer',
        'manager',
        'active',
    )
    search_fields = ('name',)
    raw_id_fields = ('parent', 'manager', 'customer')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'department',
        'parent',
        'supervisor',
        'active',
    )
    list_filter = (
        'department',
        'parent',
        'supervisor',
        'customer',
        'active',
    )
    search_fields = ('name',)
    raw_id_fields = ('parent', 'department', 'supervisor', 'customer')
