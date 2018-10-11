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
        {
            'key': 'address_line_1',
            'defaults': {
                'value': 'GlobalLearningXchange.com'
            },
        },
        {
            'key': 'address_line_2',
            'defaults': {
                'value': '38 Saint Marks Place'
            },
        },
        {
            'key': 'address_line_3',
            'defaults': {
                'value': 'Roslyn Heights, NY 11577'
            },
        },
        {
            'key': 'phone',
            'defaults': {
                'value': '+1 516 535 9236'
            },
        },
        {
            'key': 'copyright',
            'defaults': {
                'value': '2018 GlobalLearningXchange.com'
            },
        },
        {
            'key': 'facebook_link',
            'defaults': {
                'value': 'http://www.facebook.com/BeijingTeach'
            },
        },
        {
            'key': 'twitter_link',
            'defaults': {
                'value': 'http://www.twitter.com/BeijingTeach'
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
