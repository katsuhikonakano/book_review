from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.urls import reverse
# Create your models here.

class Author(models.Model):
    name = models.CharField('著者名', max_length=200)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField('タグ名', max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        unique=True,
        error_messages={
            'unique': _("この本は既に登録済みです"),
        },
    )
    title = models.CharField('書籍名', max_length=200)
    subtitle = models.CharField('サブタイトル', max_length=200, blank=True, null=True)
    authors = models.ManyToManyField(Author, verbose_name='著者')
    tags = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)
    published_date = models.DateField('発刊日', blank=True, null=True)
    description = models.TextField('説明')
    image_link = models.URLField('画像URL')
    info_link = models.URLField('書籍情報URL')
    marks = models.ManyToManyField(get_user_model(), related_name='marks', verbose_name='マークしたユーザ', blank=True)

    def __str__(self):
        return self.title
    
    def get_api_mark_url(self):
        return reverse('mark_book_api', kwargs={'book_id': self.id})
    
    def latest_review_set(self):
        return self.review_set.order_by('-reviewed_at')
    
    def avg_score(self):
        return self.review_set.aggregate(Avg('score'))['score__avg']

class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews', verbose_name='レビューユーザー')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='対象の本')
    score = models.IntegerField('スコア', validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField('タイトル', max_length=200)
    reason = models.TextField('読んだ理由')
    body = models.TextField('レビュー')
    likes = models.ManyToManyField(get_user_model(), related_name='likes', verbose_name='いいねしたユーザ', blank=True)
    reviewed_at = models.DateField('レビュー日時', auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_api_like_url(self):
        return reverse('like_review_api', kwargs={'review_id': self.id})
    
    def oldest_comment_set(self):
        return self.comment_set.order_by('commented_at')

class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='コメントユーザ')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, verbose_name='対象のレビュー')
    body = models.TextField('コメント')
    commented_at = models.DateField('コメント日時', auto_now_add=True)

    def __str__(self):
        return self.body
    

#OK