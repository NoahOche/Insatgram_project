import uuid

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  id_user = models.IntegerField()
  bio = models.TextField(null=True)
  profile_img = models.ImageField(upload_to='profile_images', default='avatar.png')

  def __str__(self) -> str:
    return str(self.user)


class Comment(models.Model):
  text = models.TextField()
  profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return '{}...'.format(self.text[:30])
class Post(models.Model):
  post_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
  image = models.ImageField(upload_to='post_images', default=None, blank=True, null=True)
  caption = models.CharField(max_length=200)
  created_at = models.DateTimeField(auto_now_add=True)
  liked = models.ManyToManyField(to=Profile, related_name='likes', blank=True)
  comments = models.ManyToManyField(to=Comment, related_name='comments')

  def __str__(self) -> str:
    return self.caption
  
  def get_likers_header(self):
    return self.liked.all()[:3]
  
  def get_comments_header(self):
    return self.comments.all().order_by('-created_at')[:4]
  

class Follow(models.Model):
  follower = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='following')
  following = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='followers')
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self) -> None:
    return '{} -> {}'.format(self.following, self.follower)
class Message(models.Model):
  text=models.TextField(null=False)
  sender= models.ForeignKey(to=Profile, on_delete=models.CASCADE,related_name='sender')
  receiver= models.ForeignKey(to=Profile, on_delete=models.CASCADE,related_name='receiver')
  created = models.DateTimeField(auto_now_add=True)