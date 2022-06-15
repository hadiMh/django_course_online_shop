from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField()
    short_description = models.TextField(blank=True)
    price = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    image = models.ImageField(_('Product Image'), upload_to='product/product_cover/', blank=True, )

    datetime_created = models.DateTimeField(_('Date Time of Creation'), default=timezone.now)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])


class ActiveCommentsManger(models.Manager):
    def get_queryset(self):
        return super(ActiveCommentsManger, self).get_queryset().filter(active=True)


class Comment(models.Model):
    PRODUCT_STARS = [
        ('1', _('Very Bad')),
        ('2', _('Bad')),
        ('3', _('Normal')),
        ('4', _('Good')),
        ('5', _('Perfect')),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments',)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Comment author'
    )
    body = models.TextField(verbose_name=_('Comment Text'))
    stars = models.CharField(max_length=10, choices=PRODUCT_STARS, verbose_name=_('What is your score?'))

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    # Manager
    objects = models.Manager()
    active_comments_manager = ActiveCommentsManger()

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.product.id])
