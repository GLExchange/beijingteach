from django import template
from dashboard.models import PagePos, SiteSetting

register = template.Library()


@register.inclusion_tag('header_links.html')
def show_header_links():
    header_pos = PagePos.objects.get_headers()
    return locals()


@register.inclusion_tag('footer.html')
def show_footer():
    footer_elements = dict.fromkeys(['address_lines', 'phone', 'copyright',
                                     'facebook_link', 'twitter_link'])

    footer_elements['address_lines'] = [setting.value for setting in sorted(
        SiteSetting.objects.filter(key__startswith='address_line_'),
        key=lambda address: address.key.rsplit('_', 1)[-1],
    )]

    for k, v in footer_elements.iteritems():
        footer_elements[k] = v or SiteSetting.get(k, '')

    return footer_elements
