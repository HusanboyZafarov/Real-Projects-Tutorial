from django import forms
from .models import Contact, Work


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = '__all__'
        exclude = ['author', 'slug', 'likes', 'views_count']

