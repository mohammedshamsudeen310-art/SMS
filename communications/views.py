# communications/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.utils import timezone
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

# ✅ Local imports
from .models import Conversation, Message, Attachment
from accounts.models import CustomUser


# ================================================================
# 🔹 VIEW: Conversation detail page (shows messages)
# ================================================================
@login_required
def conversation_detail(request, pk):
    convo = get_object_or_404(Conversation, pk=pk)

    # 🚫 Restrict access to participants only
    if not convo.participants.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden("Not allowed")

    # 📨 Load recent 100 messages (oldest to newest)
    messages = convo.messages.select_related("sender").order_by("-created_at")[:100][::-1]

    return render(request, "communications/conversation_detail.html", {
        "conversation": convo,
        "messages": messages,
    })


# ================================================================
# 🔹 VIEW: Create a new conversation
# ================================================================
@login_required
def create_conversation(request):
    if request.method == "POST":
        participant_ids = request.POST.getlist("participants")
        name = request.POST.get("name", "")

        convo = Conversation.objects.create(name=name or "")
        convo.participants.add(request.user)

        for uid in participant_ids:
            try:
                user = CustomUser.objects.get(pk=uid)
                convo.participants.add(user)
            except CustomUser.DoesNotExist:
                continue

        convo.save()
        return redirect("conversation_detail", pk=convo.pk)

    users = CustomUser.objects.exclude(pk=request.user.pk)
    return render(request, "communications/create_conversation.html", {"users": users})


# ================================================================
# 🔹 VIEW: Handle message send + attachments (AJAX)
# ================================================================
@login_required
def upload_attachment(request, pk):
    """
    Handles sending a new chat message (text and optional files).
    Returns rendered HTML for dynamic injection.
    """
    convo = get_object_or_404(Conversation, pk=pk)

    # 🚫 Ensure user belongs to this chat
    if not convo.participants.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden("You are not a participant in this conversation.")

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    text = request.POST.get("text", "").strip()
    files = request.FILES.getlist("files")

    # ✅ Save message to DB
    message = Message.objects.create(
        conversation=convo,
        sender=request.user,
        content=text or "",
        created_at=timezone.now()
    )

    # ✅ Save attachments (if any)
    attachments = []
    for f in files:
        att = Attachment.objects.create(
            message=message,
            file=f,
            original_name=f.name
        )
        attachments.append({
            "id": att.id,
            "url": att.file.url,
            "name": att.original_name
        })

    # ✅ Render message bubble HTML (for instant display)
    html = render_to_string("communications/message_bubble.html", {
        "m": message,
        "request": request,
    })

    # ✅ Broadcast via WebSocket (real-time)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"chat_{convo.pk}",
        {
            "type": "message.broadcast",
            "message": {
                "id": message.id,
                "sender_id": request.user.id,
                "sender_username": request.user.get_full_name() or request.user.username,
                "content": message.content,
                "created_at": message.created_at.isoformat(),
                "attachments": attachments,
            },
        }
    )

    # ✅ Clean JSON response (no debug strings)
    return JsonResponse({
        "success": True,
        "html": html,
        "attachments": attachments,
    }, content_type="application/json")


# ================================================================
# 🔹 VIEW: List conversations (with search and filters)
# ================================================================
@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(participants=request.user)
    q = request.GET.get("q", "")
    filter_option = request.GET.get("filter", "")

    if q:
        conversations = conversations.filter(
            Q(name__icontains=q) |
            Q(participants__username__icontains=q)
        ).distinct()

    if filter_option == "recent":
        conversations = conversations.order_by("-updated_at")
    elif filter_option == "active":
        conversations = conversations.filter(messages__isnull=False).distinct()

    return render(request, "communications/conversation_list.html", {"conversations": conversations})


# ================================================================
# 🔹 VIEW: AJAX filtering / search for conversations
# ================================================================
@login_required
def conversation_list_ajax(request):
    conversations = Conversation.objects.filter(participants=request.user)
    q = request.GET.get("q", "")
    filter_option = request.GET.get("filter", "")

    if q:
        conversations = conversations.filter(
            Q(name__icontains=q) |
            Q(participants__username__icontains=q)
        ).distinct()

    if filter_option == "recent":
        conversations = conversations.order_by("-updated_at")
    elif filter_option == "active":
        conversations = conversations.filter(messages__isnull=False).distinct()

    return render(request, "communications/conversation_list_partial.html", {"conversations": conversations})


# ================================================================
# 🔹 VIEW: Handle text-only message via JSON (fallback)
# ================================================================
@login_required
def send_message(request, convo_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "").strip()
            if not text:
                return JsonResponse({"success": False, "error": "Empty message"})

            convo = Conversation.objects.get(pk=convo_id)
            msg = Message.objects.create(
                conversation=convo,
                sender=request.user,
                content=text,
                created_at=timezone.now()
            )

            return JsonResponse({
                "success": True,
                "message": {
                    "id": msg.id,
                    "sender": request.user.get_full_name() or request.user.username,
                    "content": msg.content,
                    "timestamp": msg.created_at.strftime("%b %d, %Y %H:%M")
                }
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid method"})


# ================================================================
# 🔹 VIEW: Fetch new messages (for auto-refresh / live chat)
# ================================================================
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Message, Conversation  # adjust if your app name differs

@login_required
def fetch_new_messages(request, conversation_id):
    last_id = request.GET.get("after", 0)
    conversation = Conversation.objects.get(pk=conversation_id)

    messages = (
        Message.objects.filter(conversation=conversation, id__gt=last_id)
        .select_related("sender")
        .order_by("id")
    )

    data = []
    for m in messages:
        data.append({
            "id": m.id,
            "sender": m.sender.get_full_name() or m.sender.username,
            "content": m.content,
            "timestamp": m.created_at.strftime("%b %d, %Y %H:%M"),
            "is_self": m.sender == request.user,
        })

    return JsonResponse({"messages": data})

