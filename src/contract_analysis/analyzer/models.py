from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
import os

# Create your models here.
class Contract(models.Model):
    document = models.FileField(upload_to='analyzer/contracts', verbose_name="")
    resWatsonKeywords = models.FileField(upload_to='analyzer/keywords', null=True, blank=True)
    def __str__(self):
        # return self.contract_title
        # return "%s (ID:%s)" % (self.name, self.id)
        return "(ID:%s)" % (self.id)