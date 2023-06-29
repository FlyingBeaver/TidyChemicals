from django import template


register = template.Library()


@register.filter()
def filename_item(page_obj):
    return page_obj.filename_item()
