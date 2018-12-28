from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
import os



class Document(models.Model):
    document = models.FileField(upload_to='documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    resWatsonClase= models.CharField(max_length=1000, blank=True, null= True)
    resWatsonScore= models.IntegerField(blank=True, null= True)

    def __str__(self):
            return "%s (ID:%s)" % (self.name, self.id)
    

















        

