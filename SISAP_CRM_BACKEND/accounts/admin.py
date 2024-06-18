from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'display_roles')
    list_filter = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'roles')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'roles', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    def display_roles(self, obj):
        return ", ".join([role.common_name for role in obj.roles.all()])

    display_roles.short_description = 'Roles'

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('key', 'common_name')
    search_fields = ('key', 'common_name')
    filter_horizontal = ('groups',)

admin.site.register(CustomUser, CustomUserAdmin)
