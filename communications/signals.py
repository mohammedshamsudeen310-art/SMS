# communications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from .models import get_profile

@receiver(post_save, sender=Message)
def notify_participants(sender, instance, created, **kwargs):
    if not created:
        return

    convo = instance.conversation

    # Exclude sender
    recipients = convo.participants.exclude(pk=instance.sender_id)

    # 🔹 Optional: filter those who have email_notify=True (for any profile type)
    notified = []
    for user in recipients:
        profile = None
        # Try to detect which profile the user has
        if hasattr(user, "admin_profile"):
            profile = user.admin_profile
        elif hasattr(user, "teacher_profile"):
            profile = user.teacher_profile
        elif hasattr(user, "parent_profile"):
            profile = user.parent_profile
        elif hasattr(user, "accountant_profile"):
            profile = user.accountant_profile

        # Now check safely
        if profile and getattr(profile, "email_notify", False):
            notified.append(user)


@receiver(post_save, sender=Message)
def notify_participants(sender, instance, created, **kwargs):
    if not created:
        return
    convo = instance.conversation
    recipients = convo.participants.exclude(pk=instance.sender_id)
    notified = [u for u in recipients if getattr(get_profile(u), "email_notify", False)]
    # Send notifications to `notified`

