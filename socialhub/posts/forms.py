from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Loop through all fields to apply a consistent style
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            # Customize specific fields based on their type
            if field_name == 'text':
                field.widget.attrs.update({
                    'rows': 4,  # Adjust rows for better user experience
                    'placeholder': 'What\'s on your mind?'
                })
                field.label = ''  # Using a placeholder instead of a label
                
            elif field_name == 'image':
                # The 'form-control' class for file inputs works well in Bootstrap 5+
                field.label = 'Upload an image'
                
            elif field_name == 'privacy':
                # For select fields, use 'form-select' for proper styling
                field.widget.attrs['class'] = 'form-select'
                field.label = 'Who can see this post?'
                
    class Meta:
        model = Post
        fields = ['text', 'image', 'privacy']

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='Add a Comment',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = Comment
        fields = ['content']