from django import template


register = template.Library()


@register.filter()
def filename_item(page_obj):
    return page_obj.filename_item()


@register.filter()
def split_path(storage, exclude):
    splitted = str(storage).split("/")
    if splitted[0] == exclude:
        return splitted[1:]
    else:
        return splitted


@register.filter()
def custom_floatformat(number):
    if number % 1 == 0:
        return str(int(number))
    else:
        return str(number)


@register.filter()
def cas_format(number):
    str_cas = str(number)
    dashed_cas = str_cas[: -3] + "-" + str_cas[-3: -1] + "-" + str_cas[-1]
    return dashed_cas
