from django import forms

from .models import Images, Albums


class CreateAlbumForm(forms.ModelForm):
    class Meta:
        model = Albums
        fields = ['name', 'photo', 'public']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }


class AddImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'photo', 'content', 'album']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'content_text_area', 'placeholder': 'Введите подпись...'}),
            'title': forms.TextInput(attrs={'placeholder': 'Название картинки'})
        }


class EditImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'photo', 'content', 'public']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'content_text_area', 'placeholder': 'Введите подпись...'}),
            'title': forms.TextInput(attrs={'placeholder': 'Название картинки'})
        }


class AddImageToAlbumForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'photo', 'content', 'public']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите подпись...', 'rows': 5}),
            'title': forms.TextInput(attrs={'placeholder': 'Название картинки', 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
