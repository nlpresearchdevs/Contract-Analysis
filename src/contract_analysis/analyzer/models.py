from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
import os

# Create your models here.
class Contract(models.Model):
    document = models.FileField(upload_to='analyzer/contracts', verbose_name="")
    resWatsonCategories = models.FileField(upload_to='analyzer/results/categories', null=True, blank=True)
    resWatsonConcepts = models.FileField(upload_to='analyzer/results/concepts', null=True, blank=True)
    resWatsonEntities = models.FileField(upload_to='analyzer/results/entities', null=True, blank=True)
    resWatsonKeywords = models.FileField(upload_to='analyzer/results/keywords', null=True, blank=True)
    resWatsonRelations = models.FileField(upload_to='analyzer/results/relations', null=True, blank=True)
    resWatsonSemanticRoles = models.FileField(upload_to='analyzer/results/semanticRoles', null=True, blank=True)
    resWatsonSentiments = models.FileField(upload_to='analyzer/results/sentiment', null=True, blank=True)
    resWatsonContractElements = models.FileField(upload_to='analyzer/results/contractElements', null=True, blank=True)

    @property
    def filename(self):
        return os.path.basename(self.document.name)

    def __str__(self):
        # return self.contract_title
        # return "%s (ID:%s)" % (self.name, self.id)
        return "{0}. {1}".format(self.id, self.filename)
        # return "(ID:%s)" % (self.id) 