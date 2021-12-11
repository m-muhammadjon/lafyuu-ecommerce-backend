from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreateForm
from .models import User, Verification


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreateForm

    list_display = ('email', 'first_name', 'last_name')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password', 'password2',),
        }),
    )


admin.site.register(Verification)
