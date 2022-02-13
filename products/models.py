from django.core.cache import cache
from django.db import models
from django.db.models import QuerySet, Manager
from django.utils import timezone


class CustomQuerySet(QuerySet):
    def update(self, **kwargs):
        cache.delete('product_objects')
        super().update(updated=timezone.now(), **kwargs)


class CustomManager(Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)


class Product(models.Model):
    title = models.CharField(max_length=200, blank=False)
    price = models.CharField(max_length=20, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    objects = CustomManager()