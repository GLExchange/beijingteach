from django.db import models
from django.core.mail import send_mail
from dashboard.models import Snippet, Img


class Position(models.Model):
    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.slug


class SnippetPos(Position):
    snippet = models.ForeignKey(Snippet, related_name="positions")


class ImgPos(Position):
    img = models.ForeignKey(Img, related_name="positions")


class Visitor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_valid = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)

    def send_mail(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class MessageManager(models.Manager):

    def new_message_from(self, name, email, **kwargs):
        v, _ = Visitor.objects.update_or_create(email=email,
                                                defaults={'name': name})
        return self.create(visitor=v, **kwargs)


class Message(models.Model):
    subject = models.CharField(max_length=140)
    content = models.TextField()
    visitor = models.ForeignKey(Visitor, related_name="messages")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    objects = MessageManager()


def init_all():
    pass
