from django import forms
from django.contrib.auth.models import User

from rango.models import Category, Page, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text='Name: ')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Associate model and form
        model = Category

        # Include required fields
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text='Title: ')
    url = forms.URLField(max_length=200, help_text='URL: ')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Associate model with form
        model = Page

        # Include required fields
        # Equivalent to excluding every other field with exclude = (,)
        fields = ('title', 'url', 'views',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        exclude = ('user',)
