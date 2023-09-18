from django import forms 
from .models import Article, Comment

from ckeditor.fields import RichTextField

class FormText(forms.Form):
    text = forms.CharField(label='Text', max_length=1000, widget=forms.Textarea(attrs={'class':'form-control'}), required=True)


class AddArticle(forms.ModelForm):
    description = RichTextField()  # Champ CKEditor

    # Champ texte brut pour la description
    description_plain = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False  # La description brute est facultative
    )

    class Meta:
        model = Article
        fields = ['title', 'description', 'description_plain', 'banner', 'category']
