from django.contrib import admin
from .models import CustomUser, Spam_Contacts


@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ('username', 'photo')


admin.site.register(Spam_Contacts)
