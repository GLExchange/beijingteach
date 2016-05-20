from django.db import models
from django.core.mail import send_mail


class Visitor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, default='')
    is_valid = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)

    def send_mail(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Message(models.Model):
    subject = models.CharField(max_length=140)
    content = models.TextField()
    visitor = models.ForeignKey(Visitor, related_name='messages', null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)


class AbstractBaseApplicant(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=16)

    class Meta:
        abstract = True


class AddressMixin(models.Model):
    address_1 = models.CharField(max_length=128)
    address_2 = models.CharField(max_length=128, blank=True)

    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=16)

    class Meta:
        abstract = True


class Applicant(AbstractBaseApplicant, AddressMixin):
    experiences = models.TextField()
    added_file_url = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
