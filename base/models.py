import os
from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import FileExtensionValidator


# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name



class Dataset(models.Model):
  category = models.ManyToManyField(Category, blank=True)
  title = models.CharField(_("Title"), max_length=255, blank=True)
  description = models.TextField(blank=True, null=True)
  tags = models.TextField(blank=True)
  overview = models.TextField(_("Overview"), blank=True)
  author = models.CharField(max_length=255, blank=True)
  research_title = models.CharField(max_length=255, blank=True)
  link = models.CharField(max_length=255, blank=True)
  source = models.CharField(max_length=255, blank=True, choices=(
    ("primary", "Primary"),
    ("secondary", "Secondary"),
  ))
  form = models.CharField(max_length=255, blank=True, choices=(
    ("raw", "Raw"),
    ("processed", "Processed/Cleaned"),
  ))
  format = models.CharField(max_length=255, blank=True)
  file = models.FileField(upload_to="uploads/", blank=True, null=True,
                          validators=[
                            FileExtensionValidator(allowed_extensions=["zip", "rar"])
                          ])

  def __str__(self):
    return self.title
    


    