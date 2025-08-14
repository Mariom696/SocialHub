from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import login
from django.conf import settings

from .models import Profile, Settings, Follow, Notification, Report, Block
from .forms import UserRegistrationForm, ProfileForm, SettingsForm, ReportForm
from .tokens import account_activation_token
from django.apps import apps
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')



def register(request):
    """User registration with email verification."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.is_active = True
            new_user.save()

            Profile.objects.create(user=new_user)
            Settings.objects.create(user=new_user)

            # Send activation email
            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'
            subject = 'Activate your SocialHub account'
            message = render_to_string('registration/activation_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'protocol': protocol,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [new_user.email])
            email.send()

            messages.success(request, 'Please confirm your email address to complete registration.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def activate(request, uidb64, token):
    """Activate account via email link."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        # Send welcome email
        subject = 'Welcome to SocialHub!'
        message = render_to_string('registration/welcome_email.html', {'user': user})
        email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        email.send()

        messages.success(request, 'Your account has been activated! You can now log in.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Activation link is invalid or expired.')
        return redirect('accounts:login')


@login_required
def profile_view(request, username):
    Post = apps.get_model('posts', 'Post')
    profile_user = get_object_or_404(User, username=username)
    profile_settings = getattr(profile_user, 'settings', None)
    
    # Check if current user is following the profile user
    is_following = False
    is_own_profile = request.user == profile_user
    
    if request.user.is_authenticated and not is_own_profile:
        is_following = Follow.objects.filter(
            follower=request.user, 
            following=profile_user
        ).exists()
    
    # Determine what content to show based on privacy
    can_view_posts = True
    can_view_profile_details = True
    
    if profile_settings and not is_own_profile:
        if profile_settings.profile_visibility == 'private':
            can_view_posts = is_following
            can_view_profile_details = is_following
        elif profile_settings.profile_visibility == 'friend':
            can_view_posts = is_following
            can_view_profile_details = is_following

    # Get visible posts if user can view them
    visible_posts = []
    if can_view_posts:
        posts = Post.objects.filter(author=profile_user)
        for post in posts:
            if post.privacy == 'public':
                visible_posts.append(post)
            elif post.privacy == 'private' and is_own_profile:
                visible_posts.append(post)
            elif post.privacy == 'friend' and (is_following or is_own_profile):
                visible_posts.append(post)

    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'posts': visible_posts,
        'is_following': is_following,
        'is_own_profile': is_own_profile,
        'can_view_posts': can_view_posts,
        'can_view_profile_details': can_view_profile_details,
    })

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('accounts:profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def settings_view(request):
    settings_instance = request.user.settings
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=settings_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated.')
            return redirect('accounts:settings')
    else:
        form = SettingsForm(instance=settings_instance)
    return render(request, 'accounts/settings.html', {'form': form})


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(
            follower=request.user, 
            following=user_to_follow
        )
        messages.success(request, f'You are now following {user_to_follow.username}')
    return redirect('accounts:profile', username=user_to_follow.username)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(
        follower=request.user, 
        following=user_to_unfollow
    ).delete()
    messages.success(request, f'You unfollowed {user_to_unfollow.username}')
    return redirect('accounts:profile', username=user_to_unfollow.username)

@login_required
def report_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            Report.objects.create(
                reporter=request.user,
                reported_user=target_user,
                reason=form.cleaned_data['reason']
            )
            messages.success(request, 'Report submitted.')
            return redirect('accounts:profile', username=target_user.username)
    else:
        form = ReportForm()
    return render(request, 'accounts/report_user.html', {'form': form, 'target_user': target_user})


@login_required
def block_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if target_user != request.user:
        Block.objects.get_or_create(blocker=request.user, blocked=target_user)
    return redirect('accounts:profile', username=request.user.username)


@login_required
def notifications_list(request):
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, 'accounts/notifications.html', {'notifications': notifications})


@login_required
def mark_notification_read(request, notification_id):
    notif = get_object_or_404(Notification, id=notification_id, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('accounts:notifications')
