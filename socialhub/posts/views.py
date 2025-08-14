from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm
from accounts.models import Follow  # To check friend relationships


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    login_url = reverse_lazy('accounts:login')

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.select_related('author').all()
        visible_posts = []
        for post in posts:
            if post.privacy == 'public':
                visible_posts.append(post)
            elif post.privacy == 'private' and post.author == user:
                visible_posts.append(post)
            elif post.privacy == 'friend':
                is_friend = Follow.objects.filter(follower=user, following=post.author).exists()
                if is_friend or post.author == user:
                    visible_posts.append(post)
        return visible_posts


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    login_url = reverse_lazy('accounts:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        # Privacy check before showing details
        if not self._can_view_post(post):
            context['no_access'] = True
            return context

        context['comment_form'] = CommentForm()
        context['liked_by_user'] = post.likes.filter(user=self.request.user).exists()
        return context

    def _can_view_post(self, post):
        user = self.request.user
        if post.privacy == 'public':
            return True
        if post.privacy == 'private' and post.author == user:
            return True
        if post.privacy == 'friend':
            return Follow.objects.filter(follower=user, following=post.author).exists() or post.author == user
        return False


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'
    success_url = reverse_lazy('post_list')
    login_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ToggleLikeView(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        # Respect privacy when liking
        if not self._can_interact(post):
            return redirect('post_list')

        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
        return redirect('post_detail', pk=pk)

    def _can_interact(self, post):
        if post.privacy == 'public':
            return True
        if post.privacy == 'private' and post.author == self.request.user:
            return True
        if post.privacy == 'friend':
            return Follow.objects.filter(follower=self.request.user, following=post.author).exists() or post.author == self.request.user
        return False


class AddCommentView(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        # Respect privacy when commenting
        if not self._can_interact(post):
            return redirect('post_list')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
        return redirect('post_detail', pk=pk)

    def _can_interact(self, post):
        if post.privacy == 'public':
            return True
        if post.privacy == 'private' and post.author == self.request.user:
            return True
        if post.privacy == 'friend':
            return Follow.objects.filter(follower=self.request.user, following=post.author).exists() or post.author == self.request.user
        return False
