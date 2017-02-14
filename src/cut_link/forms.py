from django import forms

from .validators import validate_url


class URLForm(forms.Form):
    url = forms.CharField(label='',
                          validators=[validate_url],
                          widget=forms.TextInput(
                              attrs={
                                  'class': "form-control",
                                  'placeholder': 'Long URL',
                              }
                          ))

    # We can validate our link this way, for example:
    # def clean(self):
    #     cleaned_data = super(URLForm, self).clean()
    #     url = cleaned_data.get('url')
    #     url_validator = URLValidator()
    #     try:
    #         url_validator(url)
    #     except:
    #         raise forms.ValidationError('Invalid URL!')
    #     return url
