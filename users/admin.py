from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')

class CustomUserAdmin(UserAdmin):
    # Use custom forms for user creation and change
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    # Display fields in the list view
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    
    # List filters
    list_filter = ('is_staff', 'is_active', 'is_superuser')

    # Fields to display in the detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # Fields to include in the form for adding a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
        ),
    )

    # Search fields for the admin interface
    search_fields = ('email', 'first_name', 'last_name')

    # Ordering for the admin list view
    ordering = ('email',)

    # Ensure the admin can handle the CustomUser model
    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)
