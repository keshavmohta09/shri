from django.db import models
from django.utils.timezone import now


class BaseModel(models.Model):
    """
    Contains the date_created, date_updated, date_deleted fields.
    """

    BASE_FIELDS = (
        "date_created",
        "date_updated",
        "date_deleted",
    )

    date_created = models.DateTimeField(default=now)
    date_updated = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(default=None, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
