# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from accounts.models import Notification, Settings
from posts.models import Like, Comment  # Ensure these exist with .post and .user fields
from accounts.models import Follow  # Add this import

@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        # Create notification
        Notification.objects.create(
            user=instance.following,
            message=f"{instance.follower.username} started following you."
        )
        
        # Send email if enabled
        send_notification_email(
            instance.following,
            "New Follower",
            'accounts/emails/follow_notification.html',
            'accounts/emails/follow_notification.txt',
            {'user': instance.following, 'follower': instance.follower}
        )


def send_notification_email(user, subject, html_template, txt_template, context):
    """Helper to send both HTML + plain text email."""
    if not getattr(user, 'email', None):
        return
    # Check if user allows notifications
    if hasattr(user, 'settings') and not user.settings.allow_notifications:
        return

    html_content = render_to_string(html_template, context)
    text_content = render_to_string(txt_template, context)
    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        liker = instance.user
        if post.author != liker:
            Notification.objects.create(
                user=post.author,
                message=f"{liker.username} liked your post."
            )
            send_notification_email(
                post.author,
                "New Like on Your Post",
                'accounts/emails/like_notification.html',
                'accounts/emails/like_notification.txt',
                {'user': post.author, 'liker': liker, 'post': post}
            )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        commenter = instance.user
        if post.author != commenter:
            Notification.objects.create(
                user=post.author,
                message=f"{commenter.username} commented on your post."
            )
            send_notification_email(
                post.author,
                "New Comment on Your Post",
                'accounts/emails/comment_notification.html',
                'accounts/emails/comment_notification.txt',
                {'user': post.author, 'commenter': commenter, 'post': post}
            )
