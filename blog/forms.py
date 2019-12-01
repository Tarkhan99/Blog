from django import forms
from blog.models import BlogPost


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image']


class UpdateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image']

    def save(self, commit=True):
        blogPost = self.instance
        blogPost.title = self.cleaned_data['title']
        blogPost.body = self.cleaned_data['body']

        if self.cleaned_data['image']:
            blogPost.image = self.cleaned_data['image']

        if commit:
            blogPost.save()

        return blogPost
