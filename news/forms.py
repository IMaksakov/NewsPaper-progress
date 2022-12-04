from django import forms
from .models import Post, Author
from django.core.exceptions import ValidationError
class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=20)

    class Meta:
       model = Post
       fields = [
           'author',
           'text',
           'title',
           'choice',
           'posting_time',
           'category',
           'post_rating',
       ]

       def clean(self):
           cleaned_data = super().clean()
           text = cleaned_data.get("text")
           title = cleaned_data.get("title")

           if text == title:
               raise ValidationError(
                   "Описание не должно быть идентично названию."
               )

           return cleaned_data