from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, ToggleLikeView, AddCommentView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/like/', ToggleLikeView.as_view(), name='toggle_like'),
    path('<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
]
