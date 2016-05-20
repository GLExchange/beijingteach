from django import forms
from .models import Page, Img, PagePos


class StyledModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StyledModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.itervalues():
            field.widget.attrs['class'] = 'form-control'


class PageForm(StyledModelForm):

    POSITION_CHOICES = (('', '----------'),) + \
        tuple((pp.slug, pp.route) for pp in PagePos.objects.all())

    position = forms.CharField(
        required=False,
        label='position',
        widget=forms.Select(
            choices=POSITION_CHOICES,
        ),
    )

    class Meta:
        model = Page
        fields = ['subject', 'style', 'content', 'javascript', 'position', 'is_inherited']

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['style'].widget.attrs['rows'] = 3
        self.fields['javascript'].widget.attrs['rows'] = 3
        self.fields['content'].widget.attrs['rows'] = 25
        self.fields['position'].label = u'Route'
        self.fields['is_inherited'].label = u'Inherit original framework'

    def save(self):
        instance = super(PageForm, self).save()

        original_page_pos_set = PagePos.objects.filter(page=instance)
        if len(original_page_pos_set) == 1:
            original_page_pos_set[0].page = None
            original_page_pos_set[0].save()

        position = self.clean().get('position', '')
        page_pos_set = PagePos.objects.filter(slug=position)
        if len(page_pos_set) == 1:
            page_pos_set[0].page = instance
            page_pos_set[0].save()

        return instance


class ImgForm(forms.ModelForm):

    class Meta:
        model = Img
        fields = ['url']
