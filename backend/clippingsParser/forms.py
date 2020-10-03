from django import forms


class UploadClippingsFileForm(forms.Form):
    file = forms.FileField()
