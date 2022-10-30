from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone

User = get_user_model()


class Level(models.Model):
    level = models.CharField(max_length=100)

    def __str__(self):
        return self.level


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(default='', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Category)
def category_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


class Course(models.Model):
    STATUS = (
        ('PUBLISH', 'publish'),
        ('DRAFT', 'draft'),
    )

    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='products', null=True)
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='categories', null=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, related_name='levels', null=True)
    description = models.TextField(blank=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    image = models.ImageField(upload_to='images', default=0)
    slug = models.SlugField(default='', max_length=100, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Course)
def category_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


class WhatYouLearn(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='what_learn')
    points = models.CharField(max_length=500) # Раздел для списков, что мы будем изучать

    def __str__(self):
        return self.points


class Requirements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='requirements')
    points = models.CharField(max_length=500) # Раздел для списков рекомендаций

    def __str__(self):
        return self.points