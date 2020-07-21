import requests
from django import forms
from dateutil.parser import parse
from django.contrib.auth import get_user_model
from .models import Book, Review, Author, Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django_starfield import Stars


url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({'class': 'bs-textarea', 'placeholder': 'コメントする', 'rows': 5})


class AddBookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('isbn',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['isbn'].widget.attrs['class'] = 'bs-input'
        self.fields['isbn'].widget.attrs['placeholder'] = 'ISBN'

    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']

        req_url = url + isbn
        response = requests.get(req_url)
        data = response.json()
        if data['totalItems'] == 0:
            raise forms.ValidationError('この本はGoogleブックスに存在しません')

        if len(isbn) == 10:
            identifiers = data['items'][0]['volumeInfo']['indusryIdentifiers']
            for identifier in identifiers:
                if identifier['type'] == 'ISBN_13':
                    isbn_13 = identifier['identifier']
                    if Book.objects.filter(isbn=isbn_13).exists():
                        raise forms.ValidationError('この本は既に登録済みです')
                    else:
                        isbn = isbn_13
        return isbn
    
    def save_form_api(self):
        book = super().save(commit=False)

        req_url = url + book.isbn
        response = requests.get(req_url)
        data = response.json()['items'][0]['volumeInfo']

        book.title = data['title']
        if 'subtitle' in data:
            book.subtitle = data['subtitle']
        book.description = data['description']
        book.image_link = data['imageLinks']['thumbnail']
        book.info_link = data['infoLink']
        if 'publishedDate' in data:
            book.published_date = parse(data['publishedDate']).date()
        book.save()

        book_authors = data['authors']
        for book_author in book_authors:
            author, created = Author.objects.get_or_create(name=book_author)
            book.authors.add(author)

        return book


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'bs-input bs-form-large'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['class'] = 'bs-input bs-form-large'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'bs-input bs-form-large'
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
        self.fields['password1'].widget.attrs['class'] = 'bs-input bs-form-large'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード（英数字８〜１５０文字）'
        self.fields['password2'].widget.attrs['class'] = 'bs-input bs-form-large'
        self.fields['password2'].widget.attrs['placeholder'] = '確認用パスワード'


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('icon', 'username', 'first_name', 'last_name', 'email', 'bio',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'bs-input bs-form-width-large'
        self.fields['first_name'].widget.attrs['class'] = 'bs-input bs-form-width-large'
        self.fields['last_name'].widget.attrs['class'] = 'bs-input bs-form-width-large'
        self.fields['email'].widget.attrs['class'] = 'bs-input bs-form-width-large'
        self.fields['bio'].widget.attrs.update({'class': 'bs-textarea', 'rows': 8})


class PostReviewForm(forms.ModelForm):

    score = forms.IntegerField(
        label='',
        max_value=5.0,
        min_value=1.0,
        required=True,
        initial=1,
        widget=Stars,
    )

    class Meta:
        model = Review
        fields = ('score', 'title', 'reason', 'body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'bs-input'})
        self.fields['reason'].widget.attrs.update({'class': 'bs-textarea', 'rows': 3})
        self.fields['body'].widget.attrs.update({'class': 'bs-textarea', 'rows': 8})


