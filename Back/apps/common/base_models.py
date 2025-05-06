from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating 'created_at' and 'updated_at' fields.
    These fields record when an instance is created and last updated.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    An abstract base class model that provides a soft delete mechanism.
    Instead of permanently deleting records, they are marked as deleted.
    """
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        """
        Override the default delete method to perform a soft delete.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        """
        Restore a soft-deleted record.
        """
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])

    def hard_delete(self, using=None, keep_parents=False):
        """
        Permanently delete the record from the database.
        """
        super(SoftDeleteModel, self).delete(using=using, keep_parents=keep_parents)

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel, SoftDeleteModel):
    """
    An abstract base model that combines timestamping and soft deletion.
    This model serves as a foundation for all other models in the platform.
    
    Additional hooks for event logging or auditing can be added by overriding the save() method here.
    """
    class Meta:
        abstract = True
