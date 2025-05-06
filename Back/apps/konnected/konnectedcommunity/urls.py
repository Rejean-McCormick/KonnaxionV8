from django.urls import path
from .views import (
    DiscussionThreadListView,
    DiscussionThreadDetailView,
    DiscussionThreadCreateView,
    CommentCreateView,
)

app_name = "community"

urlpatterns = [
    path("", DiscussionThreadListView.as_view(), name="thread_list"),
    path("thread/<int:pk>/", DiscussionThreadDetailView.as_view(), name="thread_detail"),
    path("thread/create/", DiscussionThreadCreateView.as_view(), name="thread_create"),
    # For posting a comment on a specific thread
    path("thread/<int:thread_pk>/comment/create/", CommentCreateView.as_view(), name="comment_create"),
]
