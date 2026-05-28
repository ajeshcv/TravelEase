from django.contrib import admin
from .models import CustomUser, Place, Spotlight, Image
from django.contrib.auth.admin import UserAdmin
from .models import PackagerProfile, Hotel
from .models import FAQ


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'is_spotlight')
    list_filter = ('is_spotlight',)
    search_fields = ('name', 'description')
    filter_horizontal = ('extra_images',)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_approved', 'document') 
    list_filter = ('user_type', 'is_approved')
    search_fields = ('username', 'email')
    actions = ['approve_packagers']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_approved', 'user_type')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    def approve_packagers(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected packagers have been approved.")
    approve_packagers.short_description = "Approve selected packagers"


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'url')
    search_fields = ('description',)


class SpotlightAdmin(admin.ModelAdmin):
    list_display = ('title',)


class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rating', 'price_per_person', 'phone_number', 'email', 'image')
    search_fields = ('name', 'description')
    list_filter = ('rating', 'price_per_person')
    filter_horizontal = ('extra_images',) 


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'created_at', 'answer')
    search_fields = ('question',)
    readonly_fields = ('question', 'user', 'created_at') 

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False   


admin.site.register(Place, PlaceAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Spotlight, SpotlightAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PackagerProfile)
admin.site.register(Hotel, HotelAdmin)
