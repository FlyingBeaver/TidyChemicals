from django.contrib import admin
from profiles.models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",
                    "middle_names",
                    "phone_numbers",
                    "room",
                    "n_of_unread_messages",
                    "initialized",
                    "admin")


class HashtagAdmin(admin.ModelAdmin):
    list_display = ("name",
                    "creator",
                    "n_of_chemicals")


class AmpersandtagAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "name",
                    "creator",
                    "n_of_chemicals")


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "header",
                    "time_created",
                    "time_sent",
                    "message_type",
                    "read",
                    "recipient")


class FreeBarcodeAdmin(admin.ModelAdmin):
    list_display = ("number", "standard")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Ampersandtag, AmpersandtagAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(FreeBarcode, FreeBarcodeAdmin)
