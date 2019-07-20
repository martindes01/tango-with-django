from django import forms
from rango.models import Category, Page

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text='Category name')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Associate model and form
        model = Category

        # Include required fields
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text='Page title')
    url = forms.URLField(max_length=200, help_text='Page URL')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Associate model with form
        model = Page

        # Exclude category field from form
        exclude = ('category',)
        # Equivalent to including every other field
        #fields = ('title', 'url', 'views',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data
