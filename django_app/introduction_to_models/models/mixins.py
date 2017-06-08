from django.db import models
from utils.models.mixins import TimeStampMixin


class Post(TimeStampMixin):
    author = models.OneToOneField('User')
    title = models.CharField(max_length=20)
    content = models.TextField()
    like_users = models.ManyToManyField(
        'User',
        through='Postlike',
        related_name='like_posts',
    )
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

    def like_post(self):
        return '이 포스트를 좋아요 한 사람 {}'.format(self.ahthor.like_post.all())


class Comment(TimeStampMixin):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey('User')
    content = models.TextField()


class User(TimeStampMixin):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


'''
실습하기
'''


class Tag(models.Model):
    title = models.CharField(max_length=50)


class Postlike(models.Model):
    post = models.ForeignKey('Post')
    user = models.ForeignKey('User')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{author}의 {post_title}Post에 대한 {like_user}의 좋아요. {like_datetime}'.format(
            author=self.post.author.name,
            post_title=self.post.title,
            like_user=self.user.name,
            like_datetime=self.created_date,
        )
