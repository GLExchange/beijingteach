from django.contrib import admin
from .models import Page, Img, ImgPos, SiteSetting, PagePos

admin.site.register(Page)
admin.site.register(Img)
admin.site.register(ImgPos)
admin.site.register(SiteSetting)
admin.site.register(PagePos)
