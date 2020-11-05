from django import forms


class UploadClippingsFileForm(forms.Form):
    library_name = forms.CharField(max_length=50)
    file = forms.FileField()
