from django import forms
from .models import Dataset


# class DatasetForm(forms.ModelForm):
#   title = forms.CharField(widget=forms.Textarea(attrs={"placeholder" : "The title"}))
#   CHOICES = [("1", "First"), ("2", "Second")]
#   category = forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices=CHOICES)
#   class Meta:
#     model = Dataset
#     fields = "__all__"
#     exclude = ["overview"]


class DatasetFormFirstPage(forms.ModelForm):
    class Meta:
        model = Dataset
        exclude = ['file']

class DatasetFormSecondPage(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['file']

