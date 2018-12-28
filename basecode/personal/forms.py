from django import forms
from personal.models import Document



class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)







