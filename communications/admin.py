# communications/admin.py
from django.contrib import admin
from django.utils import timezone
from .models import Message, Conversation, Attachment, MessageFlag


@admin.register(MessageFlag)
class MessageFlagAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "flagged_by", "created_at", "resolved")
    actions = ["resolve_flags"]

    def resolve_flags(self, request, queryset):
        queryset.update(resolved=True, resolved_by=request.user, resolved_at=timezone.now())
        self.message_user(request, f"{queryset.count()} flags resolved.")
    resolve_flags.short_description = "Resolve selected flags"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "created_at", "is_system")
    search_fields = ("content", "sender__username", "conversation__name")
    list_filter = ("is_system", "created_at")

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_group", "updated_at")
    search_fields = ("name",)
    filter_horizontal = ("participants",)

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):    
    list_display = ("id", "message", "original_name", "uploaded_at")
    search_fields = ("original_name", "message__content")

    
