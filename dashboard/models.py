from django.db import models


class Snippet(models.Model):
    subject = models.CharField(max_length=140)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return '{} ({})'.format(self.subject, self.updated)

    def has_pos(self):
        return len(SnippetPos.objects.filter(snippet=self)) == 1


class Img(models.Model):
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)


class Page(models.Model):
    subject = models.CharField(max_length=140)
    content = models.TextField(blank=True)
    style = models.TextField(blank=True)
    javascript = models.TextField(blank=True)
    is_inherited = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return '{} ({})'.format(self.subject, self.updated)

    def has_pos(self):
        return len(PagePos.objects.filter(page=self)) == 1


class Position(models.Model):
    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.slug


class SnippetPosManager(models.Manager):

    def get_snippet(self, **kwargs):
        sp = self.filter(**kwargs)
        return sp[0].snippet if sp else None


class SnippetPos(Position):
    snippet = models.OneToOneField(Snippet, related_name="position", null=True, blank=True)
    objects = SnippetPosManager()

    class Meta:
        verbose_name_plural = "Snippet Positons"


class PagePosManager(models.Manager):

    def get_page(self, **kwargs):
        pp = self.filter(**kwargs)
        return pp[0].page if pp else None

    def get_headers(self):
        raw_setting = SiteSetting.get('header_links')
        links = raw_setting.split('|')
        return self.filter(slug__in=links)


class PagePos(Position):
    page = models.OneToOneField(Page, related_name="position", null=True, blank=True)
    objects = PagePosManager()

    class Meta:
        verbose_name_plural = "Page Positons"

    @property
    def route(self):
        return u'/pages/{slug}'.format(slug=self.slug)


class ImgPos(Position):
    img = models.ForeignKey(Img, related_name="position", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Img Positons"


class SiteSetting(models.Model):
    key = models.SlugField(unique=True)
    value = models.CharField(max_length='50', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return '{ "%s": "%s" }' % (self.key, self.value)

    # needn't a set method cus it's for administrator in admin
    @classmethod
    def get(cls, k, default=None):
        k_set = cls.objects.filter(key=k)
        return default if len(k_set) < 1 else k_set[0].value
