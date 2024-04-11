from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


# Now register the new UserAdmin...
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'last_name', 'first_name', 'is_active')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email','username','password')}),
        ('Personal Info', {'fields': ('first_name','last_name','tel', 'dob')}),
        ('Business Info', {'fields': ('business_name','role',)}),
        ('Location', {'fields': ('address_line', 'city', 'state', 'zip_code', 'country')}),
        ('Graph Data', {'fields': ('person_id','business_id')}),
        ('Permissions', 
            {
                'fields': (
                    'is_active',
                    'is_verified',
                    'is_staff',
                    'is_admin',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'last_name','first_name', 'password1', 'password2'),
        }),
    )
    search_fields       = ('email',)
    readonly_fields     = ('date_joined', 'last_login')
    ordering            = ('email', 'last_name','first_name')
    filter_horizontal   = ()