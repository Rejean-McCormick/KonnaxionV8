"""
File: apps/kreative/kreative_community/models.py

Purpose:
Create models for community posts, reviews, ratings, and threaded comments related to art.
"""

from django.db import models
from common.base_models import BaseModel

class CommunityPost(BaseModel):
    """
    Represents a community post related to art.
    """
    title = models.CharField(max_length=255, help_text="Title of the post")
    content = models.TextField(help_text="Content of the post")
    posted_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="community_posts",
        help_text="User who posted the community post"
    )

    def __str__(self):
        return self.title

class PostComment(BaseModel):
    """
    Represents a comment on a community post, supporting threaded replies.
    """
    post = models.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="The community post being commented on"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        help_text="Parent comment for threaded replies"
    )
    content = models.TextField(help_text="Content of the comment")
    commented_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="post_comments",
        help_text="User who made the comment"
    )

    def __str__(self):
        return f"Comment by {self.commented_by} on {self.post.title}"

class ArtworkReview(BaseModel):
    """
    Represents a review or rating for an artwork.
    """
    artwork = models.ForeignKey(
        "artworks.Artwork",
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Artwork being reviewed"
    )
    reviewed_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="artwork_reviews",
        help_text="User who reviewed the artwork"
    )
    rating = models.PositiveSmallIntegerField(help_text="Rating value (e.g., 1 to 5)")
    review_text = models.TextField(null=True, blank=True, help_text="Optional review text")

    def __str__(self):
        return f"Review for {self.artwork.title} by {self.reviewed_by}"
