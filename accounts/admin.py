from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User
from .forms import UserCreation, UserChange
# Register your models here.
class ZnUserAdmin(UserAdmin):
    add_form = UserCreation
    form = UserChange
    model = User
    list_display = ('email','first_name','last_name','profile_photo_tag', 'added_on', 'updated_on', 'is_superuser', 'is_active',)
    list_filter = ('first_name','last_name','email', 'is_superuser', 'is_active',)
    def profile_photo_tag(self, obj):
        if obj.profile_photo:
            return format_html('<img src="{}" style="border-radius:30px" width="30" height="30" />'.format(obj.profile_photo.url))
        return '-'
    profile_photo_tag.short_description = 'Profile Photo'
    fieldsets = (
        (None, {'fields': ('first_name','last_name', 'email', 'password','profile_photo')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','email', 'password1', 'password2', 'profile_photo', 'is_superuser', 'is_active')}
        ),
    )
    search_fields = ('email','first_name','last_name', 'added_on', 'updated_on')
    ordering = ('email','first_name','last_name', 'added_on', 'updated_on')
admin.site.register(User, ZnUserAdmin)