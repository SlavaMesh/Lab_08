from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    rate = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'

    def get_author_posts_rate(self):
        result = 0
        for post in self.posts.values('rate'):
            result += post['rate']
        return result * 3

    def get_author_comments_rate(self):
        result = 0
        for comment in self.user.comments.values():
            result += comment['rate']
        return result

    def get_comments_to_author_posts_rate(self):
        result = 0
        for post in self.posts.all():
            for comment in Comment.objects.filter(post=post).values('rate'):
                result += comment['rate']
        return result

    def update_rating(self, some_rate: models.IntegerField):
        self.rate = some_rate
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')
    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=24, choices=[('article', 'Статья'), ('news', 'Новость')])
    date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=124)
    text = models.TextField(blank=False)
    rate = models.IntegerField(default=0)

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def __str__(self):
        return f'{self.date} : {self.text} Author:{self.author.user}'

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def set_title(self):
        self.title = str(self.text)[:124]
        self.save()

    def preview(self):
        while not self.title:
            self.set_title()
        return (str(self.title)) + '...' if len(str(self.title)) == 124 else str(self.title)


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments_to_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()