import os
from django.conf import settings
from django.core.management.base import BaseCommand
from dashboard.models import Page, PagePos, SiteSetting
from basic_templates import Translator

MARK_FILE_PATH = os.path.join(settings.BASE_DIR, 'basic_templates')


class Command(BaseCommand):

    page_pos_init_data = [
        {'slug': 'about'},
        {'slug': 'experience'},
        {'slug': 'china'},
        {'slug': 'accommodation'},
    ]

    site_setting_init_data = [
        {
            'key': 'header_links',
            'defaults': {
                'value': '|'.join(d['slug'] for d in page_pos_init_data)
            },
        },
    ]

    def add_arguments(self, parser):
        parser.add_argument('--with-templates',
                            action='store_true',
                            dest='with_templates',
                            default=False,
                            help='Create default templates.')

    def handle(self, *args, **options):

        for d in self.page_pos_init_data:
            print 'Update or create PagePos(%s)' % d
            PagePos.objects.update_or_create(**d)

        for d in self.site_setting_init_data:
            print 'Update or create SiteSetting(%s)' % d
            SiteSetting.objects.update_or_create(**d)

        if options['with_templates']:
            self.auto_templates()

        print 'All Done!\nMay your system never fail!'

    def auto_templates(self):
        print 'Create default templates...'

        page_slugs = (d['slug'] for d in self.page_pos_init_data)
        for slug in page_slugs:
            print 'Create default templates of %s' % slug
            data = self.translate_mark_file(slug)
            new_page = Page.objects.create(**data)
            pp = PagePos.objects.get(slug=slug)
            pp.page = new_page
            pp.save()

    def translate_mark_file(self, slug):
        filename = slug + '.html'
        filepath = os.path.join(MARK_FILE_PATH, filename)

        with Translator(filepath) as t:
            data = t.translate()

        data['subject'] = slug
        return data
