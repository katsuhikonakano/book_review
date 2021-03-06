# Generated by Django 2.2.5 on 2020-06-11 00:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='著者名')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(error_messages={'unique': 'この本は既に登録済みです'}, max_length=13, unique=True, verbose_name='ISBN')),
                ('title', models.CharField(max_length=200, verbose_name='書籍名')),
                ('subtitle', models.CharField(blank=True, max_length=200, null=True, verbose_name='サブタイトル')),
                ('published_date', models.DateField(verbose_name='発刊日')),
                ('description', models.TextField(verbose_name='説明')),
                ('image_link', models.URLField(verbose_name='画像URL')),
                ('info_link', models.URLField(verbose_name='書籍情報URL')),
                ('authors', models.ManyToManyField(to='bookapp.Author', verbose_name='著者')),
                ('marks', models.ManyToManyField(blank=True, related_name='marks', to=settings.AUTH_USER_MODEL, verbose_name='マークしたユーザ')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='タグ名')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='スコア')),
                ('title', models.CharField(max_length=200, verbose_name='タイトル')),
                ('reason', models.TextField(verbose_name='読んだ理由')),
                ('body', models.TextField(verbose_name='レビュー')),
                ('reviewed_at', models.DateField(auto_now_add=True, verbose_name='レビュー日時')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookapp.Book', verbose_name='対象の本')),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='いいねしたユーザ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='レビューユーザー')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='コメント')),
                ('commented_at', models.DateField(auto_now_add=True, verbose_name='コメント日時')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookapp.Review', verbose_name='対象のレビュー')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='コメントユーザ')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(blank=True, to='bookapp.Tag', verbose_name='タグ'),
        ),
    ]
