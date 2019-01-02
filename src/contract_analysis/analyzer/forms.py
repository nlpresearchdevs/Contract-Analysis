from django import forms
from analyzer.models import Contract

class ContractForm(forms.ModelForm):
    # title = forms.CharField(max_length=50)
    # file = forms.FileField()
    class Meta:
        model = Contract
        fields = ('document',)